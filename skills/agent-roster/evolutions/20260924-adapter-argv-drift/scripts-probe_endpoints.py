#!/usr/bin/env python3
"""探测本机有哪些 agent Endpoint 可用。

L1 只看 CLI 在不在 PATH、什么版本；L2 额外拉起 ACP 适配器走一次 initialize 握手。
L3（真发 prompt 确认登录态与额度）要花钱，由人手动做，本脚本不涉及。

输出 JSON；加 --render 则输出可粘贴进 Endpoint 台账的 Markdown 状态块。
加 --write 则按台账 schema 直接回填「探测状态」段（只动机器段，只留最近 2 条，
任务倾向/备注不碰）——schema 已冻结，写回是确定性的。
"""

from __future__ import annotations

import argparse
import json
import queue
import shutil
import socket
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _roster import agents_dir  # noqa: E402

# kind -> CLI 命令、取版本的参数、拉起 ACP 适配器的命令。
# cli 可以是候选名列表：上游改过名的 CLI，新旧名可能并存或只剩其一，取第一个在 PATH 里的。
AGENT_KINDS: dict[str, dict[str, object]] = {
    "claude": {
        "cli": "claude",
        "version": ["--version"],
        "acp": ["npx", "-y", "@agentclientprotocol/claude-agent-acp"],
    },
    "codex": {
        "cli": "codex",
        "version": ["--version"],
        "acp": ["npx", "-y", "@agentclientprotocol/codex-acp"],
    },
    "gemini": {"cli": "gemini", "version": ["--version"], "acp": ["gemini", "--acp"]},
    "cursor": {
        "cli": "cursor-agent",
        "version": ["--version"],
        "acp": ["cursor-agent", "acp"],
    },
    "opencode": {
        "cli": "opencode",
        "version": ["--version"],
        "acp": ["npx", "-y", "opencode-ai", "acp"],
    },
    "qwen": {"cli": "qwen", "version": ["--version"], "acp": ["qwen", "--acp"]},
    "kiro": {
        "cli": "kiro-cli-chat",
        "version": ["--version"],
        "acp": ["kiro-cli-chat", "acp"],
    },
    "copilot": {
        "cli": "copilot",
        "version": ["--version"],
        "acp": ["copilot", "--acp", "--stdio"],
    },
    "pi": {"cli": "pi", "version": ["--version"], "acp": ["npx", "pi-acp"]},
    # 该 CLI 有改名史：qodercli / qoderclicn → qodercn。acpx 内置 kind argv 仍指旧名，
    # 所以本表记的是**当前正确名**，acpx 那份滞后由 acpx_kind_argv() 比对并报 argv_gap。
    "qoder": {
        "cli": ["qodercn", "qodercli", "qoderclicn"],
        "version": ["--version"],
        "acp": ["qodercn", "--acp"],
    },
}

# 包运行器：这些出现在 argv[0] 时，真正的适配器包名在后面的元素里，不比对二进制名
RUNNER_BINS = {"npx", "pnpx", "bunx", "deno", "node", "uvx", "uv"}

INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": 1,
        "clientCapabilities": {"fs": {"readTextFile": False, "writeTextFile": False}},
    },
}


def _npm_global_root() -> Path | None:
    try:
        done = subprocess.run(
            ["npm", "root", "-g"], capture_output=True, text=True, timeout=20
        )
    except (subprocess.SubprocessError, OSError):
        return None
    out = done.stdout.strip()
    return Path(out) if done.returncode == 0 and out else None


_ACPX_ROOT_CACHE: Path | None = None


def acpx_kind_argv(kind: str) -> list[str] | None:
    """读 acpx 内置 registry 里该 kind 实际要 spawn 的 argv；读不到返回 None（不猜）。

    acpx 把 kind→命令写死在自己的 dist 里，CLI 上游改名后这份 argv 滞后于本机现实，
    于是「CLI 装了、适配器握手也通，acpx 却 spawn 不到」。npm root -g 是唯一不依赖
    具体安装器路径的定位方式。
    """
    import re

    global _ACPX_ROOT_CACHE
    if _ACPX_ROOT_CACHE is None:
        _ACPX_ROOT_CACHE = _npm_global_root() or Path("/nonexistent")
    pkg = _ACPX_ROOT_CACHE / "acpx" / "dist"
    if not pkg.is_dir():
        return None
    try:
        text = "\n".join(
            f.read_text(encoding="utf-8", errors="replace")
            for f in sorted(pkg.glob("agent-registry-*.js"))
        )
    except OSError:
        return None
    # dist 里的键可能不带引号（实测形态：qoder: {\n name: "Qoder",\n argv: ["qodercli", "--acp"]）
    m = re.search(
        rf'["\']?{re.escape(kind)}["\']?\s*:\s*\{{[^}}]*?'
        rf'["\']?argv["\']?\s*:\s*\[([^\]]*)\]',
        text,
        re.S,
    )
    if m:
        return [t.strip().strip('"\'') for t in m.group(1).split(",") if t.strip()]
    m = re.search(
        rf'["\']?{re.escape(kind)}["\']?\s*:\s*\{{[^}}]*?'
        rf'["\']?command["\']?\s*:\s*(["\'][^"\']*["\'])',
        text,
        re.S,
    )
    if m:
        return m.group(1).strip('"\'').split()
    return None


