#!/usr/bin/env python3
"""delegate.py —— 受控委派的单入口：一条命令完成 run 目录、decision.md、status.json、
timeout 兜底、acpx 启动与状态判定。不再手动拼接 acpx 命令。

用法:
  python3 delegate.py --endpoint example-host/codex --kind codex --model MiniMax-M3 \
      --cwd /path --permission read-only --timeout 600 --slug my-task \
      --reason "使用者点名 codex" -- prompt 文本
  python3 delegate.py ... --smoke        # 用标准冒烟 prompt
  python3 delegate.py ... --wait         # 前台等待至完成或超时（默认后台立即返回）
  python3 delegate.py ... --env K=V      # 给 acpx 进程注入环境变量（可重复）

结束后用 scripts/run_status.py <run-id> 判定状态。
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_status import classify, RUNS_ROOT  # noqa: E402

SMOKE_PROMPT = "reply with just: ok"


def build_acpx_cmd(args: argparse.Namespace) -> list[str]:
    perm_flag = "--approve-all" if args.permission == "write" else "--approve-reads"
    cmd = ["acpx", "--cwd", args.cwd, "--format", "json", perm_flag]
    if args.model:
        cmd += ["--model", args.model]
    cmd += [args.kind, "exec", getattr(args, "_prompt", "")]
    return cmd


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="受控委派单入口（run 目录 + timeout + 状态判定）")
    p.add_argument("--endpoint", required=True, help="Host/Kind，如 example-host/codex")
    p.add_argument("--kind", required=True, help="acpx 子命令名")
    p.add_argument("--model", default=None, help="模型 id；缺省不传 --model")
    p.add_argument("--cwd", required=True)
    p.add_argument("--permission", choices=["read-only", "write"], default="read-only")
    p.add_argument("--timeout", type=int, required=True, help="秒；超时杀整个进程组")
    p.add_argument("--slug", required=True, help="run-id 后缀")
    p.add_argument("--reason", required=True, help="为什么选它（脱离本次任务也成立的一句话）")
    p.add_argument("--evidence", default="", help="依据：读过哪些画像与 Trace")
    p.add_argument("--env", action="append", default=[], help="KEY=VAL，可重复")
    p.add_argument("--smoke", action="store_true", help="使用标准冒烟 prompt")
    p.add_argument("--wait", action="store_true", help="前台等待结束并打印判定")
    p.add_argument("--dry-run", action="store_true", help="只打印 acpx 命令不执行")
    p.add_argument("prompt_parts", nargs=argparse.REMAINDER,
                   help="-- 之后的 prompt 文本")
    args = p.parse_args(argv)

    prompt = SMOKE_PROMPT if args.smoke else " ".join(args.prompt_parts).lstrip("- ").strip()
    if not prompt:
        p.error("缺 prompt：用 --smoke 或 '-- <prompt>'")

    run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{args.slug}"
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    decision = (
        f"# decision — {run_id}\n\n"
        f"- 候选: 见 --endpoint（本 run 由调用方指定单一 Endpoint）\n"
        f"- 选择: {args.endpoint}\n"
        f"- 为什么选它: {args.reason}\n"
        f"- 依据: {args.evidence or '调用方指定的 Endpoint 画像'}\n"
        f"- 模型: {args.model or '(Endpoint 默认)'}\n"
        f"- 权限: {args.permission}\n"
        f"- 期望产出: {'冒烟：一句 ok' if args.smoke else '见 prompt'}\n"
    )
    (run_dir / "decision.md").write_text(decision, encoding="utf-8")

    args._prompt = prompt
    cmd = build_acpx_cmd(args)
    env = dict(os.environ)
    for kv in args.env:
        k, _, v = kv.partition("=")
        env[k] = v

    if args.dry_run:
        print(" ".join(cmd))
        return 0

    (run_dir / "cmd.sh").write_text(" ".join(cmd) + "\n", encoding="utf-8")

    proc = subprocess.Popen(
        cmd,
        stdout=open(run_dir / "run.ndjson", "w", encoding="utf-8"),
        stderr=open(run_dir / "stderr.log", "w", encoding="utf-8"),
        env=env,
        start_new_session=True,  # 独立进程组，超时时整组杀掉
        cwd=args.cwd,
    )
    (run_dir / "pid").write_text(str(proc.pid), encoding="utf-8")
    status = {
        "endpoint": args.endpoint,
        "kind": args.kind,
        "model": args.model,
        "pid": proc.pid,
        "started_at": time.time(),
        "timeout_seconds": args.timeout,
        "permission": args.permission,
        "smoke": args.smoke,
    }
    (run_dir / "status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2),
                                         encoding="utf-8")

    print(f"run_id: {run_id}")
    print(f"cmd: {' '.join(cmd)}")
    print(f"查看状态: python3 {Path(__file__).resolve().parent}/run_status.py {run_id}")

    if not args.wait:
        return 0

    deadline = status["started_at"] + args.timeout
    while time.time() < deadline:
        report = classify(run_dir)
        if report["state"] in ("done", "stuck", "truncated", "cancelled") \
                and not report["pid_alive"]:
            break
        if proc.poll() is not None and report["state"] in ("done", "stuck", "truncated"):
            break
        time.sleep(5)

    if proc.poll() is None and time.time() >= deadline:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            time.sleep(3)
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    report = classify(run_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["state"] == "done" else 1


if __name__ == "__main__":
    raise SystemExit(main())
