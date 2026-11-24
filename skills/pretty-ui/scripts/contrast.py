#!/usr/bin/env python3
"""按 WCAG 对比度门槛校验文字 / 背景配对。

移植并改写自 edisonmbli/refactoring-ui-skill 的 scripts/check_contrast.py
（MIT © 2026 Edison Li，许可全文见 ../licenses/refactoring-ui-skill-MIT.txt）。
改动：中文说明与修法提示。

门槛：正文至少 4.5:1；18px 以上或 14px 粗体以上的大字至少 3:1。
支持 #rgb / #rgba / #rrggbb / #rrggbbaa、rgb(...) / rgba(...) 与 rgb(r g b / a)（前景色含透明度时按背景合成后计算）。
--brightness 报告感知亮度（解释为什么同样的 HSL 明度下黄色比蓝色显得亮）。

只依赖 Python 3 标准库。

  python3 contrast.py --pair '#6b7280' '#ffffff'
  python3 contrast.py --pair '#ffffff' '#0f7b6c' --size large
  python3 contrast.py --matrix pairs.json
  python3 contrast.py --brightness '#eab308' '#2563eb'

pairs.json：{"pairs": [{"name": "正文", "fg": "#111827", "bg": "#ffffff", "size": "normal"}]}

有任何配对不达标时退出码为 1，输入有误时为 2，可直接当门禁用。
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys

AA_NORMAL, AA_LARGE = 4.5, 3.0


def hex_to_rgb(s: str) -> tuple[int, int, int]:
    r, g, b, _ = parse_rgba(s)
    return r, g, b


def parse_rgba(s: str) -> tuple[int, int, int, float]:
    """解析 #rgb/#rgba/#rrggbb/#rrggbbaa、rgb()/rgba() 与 rgb(r g b / a)。"""
    raw = s.strip()
    if raw.startswith("#") or re.fullmatch(r"[0-9a-fA-F]{3,8}", raw):
        h = raw.lstrip("#")
        if len(h) in (3, 4) and re.fullmatch(r"[0-9a-fA-F]{3,4}", h):
            h = "".join(c * 2 for c in h)
        if len(h) == 6 and re.fullmatch(r"[0-9a-fA-F]{6}", h):
            r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
            return r, g, b, 1.0
        if len(h) == 8 and re.fullmatch(r"[0-9a-fA-F]{8}", h):
            r, g, b, a = (int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
            return r, g, b, a / 255.0
        raise ValueError(f"不是十六进制颜色：{raw}")

    m = re.fullmatch(r"rgba?\(\s*(.+?)\s*\)", raw, re.I)
    if not m:
        raise ValueError(f"不支持的颜色格式：{raw}")
    inner = m.group(1)
    if "," in inner:
        parts = [p.strip() for p in inner.split(",")]
        if len(parts) not in (3, 4):
            raise ValueError(f"颜色参数数量有误：{raw}")
        rgb_parts, alpha_str = parts[:3], (parts[3] if len(parts) == 4 else None)
    else:
        if "/" in inner:
            left, alpha_str = [p.strip() for p in inner.split("/", 1)]
        else:
            left, alpha_str = inner, None
        rgb_parts = left.split()
        if len(rgb_parts) != 3:
            raise ValueError(f"颜色参数数量有误：{raw}")

    rgb: list[int] = []
    for p in rgb_parts:
        val = float(p)
        if not (0.0 <= val <= 255.0):
            raise ValueError(f"RGB 超出 0–255 范围：{raw}")
        rgb.append(round(val))

    if alpha_str is None:
        alpha = 1.0
    elif alpha_str.endswith("%"):
        alpha = float(alpha_str[:-1]) / 100.0
    else:
        alpha = float(alpha_str)
    if not (0.0 <= alpha <= 1.0):
        raise ValueError(f"透明度超出 0–1 范围：{raw}")
    return rgb[0], rgb[1], rgb[2], alpha


def composite_over(fg: tuple[int, int, int, float], bg: tuple[int, int, int]) -> tuple[int, int, int]:
    """将带透明度的前景色合成到不透明背景色上。"""
    r, g, b, a = fg
    if a >= 1.0:
        return r, g, b
    return (
        round(a * r + (1.0 - a) * bg[0]),
        round(a * g + (1.0 - a) * bg[1]),
        round(a * b + (1.0 - a) * bg[2]),
    )


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.x 相对亮度，4.5:1 等门槛按它定义。"""

    def lin(c: int) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    fg = parse_rgba(a)
    bg = parse_rgba(b)
    if bg[3] < 1.0:
        raise ValueError("背景色需为不透明颜色")
    fg_rgb = composite_over(fg, bg[:3])
    la, lb = relative_luminance(fg_rgb), relative_luminance(bg[:3])
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def perceived_brightness(c: str) -> float:
    """感知亮度 sqrt(0.299r² + 0.587g² + 0.114b²) / 255，和 WCAG 亮度不是一回事。"""
    r, g, b = hex_to_rgb(c)
    return math.sqrt(0.299 * r * r + 0.587 * g * g + 0.114 * b * b) / 255


def verdict(ratio: float, size: str) -> tuple[bool, str]:
    need = AA_LARGE if size == "large" else AA_NORMAL
    ok = ratio >= need
    label = "大字" if size == "large" else "正文"
    return ok, f"{'PASS' if ok else 'FAIL'}  {ratio:.2f}:1（{label}需要 {need}:1）"


def advise(fg: str, bg: str, size: str) -> list[str]:
    tips = []
    if perceived_brightness(bg) < 0.45:
        tips.append("翻转：深色有色底上的浅字，改成同色相浅底上的深色字")
        tips.append("或转色相：把文字色相向青、品红、黄转一点（不超过 20–30°），不变白也能提高对比")
    else:
        tips.append("把文字沿色阶往深处挪一两级")
    if size == "normal":
        tips.append("如果这是 18px 以上（或 14px 粗体以上）的大字，只需要 3:1，用 --size large 再查")
    return tips


def check_matrix(path: str, size: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{path}：读不了（{e}）", file=sys.stderr)
        return 2
    pairs = data.get("pairs") if isinstance(data, dict) else None
    if not pairs:
        print(f"{path}：没有找到 pairs 数组；列出界面里真实出现的文字 / 背景组合", file=sys.stderr)
        return 2
    failures = 0
    width = max((len(p.get("name", "")) for p in pairs), default=4)
    for p in pairs:
        s = p.get("size", size)
        ok, line = verdict(contrast_ratio(p["fg"], p["bg"]), s)
        failures += not ok
        print(f"{p.get('name', ''):<{width}}  {p['fg']} 在 {p['bg']} 上  {line}")
        if not ok:
            for t in advise(p["fg"], p["bg"], s):
                print(f"{'':<{width}}    → {t}")
    print(f"\n{len(pairs) - failures}/{len(pairs)} 通过")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"), help="校验一组配对")
    ap.add_argument("--matrix", metavar="PAIRS.JSON", help="校验一份配对清单")
    ap.add_argument("--brightness", nargs="+", metavar="COLOR", help="报告感知亮度")
    ap.add_argument("--size", choices=("normal", "large"), default="normal", help="normal 为正文（4.5:1），large 为大字（3:1）")
    a = ap.parse_args()

    try:
        if a.brightness:
            for c in a.brightness:
                print(f"{c}  感知亮度 {perceived_brightness(c):.3f}  WCAG 亮度 {relative_luminance(hex_to_rgb(c)):.3f}")
            return 0
        if a.pair:
            fg, bg = a.pair
            ok, line = verdict(contrast_ratio(fg, bg), a.size)
            print(f"{fg} 在 {bg} 上   {line}")
            if not ok:
                for t in advise(fg, bg, a.size):
                    print(f"  → {t}")
            return 0 if ok else 1
        if a.matrix:
            return check_matrix(a.matrix, a.size)
    except (ValueError, KeyError) as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2
    ap.error("需要 --pair、--matrix 或 --brightness")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
