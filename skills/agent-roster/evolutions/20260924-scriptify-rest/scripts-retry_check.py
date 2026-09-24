#!/usr/bin/env python3
"""retry_check.py <run-id> —— 重试前检查单（契约「同一 Endpoint 只重发一次」的前置门禁）。

四项全过才输出 retry-allowed；任一不满足输出差在哪一步并 exit 1：
1. 记录的 PID 已退出（os.kill(pid, 0)，不用 pgrep -f，避开自匹配假等待）
2. 无残留适配器子进程（按 run 的 kind 查 /proc 真实 cmdline，排除自身与祖先）
3. run.ndjson 体积复查两次停涨（前一轮确实死了）
4. 失败已归类（run_status 判为 stuck / truncated / timed-out / cancelled，done 不许重发）

「同一 Endpoint 只重发一次」的额度核对不由本脚本判断——它不知道历史，交由调用方。
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_status import RUNS_ROOT, classify  # noqa: E402

# kind -> 适配器进程特征串（出现在 /proc/*/cmdline 里即视为残留）
ADAPTER_MARKERS: dict[str, list[str]] = {
    "claude": ["claude-agent-acp"],
    "codex": ["codex-acp"],
    "opencode": ["opencode"],
    "qwen": ["qwen", "--acp"],
    "pi": ["pi-acp"],
    "cursor": ["cursor-agent"],
    "kiro": ["kiro-cli-chat"],
    "gemini": ["gemini", "--acp"],
    "copilot": ["copilot", "--acp"],
}

FAILED_STATES = {"stuck", "truncated", "timed-out", "cancelled"}


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def ancestor_pids() -> set[int]:
    out: set[int] = {os.getpid()}
    pid = os.getpid()
    for _ in range(64):
        try:
            with open(f"/proc/{pid}/stat", encoding="ascii", errors="replace") as fh:
                pid = int(fh.read().rsplit(")", 1)[1].split()[1])
        except (FileNotFoundError, IndexError, ValueError, PermissionError):
            break
        if pid <= 1:
            break
        out.add(pid)
    return out


def residual_adapters(kind: str) -> list[str]:
    markers = ADAPTER_MARKERS.get(kind, [kind])
    skip = ancestor_pids()
    found = []
    proc = Path("/proc")
    if not proc.is_dir():
        return []  # 非 Linux：跳过此项（由 pid/体积两项兜底）
    for entry in proc.iterdir():
        if not entry.name.isdigit() or int(entry.name) in skip:
            continue
        try:
            cmdline = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace")
        except (FileNotFoundError, PermissionError):
            continue
        if markers and all(m in cmdline for m in markers[:1]) and any(m in cmdline for m in markers):
            found.append(f"pid={entry.name} cmd={cmdline.strip()[:100]}")
    return found


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="重试前检查单（确定性四项）")
    p.add_argument("run_id")
    args = p.parse_args(argv)

    run_dir = Path(args.run_id)
    if not run_dir.is_dir():
        run_dir = RUNS_ROOT / args.run_id
    if not run_dir.is_dir():
        print(f"error: run 目录不存在: {run_dir}", file=sys.stderr)
        return 2

    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    kind = status.get("kind", "")
    pid = status.get("pid")
    ndjson = run_dir / "run.ndjson"

    checks: list[tuple[bool, str]] = []

    alive = pid_alive(pid) if isinstance(pid, int) else False
    checks.append((not alive, f"1. 记录 PID {pid} 已退出" + ("（仍在运行——先等或 --kill）" if alive else "")))

    residual = residual_adapters(kind)
    checks.append((not residual, "2. 无残留适配器子进程" + (f"（发现 {len(residual)} 个：）" if residual else "")))
    for r in residual:
        checks.append((False, f"   {r}"))

    if ndjson.exists():
        s1 = ndjson.stat().st_size
        time.sleep(2)
        s2 = ndjson.stat().st_size
        stable = s1 == s2
        checks.append((stable, f"3. ndjson 体积停涨（{s1}B -> {s2}B）" + ("" if stable else "（仍在增长！）")))
    else:
        checks.append((True, "3. 无 ndjson（not-started，视为停涨）"))

    report = classify(run_dir)
    state = report["state"]
    checks.append((state in FAILED_STATES, f"4. 失败已归类: {state}（{report['action']}）"))

    for ok, label in checks:
        print(f"{'✅' if ok else '❌'} {label}")

    if all(ok for ok, _ in checks):
        print("verdict: retry-allowed")
        print("提醒: 「同一 Endpoint 只重发一次」的额度核对是调用方的责任，本脚本不知道历史。")
        return 0
    print("verdict: retry-blocked")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
