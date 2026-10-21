#!/usr/bin/env python3
"""生成一条 9 级色阶（100–900，可选 50 / 950）。

移植并改写自 edisonmbli/refactoring-ui-skill 的 scripts/generate_palette.py
（MIT © 2026 Edison Li，许可全文见 ../licenses/refactoring-ui-skill-MIT.txt）。
改动：中文说明、新增 --css 输出 CSS 变量。

算法：
  1. 主色放 500，先定两端 100 / 900，再二分出 700 / 300，再二分出 800 / 600 / 400 / 200；
  2. 明度离 50% 越远饱和度越高，避免两端发灰；
  3. 变浅时色相向亮色相（黄、青、品红）转，变深时向暗色相（红、绿、蓝）转，转动有上限；
  4. 灰阶带冷暖，最浅一级停在接近白而不是纯白。

只依赖 Python 3 标准库。

  python3 palette.py --base '#0f7b6c' --name brand
  python3 palette.py --base 'hsl(15, 65%, 45%)' --extended --css
  python3 palette.py --grey --temperature warm --css
  python3 palette.py --base '#d97706' --name warning --json
"""
from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys

BRIGHT_HUES = (60.0, 180.0, 300.0)  # 感知亮度的波峰：变浅时转向这里
DARK_HUES = (0.0, 120.0, 240.0)  # 感知亮度的波谷：变深时转向这里


def hex_to_hsl(s: str) -> tuple[float, float, float]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"不是十六进制颜色：{s}")
    r, g, b = (int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, light, sat = colorsys.rgb_to_hls(r, g, b)
    return h * 360, sat * 100, light * 100


def hsl_to_hex(h: float, s: float, light: float) -> str:
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, light / 100, s / 100)
    return "#%02x%02x%02x" % tuple(round(c * 255) for c in (r, g, b))


def parse_color(s: str) -> tuple[float, float, float]:
    """接受 #rgb、#rrggbb 或 hsl(h, s%, l%)。"""
    m = re.match(r"hsl\(\s*([\d.]+)\s*[, ]\s*([\d.]+)%?\s*[, ]\s*([\d.]+)%?\s*\)", s.strip(), re.I)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3))
    return hex_to_hsl(s)


def fmt_hsl(h: float, s: float, light: float) -> str:
    return f"hsl({h % 360:.0f}, {s:.0f}%, {light:.0f}%)"


def _chroma_headroom(light: float) -> float:
    """HSL 色度 = (1 - |2L-1|) * S，返回 (1 - |2L-1|)；越靠两端越小。"""
    return max(1e-6, 1.0 - abs(2.0 * (light / 100.0) - 1.0))


def compensate_saturation(s_base: float, l_base: float, l_target: float, strength: float = 0.55) -> float:
    """明度离 50% 越远，饱和度抬得越高，让色度在感知上保持平稳。

    strength 为 0 时关闭补偿，为 1 时完全保持色度（两端会很快顶到 100%）。
    """
    if s_base <= 0:
        return 0.0
    ratio = _chroma_headroom(l_base) / _chroma_headroom(l_target)
    return min(100.0, s_base * (ratio ** strength))


def _signed_delta(frm: float, to: float) -> float:
    """最短的带符号角度差，范围 (-180, 180]。"""
    return (to - frm + 180.0) % 360.0 - 180.0


def _nearest(h: float, targets: tuple[float, ...], prefer: str = "auto") -> float:
    """最近的目标色相；红色这类到两个目标等距时，按 prefer 决定偏暖还是偏冷。"""
    if prefer in ("warm", "cool"):
        want = 1.0 if prefer == "warm" else -1.0
        ranked = sorted(targets, key=lambda t: (abs(_signed_delta(h, t)), -want * _signed_delta(h, t)))
        return ranked[0]
    return min(targets, key=lambda t: abs(_signed_delta(h, t)))


def rotate_hue(h_base: float, l_base: float, l_target: float, cap: float = 20.0, prefer: str = "auto") -> float:
    """变浅转向亮色相、变深转向暗色相；幅度随明度变化量增长，并被 cap 截断。"""
    if l_target == l_base:
        return h_base
    lighten = l_target > l_base
    target = _nearest(h_base, BRIGHT_HUES if lighten else DARK_HUES, prefer)
    delta = _signed_delta(h_base, target)
    span = (100.0 - l_base) if lighten else l_base
    if span <= 0:
        return h_base
    progress = min(1.0, abs(l_target - l_base) / span)
    return h_base + max(-cap, min(cap, delta * progress))


def bisect_lightness(l_light: float, l_base: float, l_dark: float) -> dict[int, float]:
    """900 / 500 / 100 → 700 / 300 → 800 / 600 / 400 / 200。"""
    lv = {900: l_dark, 500: l_base, 100: l_light}
    lv[700] = (lv[900] + lv[500]) / 2
    lv[300] = (lv[500] + lv[100]) / 2
    lv[800] = (lv[900] + lv[700]) / 2
    lv[600] = (lv[700] + lv[500]) / 2
    lv[400] = (lv[500] + lv[300]) / 2
    lv[200] = (lv[300] + lv[100]) / 2
    return lv


