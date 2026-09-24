#!/usr/bin/env python3
"""collect_handoff.py <run-id> [--path X] [--keep-think] —— 回收落地：
从 run.ndjson 抽最终 assistant 文本写成 Handoff 文件，把实际路径回填进
status.json 的 handoff_paths（契约输出表里此前无人实现的字段），
并对「最终文本与任务体量不相称」给 suspicious 警告（半成品防线）。

只在 state=done 时允许回收；truncated/stuck 的 run 先按失败处置，不许收 half-baked 产物。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_status import RUNS_ROOT, classify  # noqa: E402

MIN_EXPECTED_CHARS = 200  # 低于此长度的「完成」值得人工复核


def final_text(run_dir: Path) -> str:
    chunks: list[str] = []
    for line in (run_dir / "run.ndjson").read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        update = (event.get("params") or {}).get("update") or {}
        if update.get("sessionUpdate") != "agent_message_chunk":
            continue
        content = update.get("content") or {}
        if content.get("type") == "text":
            chunks.append(content.get("text", ""))
    return "".join(chunks)


def strip_think(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    # 未闭合的 <think>：截到文本末尾；但若截完什么都不剩，说明全文都在 think
    # 里（模型没收尾），退回原文并交由 suspicious 警告与人工核对——宁留噪声不误删产出
    i = text.rfind("<think>")
    if i >= 0 and text[:i].strip():
        text = text[:i]
    return text.strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="回收 Handoff：抽最终文本、回填 handoff_paths")
    p.add_argument("run_id")
    p.add_argument("--path", default=None, help="Handoff 输出路径；缺省 run 目录下 handoff.md")
    p.add_argument("--keep-think", action="store_true", help="保留 <think> 段（默认剥掉）")
    args = p.parse_args(argv)

    run_dir = Path(args.run_id)
    if not run_dir.is_dir():
        run_dir = RUNS_ROOT / args.run_id
    if not run_dir.is_dir():
        print(f"error: run 目录不存在: {run_dir}", file=sys.stderr)
        return 2

    report = classify(run_dir)
    if report["state"] != "done":
        print(f"error: state={report['state']}，不是 done——先按失败处置，不收半成品", file=sys.stderr)
        return 1

    text = final_text(run_dir)
    if not args.keep_think:
        text = strip_think(text)
    if not text:
        print("error: 最终文本为空", file=sys.stderr)
        return 1

    out = Path(args.path) if args.path else run_dir / "handoff.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n", encoding="utf-8")

    status_path = run_dir / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    paths = status.get("handoff_paths") or []
    if str(out) not in paths:
        paths.append(str(out))
    status["handoff_paths"] = paths
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"handoff: {out}（{len(text)} 字符）")
    if len(text) < MIN_EXPECTED_CHARS:
        print(f"warning: suspicious——完成文本仅 {len(text)} 字符，低于 {MIN_EXPECTED_CHARS}，"
              "请人工核对是否与任务体量相称（半成品防线，不是判定）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
