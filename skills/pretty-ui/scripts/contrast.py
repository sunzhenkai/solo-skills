#!/usr/bin/env python3
"""按 WCAG 对比度门槛校验文字 / 背景配对。

移植并改写自 edisonmbli/refactoring-ui-skill 的 scripts/check_contrast.py
（MIT © 2026 Edison Li，许可全文见 ../licenses/refactoring-ui-skill-MIT.txt）。
改动：中文说明与修法提示。

门槛：正文至少 4.5:1；18px 以上或 14px 粗体以上的大字至少 3:1。
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
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"不是十六进制颜色：{s}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.x 相对亮度，4.5:1 等门槛按它定义。"""

    def lin(c: int) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(hex_to_rgb(a)), relative_luminance(hex_to_rgb(b))
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
