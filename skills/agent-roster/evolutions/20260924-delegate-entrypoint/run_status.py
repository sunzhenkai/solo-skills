#!/usr/bin/env python3
"""run_status.py <run-id|run-dir> [--json] —— acpx 委派运行的确定性状态判定。

状态指纹（依据 2026-09-24 实测，见 agent-roster 契约「受控执行」）：
- done        session/prompt 的 RESULT stopReason=end_turn 且最终文本非空
              （注意：请求 id 不是固定的 0/1/2——set_config_option（如 acpx 应用
              --model）会占用一个 id，prompt RESULT 实测落在 id=3。必须按
              session/prompt 事件的实际 id 匹配，不能硬编码）
- stuck       恰好停在 initialize/RESULT/session/new 三事件，无 RESULT(id=1)（会话建立无响应）
- cancelled   出现 session/cancel
- truncated   prompt 已发、有 update 流，但无 RESULT(id=2)（被截断的半成品）
- timed-out   status.json 记录的 timeout 已到期且未 done
- running     pid 存活（先等再判；体积多次复查不涨按 stuck/truncated 处置）
- not-started 无 run.ndjson

只做确定性判定，不解析自然语言意图。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

RUNS_ROOT = Path.home() / ".cache" / "agent-roster" / "runs"


def load_events(ndjson: Path) -> list[dict]:
    if not ndjson.exists():
        return []
    events: list[dict] = []
    for line in ndjson.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def result_for(events: list[dict], request_id: object) -> dict | None:
    """取该请求 id 的最后一个响应——中间可能有权限请求等同 id 响应（如 outcome:selected）。"""
    for event in reversed(events):
        if event.get("id") == request_id and ("result" in event or "error" in event):
            return event
    return None


def final_text_length(events: list[dict]) -> int:
    total = 0
    for event in events:
        update = (event.get("params") or {}).get("update") or {}
        if update.get("sessionUpdate") == "agent_message_chunk":
            content = update.get("content") or {}
            if content.get("type") == "text":
                total += len(content.get("text", ""))
    return total


def classify(run_dir: Path, now: float | None = None) -> dict:
    now = now if now is not None else time.time()
    ndjson = run_dir / "run.ndjson"
    status_path = run_dir / "status.json"
    pid_path = run_dir / "pid"

    status: dict = {}
    if status_path.exists():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            status = {}

    pid: int | None = None
    if pid_path.exists():
        try:
            pid = int(pid_path.read_text().strip())
        except ValueError:
            pid = None
    pid = status.get("pid", pid)

    pid_alive = False
    if isinstance(pid, int):
        try:
            os.kill(pid, 0)
            pid_alive = True
        except ProcessLookupError:
            pid_alive = False
        except PermissionError:
            pid_alive = True

    events = load_events(ndjson)
    size = ndjson.stat().st_size if ndjson.exists() else 0
    init_result = result_for(events, 0)
    session_result = result_for(events, 1)
    prompt_id = None
    for event in events:
        if event.get("method") == "session/prompt":
            prompt_id = event.get("id")
    prompt_sent = prompt_id is not None
    final = result_for(events, prompt_id) if prompt_sent else None
    if final is None:
        # 兜底：任何带 stopReason 的 RESULT 都视为 prompt 的响应
        for event in reversed(events):
            if "stopReason" in (event.get("result") or {}):
                final = event
                break
    stop_reason = (final or {}).get("result", {}).get("stopReason") if final else None
    text_length = final_text_length(events)
    cancelled = any(
        event.get("method") == "session/cancel"
        or ((event.get("params") or {}).get("update") or {}).get("sessionUpdate") == "session_cancelled"
        for event in events
    )

    started = status.get("started_at")
    timeout_seconds = status.get("timeout_seconds")
    timed_out = False
    if isinstance(started, (int, float)) and isinstance(timeout_seconds, (int, float)):
        timed_out = now > started + timeout_seconds

    if not events:
        state = "not-started"
    elif stop_reason == "end_turn" and text_length > 0:
        state = "done"
    elif timed_out:
        state = "timed-out"
    elif cancelled:
        state = "cancelled"
    elif init_result is not None and len(events) <= 3 and session_result is None:
        state = "stuck"
    elif pid_alive:
        state = "running"
    elif prompt_sent and final is None:
        state = "truncated"
    elif session_result is None:
        state = "stuck"
    else:
        state = "truncated" if prompt_sent else "unknown"

    actions = {
        "not-started": "委派尚未产生事件流：确认命令是否真的启动（stderr 与退出码）。",
        "done": "回收产出；核对最终文本体量与任务是否相称。",
        "timed-out": "按 timeout 处置：已产生部分产出可作输入缩小范围重发一次，否则换人。",
        "cancelled": "被终止（timeout 或手动）。确认截断点后决定重发或换人。",
        "stuck": "会话建立无响应：按「受派方没起来」处置——不要重试同一 Endpoint，先探测再换候选。",
        "running": "仍在运行：等下一轮复查；若体积连续复查不涨且 pid 仍在，按 stuck 处置。",
        "truncated": "半成品：不算完成。缩小范围重发一次（同一 Endpoint 仅一次），仍失败换人。",
        "unknown": "无法判定：人工检查 run 目录。",
    }
    return {
        "run_dir": str(run_dir),
        "state": state,
        "action": actions[state],
        "pid": pid,
        "pid_alive": pid_alive,
        "events": len(events),
        "ndjson_bytes": size,
        "final_text_length": text_length,
        "stop_reason": stop_reason,
        "timed_out": timed_out,
        "endpoint": status.get("endpoint"),
        "model": status.get("model"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="acpx 委派运行状态判定（确定性指纹）")
    parser.add_argument("target", help="run-id 或 run 目录路径")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args(argv)

    target = Path(args.target)
    run_dir = target if target.is_dir() else RUNS_ROOT / args.target
    if not run_dir.is_dir():
        print(f"error: run 目录不存在: {run_dir}", file=sys.stderr)
        return 2

    report = classify(run_dir)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"state: {report['state']}")
        print(f"action: {report['action']}")
        print(f"events: {report['events']}  ndjson: {report['ndjson_bytes']}B  final_text: {report['final_text_length']}B")
        if report["stop_reason"]:
            print(f"stop_reason: {report['stop_reason']}")
        print(f"pid: {report['pid']} (alive={report['pid_alive']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