def _resolve_cli(cli: object) -> tuple[str | None, str | None]:
    """cli 允许是候选名列表：有改名史的 CLI 新旧名可能并存，取第一个在 PATH 里的。"""
    for name in ([cli] if isinstance(cli, str) else list(cli)):
        path = shutil.which(str(name))
        if path:
            return str(name), path
    return None, None


def probe_l1(kind: str, spec: dict) -> dict:
    """CLI 在不在 PATH、版本多少，并核对 acpx 真会去 spawn 的那个二进制在不在。

    两者可以指向不同文件：本表的 acp 记的是**当前正确名**，acpx registry 里可能还是旧名。
    argv_gap 就是这条警告——没有它，会出现 L1 ✅ + L2 ✅ 而委派仍以 command-not-found 失败。
    """
    name, path = _resolve_cli(spec["cli"])
    adapter_bin = str(list(spec["acp"])[0])
    result: dict = {"cli_name": name, "adapter_bin": adapter_bin}

    acpx_argv = acpx_kind_argv(kind)
    result["acpx_argv"] = acpx_argv
    if acpx_argv and name:
        # CLI 装了才谈漂移；CLI 本来就没装（argv[0] 与 CLI 名同样缺失）不是 gap，别误报成可覆盖
        spawn_bin = acpx_argv[0]
        if spawn_bin not in RUNNER_BINS and shutil.which(spawn_bin) is None:
            result["argv_gap"] = (
                f"acpx 内置 argv 指向 {spawn_bin}，本机不在 PATH；CLI 实际是 {name}"
                f" → 走 acpx config agents.{kind}.argv 覆盖，或 delegate.py --agent"
            )
        elif spawn_bin not in RUNNER_BINS and spawn_bin != adapter_bin:
            result["argv_gap"] = (
                f"acpx argv[0]={spawn_bin} 与本表 acp[0]={adapter_bin} 不一致"
            )

    if not path:
        return {"l1": "missing", "path": None, "version": None, **result}

    version = None
    try:
        done = subprocess.run(
            [path, *spec["version"]],
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = (done.stdout or done.stderr).strip()
        version = output.splitlines()[0].strip() if output else None
    except (subprocess.SubprocessError, OSError) as exc:
        # 版本取不到不影响「装了」这个结论，记下原因即可
        version = f"<unavailable: {type(exc).__name__}>"

    return {"l1": "ok", "path": path, "version": version, **result}


def probe_l2(spec: dict, timeout: float) -> dict:
    """拉起 ACP 适配器，走一次 initialize 握手，确认它真的说 ACP。"""
    command = list(spec["acp"])
    if not shutil.which(command[0]):
        return {"l2": "skipped", "detail": f"{command[0]} 不在 PATH"}

    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
    except OSError as exc:
        return {"l2": "failed", "detail": f"启动失败: {exc}"}

    lines: queue.Queue[str] = queue.Queue()

    def pump() -> None:
        assert proc.stdout is not None
        for line in proc.stdout:
            lines.put(line)

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()

    try:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(INITIALIZE) + "\n")
        proc.stdin.flush()

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=0.2)
            except queue.Empty:
                if proc.poll() is not None:
                    return {"l2": "failed", "detail": "适配器在握手完成前退出"}
                continue

            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                # 适配器在协议流里混了非 JSON 输出，忽略继续等
                continue

            if message.get("id") != 1:
                continue
            if "error" in message:
                return {"l2": "failed", "detail": f"initialize 报错: {message['error']}"}
            result = message.get("result") or {}
            return {
                "l2": "ok",
                "protocol_version": result.get("protocolVersion"),
                "auth_methods": [
                    m.get("id") for m in result.get("authMethods", []) if isinstance(m, dict)
                ],
            }

        return {"l2": "timeout", "detail": f"{timeout:.0f}s 内没有收到 initialize 响应"}
    except OSError as exc:
        return {"l2": "failed", "detail": f"通信失败: {exc}"}
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


