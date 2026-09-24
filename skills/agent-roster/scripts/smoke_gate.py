#!/usr/bin/env python3
"""smoke_gate.py <host>/<kind> [model] —— 冒烟门禁裁决：该 Endpoint+模型组合
有没有 L3 成功记录。有 → 输出 skip（正式委派可不发冒烟）；没有 → 输出 required
并给出 delegate.py 冒烟命令。

记录来源（契约「冒烟门禁」的两处）：
1. 画像 <data_root>/agents/<host>/<kind>.md 的「探测状态」段里含该模型的 L3 ✅ 行
2. traces/ 里同时提到该 Endpoint、该模型且 Outcome: completed 的 Trace

只做确定性文本匹配，不解析自然语言。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _roster import agents_dir, traces_dir  # noqa: E402


def section(text: str, header_prefix: str) -> str:
    m = re.search(rf"^##\s+{re.escape(header_prefix)}.*?$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def profile_l3_hits(profile: Path, model: str | None) -> list[str]:
    if not profile.exists():
        return []
    sec = section(profile.read_text(encoding="utf-8"), "探测状态")
    hits = [ln.strip() for ln in sec.splitlines() if "L3" in ln and "✅" in ln]
    if model:
        hits = [ln for ln in hits if model in ln]
    return hits


def trace_hits(kind: str, model: str | None) -> list[str]:
    td = traces_dir()
    if not td.is_dir():
        return []
    out = []
    for f in sorted(td.glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if kind not in t:
            continue
        if model and model not in t:
            continue
        if not re.search(r"Outcome:\s*completed", t):
            continue
        if re.search(r"L3\s*✅", t) or model:
            out.append(f.name)
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="冒烟门禁裁决（确定性）")
    p.add_argument("endpoint", help="host/kind，如 example-host/codex")
    p.add_argument("model", nargs="?", default=None, help="模型 id；缺省只看该 kind 有无任何 L3 成功记录")
    args = p.parse_args(argv)

    if "/" not in args.endpoint:
        print("error: endpoint 须为 host/kind 形态", file=sys.stderr)
        return 2
    host, kind = args.endpoint.split("/", 1)

    profile = agents_dir() / host / f"{kind}.md"
    phits = profile_l3_hits(profile, args.model)
    thits = trace_hits(kind, args.model)

    if phits or thits:
        print("verdict: skip")
        print("理由: 已有 L3 成功记录——")
        for ln in phits:
            print(f"  画像 {host}/{kind}.md: {ln}")
        for name in thits:
            print(f"  trace: {name}")
        return 0

    print("verdict: required")
    why = f"该模型（{args.model}）" if args.model else "任何模型"
    print(f"理由: {host}/{kind} 没有{why}的 L3 成功记录（画像与 trace 均无）")
    model_flag = f" --model {args.model}" if args.model else ""
    print("冒烟命令:")
    print(f"  python3 {Path(__file__).resolve().parent}/delegate.py "
          f"--endpoint {host}/{kind} --kind {kind}{model_flag} "
          f"--cwd <工作目录> --timeout 120 --slug smoke-{kind} "
          f"--reason 'L3 冒烟门禁' --smoke")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