def build_ramp(
    base: tuple[float, float, float],
    l_light: float | None = None,
    l_dark: float | None = None,
    strength: float = 0.55,
    cap: float = 20.0,
    extended: bool = False,
    prefer: str = "auto",
) -> dict[int, dict]:
    h0, s0, l0 = base
    l_light = 96.0 if l_light is None else l_light
    l_dark = 21.0 if l_dark is None else l_dark
    if not (l_dark < l0 < l_light):
        raise ValueError(f"主色明度 {l0:.0f}% 要落在 --darkest {l_dark:.0f}% 与 --lightest {l_light:.0f}% 之间")
    lv = bisect_lightness(l_light, l0, l_dark)
    if extended:
        lv[50] = l_light + (100.0 - l_light) * 0.55
        lv[950] = l_dark * 0.55
    out = {}
    for stop in sorted(lv):
        lt = lv[stop]
        h = h0 if stop == 500 else rotate_hue(h0, l0, lt, cap, prefer)
        s = s0 if stop == 500 else compensate_saturation(s0, l0, lt, strength)
        out[stop] = {
            "h": round(h % 360, 1),
            "s": round(s, 1),
            "l": round(lt, 1),
            "hex": hsl_to_hex(h, s, lt),
            "hsl": fmt_hsl(h, s, lt),
        }
    return out


def grey_base(temperature: str, saturation: float) -> tuple[float, float, float]:
    """冷灰偏蓝、暖灰偏黄橙，中性灰不带色相。"""
    hue = {"cool": 220.0, "warm": 35.0, "neutral": 0.0}[temperature]
    return hue, (0.0 if temperature == "neutral" else saturation), 50.0


def to_css(name: str, ramp: dict[int, dict]) -> str:
    lines = [":root {"]
    lines += [f"  --color-{name}-{stop}: {c['hex']};" for stop, c in ramp.items()]
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", help="主色，如 '#0f7b6c' 或 'hsl(15,65%%,45%%)'；用项目真实的品牌色")
    p.add_argument("--grey", action="store_true", help="生成灰阶")
    p.add_argument("--temperature", choices=("cool", "warm", "neutral"), default="cool", help="灰阶冷暖（默认 cool）")
    p.add_argument("--grey-saturation", type=float, default=12.0, help="灰阶带色的程度（默认 12）")
    p.add_argument("--lightest", type=float, help="100 级的明度%%（默认 96，灰阶 98）")
    p.add_argument("--darkest", type=float, help="900 级的明度%%（默认 21，灰阶 17）")
    p.add_argument("--strength", type=float, default=0.55, help="饱和度补偿强度，0 关闭，1 完全保持色度")
    p.add_argument("--cap", type=float, default=20.0, help="色相转动上限（度），超过 30 会读成另一种颜色")
    p.add_argument("--extended", action="store_true", help="额外输出 50 与 950 两级")
    p.add_argument(
        "--toward",
        choices=("auto", "warm", "cool"),
        default="auto",
        help="两个目标色相等距时（红色常见）的取向：warm 偏橙黄，cool 偏品红蓝",
    )
    p.add_argument("--name", default="color", help="色阶名，用于输出")
    out = p.add_mutually_exclusive_group()
    out.add_argument("--json", action="store_true", help="输出 JSON")
    out.add_argument("--css", action="store_true", help="输出 CSS 变量 --color-<name>-<级>")
    a = p.parse_args()

    if a.cap > 30:
        print("提示：--cap 超过 30° 会读成另一种颜色，而不是同色的深浅", file=sys.stderr)
    try:
        if a.grey:
            base = grey_base(a.temperature, a.grey_saturation)
            name = a.name if a.name != "color" else "neutral"
            light = 98.0 if a.lightest is None else a.lightest
            dark = 17.0 if a.darkest is None else a.darkest
        elif a.base:
            base, name, light, dark = parse_color(a.base), a.name, a.lightest, a.darkest
        else:
            p.error("需要 --base COLOR 或 --grey")
        ramp = build_ramp(base, light, dark, a.strength, a.cap, a.extended, a.toward)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps({name: {str(k): v for k, v in ramp.items()}}, indent=2, ensure_ascii=False))
    elif a.css:
        print(to_css(name, ramp))
    else:
        print(f"{name}   主色 {fmt_hsl(*base)}   strength={a.strength} cap={a.cap}°")
        print(f"{'级':>5}  {'hex':<9} {'hsl':<22}")
        for stop, c in ramp.items():
            mark = "  ← 主色" if stop == 500 else ""
            print(f"{stop:>5}  {c['hex']:<9} {c['hsl']:<22}{mark}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