def render_markdown(host: str, results: list[dict]) -> str:
    """输出可粘贴进 Endpoint 台账「探测状态」段的 Markdown。"""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    blocks = []
    for item in results:
        if item["l1"] == "missing":
            state = "L1 ❌ 未安装"
        elif "l2" not in item:
            state = f"L1 ✅ {item.get('version') or '版本未知'}"
        elif item["l2"] == "ok":
            state = f"L1 ✅ {item.get('version') or '版本未知'} —— L2 ✅ ACP 握手通过"
        elif item["l2"] == "skipped":
            state = f"L1 ✅ {item.get('version') or '版本未知'} —— L2 ⏭ {item.get('detail', '')}"
        else:
            state = (
                f"L1 ✅ {item.get('version') or '版本未知'} "
                f"—— L2 ❌ {item['l2']}: {item.get('detail', '')}"
            )
        if item.get("argv_gap"):
            # 装了、握手也通，但 acpx 根本 spawn 不到 —— 不写出来就会被当成「可用」
            state += f" —— ⚠ {item['argv_gap']}"
        blocks.append(f"### {host}/{item['kind']}\n\n- {stamp} —— {state}")
    return "\n\n".join(blocks)


def status_bullets(results: list[dict]) -> dict[str, str]:
    """kind -> 「探测状态」段的单行 bullet。"""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = {}
    for item in results:
        if item["l1"] == "missing":
            state = "L1 ❌ 未安装"
        elif "l2" not in item:
            state = f"L1 ✅ {item.get('version') or '版本未知'}"
        elif item["l2"] == "ok":
            state = f"L1 ✅ {item.get('version') or '版本未知'} —— L2 ✅ ACP 握手通过"
        else:
            state = f"L1 ✅ {item.get('version') or '版本未知'} —— L2 ❌ {item['l2']}: {item.get('detail', '')}"
        if item.get("argv_gap"):
            state += f" —— ⚠ {item['argv_gap']}"
        out[item["kind"]] = f"- {stamp} —— {state}"
    return out


SECTION_RE = __import__("re").compile(r"(^##\s+探测状态.*?$)", __import__("re").M)


def backfill(host: str, results: list[dict], keep: int = 2) -> list[str]:
    """把探测结果写回各画像的「探测状态」段；返回改动文件列表。
L3 记录（冒烟门禁依据）永不被挤掉，其余行只留最近 keep-1 条。"""
    import re
    bullets = status_bullets(results)
    changed = []
    for kind, bullet in bullets.items():
        path = agents_dir() / host / f"{kind}.md"
        if not path.exists():
            print(f"warn: {path} 不存在，跳过（先登记画像）", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^##\s+探测状态.*?$", text, re.M)
        if not m:
            print(f"warn: {path} 没有「探测状态」段，跳过", file=sys.stderr)
            continue
        rest = text[m.end():]
        nxt = re.search(r"^##\s+", rest, re.M)
        sec = rest[: nxt.start()] if nxt else rest
        old = [ln for ln in sec.splitlines() if ln.strip().startswith("- ")]
        # L3 记录是冒烟门禁的依据，永不被新探测挤掉；其余行保留最近 keep-1 条
        l3 = [ln for ln in old if "L3" in ln]
        non_l3 = [ln for ln in old if "L3" not in ln]
        lines = [bullet] + non_l3[: keep - 1] + l3
        new_sec = "\n" + "\n".join(lines) + "\n"
        text = text[: m.end()] + new_sec + (rest[nxt.start():] if nxt else "")
        path.write_text(text, encoding="utf-8")
        changed.append(str(path))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--level", type=int, choices=(1, 2), default=1, help="探测深度，默认 1")
    parser.add_argument("--kind", action="append", help="只探测指定 Agent Kind，可重复")
    parser.add_argument("--host", default=None, help="Host 名，建议填 ssh 别名；默认取 hostname")
    parser.add_argument("--timeout", type=float, default=60.0, help="L2 握手超时秒数，默认 60")
    parser.add_argument("--render", action="store_true", help="输出 Markdown 而非 JSON")
    parser.add_argument("--write", action="store_true",
                        help="把结果按 schema 直接回填画像「探测状态」段（需先配置 data_root）")
    args = parser.parse_args()

    kinds = args.kind or list(AGENT_KINDS)
    unknown = [k for k in kinds if k not in AGENT_KINDS]
    if unknown:
        print(f"未知的 Agent Kind: {', '.join(unknown)}", file=sys.stderr)
        return 2

    host = args.host or socket.gethostname()
    results = []
    for kind in kinds:
        spec = AGENT_KINDS[kind]
        item = {"kind": kind, **probe_l1(kind, spec)}
        if args.level >= 2 and item["l1"] == "ok":
            item.update(probe_l2(spec, args.timeout))
        results.append(item)

    if args.write:
        for path in backfill(host, results):
            print(f"backfilled: {path}")

    if args.render:
        print(render_markdown(host, results))
    else:
        print(json.dumps({"host": host, "probed_at": datetime.now().isoformat(timespec="seconds"), "level": args.level, "endpoints": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
