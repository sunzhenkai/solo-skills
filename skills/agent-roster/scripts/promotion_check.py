#!/usr/bin/env python3
"""promotion_check.py —— 固化门槛核对：同一句「为什么选它」是否已在 ≥2 条
不同任务的 Trace 里复现（SKILL.md 固化节的计数规则）。

做法：扫 traces/ 每个文件的「候选与选择」段，抽取含「因为/理由是」的选择句，
跨文件精确计数。>=2 次的打印提案草稿（哪几条 trace、哪句理由）；
计数与提案去向仍由人确认——脚本替代的是「没人去数」，不是确认权。

注意：理由抽取是启发式（确定性文本切片），抽错时以 trace 原文为准。
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _roster import traces_dir  # noqa: E402

REASON_PAT = re.compile(r"[^\n。]*(?:因为|理由是|所以选)[^\n。]*")


def selection_section(text: str) -> str:
    m = re.search(r"^##\s+候选与选择.*?$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def extract_reasons(text: str) -> list[str]:
    sec = selection_section(text)
    out = []
    for m in REASON_PAT.finditer(sec):
        s = re.sub(r"\s+", "", m.group(0))
        # 去掉模板噪声与纯元信息句
        for noise in ("从run目录的decision.md原样搬过来", "不要重写", ">从run目录"):
            s = s.replace(noise, "")
        s = s.strip(" ，。：:>*-")
        if len(s) >= 10 and not s.startswith(("Rework", "提案", "依据")):
            out.append(s)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="固化门槛核对（同一理由跨任务 >=2 次复现）")
    p.add_argument("--threshold", type=int, default=2)
    args = p.parse_args(argv)

    td = traces_dir()
    if not td.is_dir():
        print(f"error: {td} 不存在", file=sys.stderr)
        return 2

    counts: dict[str, set[str]] = defaultdict(set)
    for f in sorted(td.glob("*.md")):
        for reason in extract_reasons(f.read_text(encoding="utf-8", errors="replace")):
            counts[reason].add(f.name)

    hits = [(r, files) for r, files in counts.items() if len(files) >= args.threshold]
    if not hits:
        print(f"verdict: 无达到门槛（>= {args.threshold} 条不同任务 Trace）的复现理由")
        print("动作: 不提案。继续攒 Trace；写完新 Trace 后 rerun 本脚本。")
        return 0

    print(f"verdict: {len(hits)} 条理由达到固化门槛——提案草稿：")
    for reason, files in sorted(hits, key=lambda x: -len(x[1])):
        print(f"\n- 理由: {reason}")
        print(f"  复现于 {len(files)} 条 trace:")
        for name in sorted(files):
            print(f"    - {name}")
        print("  建议: 停下来向使用者提案（routing.md 还是 patches/ 由人去向判断），"
              "使用者确认后才写入。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
