#!/usr/bin/env python3
"""resolve_role.py <role-id> —— 把点名的 Role 解成默认 Endpoint。

对照表 <data_root>/agents/roles.yaml，一行 `<role-id>: <host>/<kind>`。
右侧空、没有这个 id、或文件不存在，都是 unbound。

verdict use（exit 0）：有 Endpoint，画像文件在，最近一条探测状态不含 ❌ 或 ⚠。
verdict ask（exit 1）：reason=unbound|missing|down。这是正常结果，不是故障。
exit 2：参数、对照表或名册目录本身坏了。

--write <role-id> <host>/<kind>：写入对照表。画像文件必须已在名册。
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ROLE_RE = re.compile(r"^[a-z][a-z0-9-]*$")
ENDPOINT_RE = re.compile(r"^[^/\s]+/[^/\s]+$")
ROLE_LINE_RE = re.compile(r"^([a-z][a-z0-9-]*)\s*:\s*(\S*)\s*$")


def section(text: str, header_prefix: str) -> str:
    m = re.search(rf"^##\s+{re.escape(header_prefix)}.*?$", text, re.M)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def load_roles(text: str) -> dict[str, str]:
    roles: dict[str, str] = {}
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = ROLE_LINE_RE.match(line)
        if not m:
            raise ValueError(f"roles.yaml:{i} 无法识别: {raw}")
        endpoint = m.group(2)
        if endpoint and not ENDPOINT_RE.match(endpoint):
            raise ValueError(f"roles.yaml:{i} Endpoint 须为 host/kind")
        roles[m.group(1)] = endpoint
    return roles


def upsert(text: str, role: str, endpoint: str) -> str:
    out: list[str] = []
    found = False
    pat = re.compile(rf"^{re.escape(role)}\s*:")
    for raw in text.splitlines():
        if pat.match(raw.strip()):
            out.append(f"{role}: {endpoint}")
            found = True
        else:
            out.append(raw)
    if not found:
        out.append(f"{role}: {endpoint}")
    body = "\n".join(out)
    if not body.endswith("\n"):
        body += "\n"
    return body


def probe_failed(text: str) -> bool:
    bullets = [ln.strip() for ln in section(text, "探测状态").splitlines() if ln.strip().startswith("-")]
    if not bullets:
        return False
    last = bullets[-1]
    return "❌" in last or "⚠" in last


def decide(binding: str | None, profile_exists: bool, profile_text: str) -> tuple[str, str | None]:
    """返回 (verdict, reason)。use 时 reason 为 None。"""
    if not binding:
        return "ask", "unbound"
    if not profile_exists:
        return "ask", "missing"
    if probe_failed(profile_text):
        return "ask", "down"
    return "use", None


def emit(verdict: str, role: str, reason: str | None, endpoint: str | None) -> None:
    print(f"verdict: {verdict}")
    if reason:
        print(f"reason: {reason}")
    print(f"role: {role}")
    if endpoint:
        print(f"endpoint: {endpoint}")


def run(argv: list[str], agents: Path) -> int:
    p = argparse.ArgumentParser(description="把点名的 Role 解成默认 Endpoint")
    p.add_argument("role", nargs="?", help="role id")
    p.add_argument("endpoint", nargs="?", help="仅与 --write 合用：host/kind")
    p.add_argument("--write", action="store_true", help="写入对照表；调用前须已得到使用者明确同意")
    args = p.parse_args(argv)

    if not args.role or not ROLE_RE.match(args.role):
        print("error: role id 须为小写字母开头，其余为小写字母、数字或连字符", file=sys.stderr)
        return 2
    if not agents.is_dir():
        print(f"error: 名册目录不存在: {agents}", file=sys.stderr)
        return 2

    path = agents / "roles.yaml"
    try:
        roles = load_roles(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.write:
        if not args.endpoint or not ENDPOINT_RE.match(args.endpoint):
            print("error: --write 需要 host/kind", file=sys.stderr)
            return 2
        host, kind = args.endpoint.split("/", 1)
        profile = agents / host / f"{kind}.md"
        if not profile.is_file():
            print(f"error: 名册里没有 {args.endpoint}", file=sys.stderr)
            return 2
        existing = path.read_text(encoding="utf-8") if path.is_file() else ""
        path.write_text(upsert(existing, args.role, args.endpoint), encoding="utf-8")
        print(f"wrote: {args.role}: {args.endpoint}")
        return 0

    if args.endpoint:
        print("error: 解析时不要带 Endpoint；写入请加 --write", file=sys.stderr)
        return 2

    binding = roles.get(args.role, "")
    endpoint = binding or None
    profile_text = ""
    profile_exists = False
    if binding:
        host, kind = binding.split("/", 1)
        profile = agents / host / f"{kind}.md"
        profile_exists = profile.is_file()
        if profile_exists:
            profile_text = profile.read_text(encoding="utf-8")
    verdict, reason = decide(binding or None, profile_exists, profile_text)
    shown = endpoint if verdict != "ask" or reason != "unbound" else None
    emit(verdict, args.role, reason, shown if verdict == "ask" or verdict == "use" else None)
    if verdict == "use":
        return 0
    return 1


def _profile(body: str) -> str:
    return f"# example-host/codex\n\n## 探测状态\n\n{body}\n"


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        agents = Path(tmp)
        codex = agents / "example-host"
        codex.mkdir()
        ok = codex / "codex.md"
        ok.write_text(_profile("- 2026-01-01 00:00 —— L1 ✅ x —— L2 ✅ ACP 握手通过"), encoding="utf-8")
        down = codex / "down.md"
        down.write_text(
            _profile(
                "- 2026-01-01 00:00 —— L1 ✅ x —— L2 ✅ ACP 握手通过\n"
                "- 2026-01-02 00:00 —— L1 ✅ x —— L2 ❌ failed: nope"
            ),
            encoding="utf-8",
        )
        warned = codex / "warned.md"
        warned.write_text(
            _profile("- 2026-01-01 00:00 —— L1 ✅ x —— L2 ✅ ACP 握手通过 —— ⚠ argv gap"),
            encoding="utf-8",
        )
        skipped = codex / "skipped.md"
        skipped.write_text(_profile("- 2026-01-01 00:00 —— L1 ✅ x —— L2 ⏭ 未测"), encoding="utf-8")

        text = "# comment\ndeveloper: example-host/codex\nreviewer:\nplanner: example-host/down\ncode-reviewer: example-host/warned\ndesigner: example-host/skipped\n"
        roles = load_roles(text)
        assert roles["developer"] == "example-host/codex"
        assert roles["reviewer"] == ""
        assert decide(roles["developer"], True, ok.read_text(encoding="utf-8")) == ("use", None)
        assert decide("", True, "") == ("ask", "unbound")
        assert decide(None, True, "") == ("ask", "unbound")
        assert decide("example-host/missing", False, "") == ("ask", "missing")
        assert decide("example-host/down", True, down.read_text(encoding="utf-8")) == ("ask", "down")
        assert decide("example-host/warned", True, warned.read_text(encoding="utf-8")) == ("ask", "down")
        assert decide("example-host/skipped", True, skipped.read_text(encoding="utf-8")) == ("use", None)
        assert upsert("# keep\nreviewer:\n", "reviewer", "example-host/codex") == "# keep\nreviewer: example-host/codex\n"
        assert upsert("", "developer", "example-host/codex") == "developer: example-host/codex\n"

        assert run(["reviewer"], agents) == 1
        assert run(["--write", "developer", "example-host/codex"], agents) == 0
        assert run(["developer"], agents) == 0
        assert run(["--write", "developer", "example-host/nope"], agents) == 2
        assert run(["--write", "planner", "example-host/down"], agents) == 0
        assert run(["planner"], agents) == 1
        assert run(["NotARole"], agents) == 2
        written = (agents / "roles.yaml").read_text(encoding="utf-8")
        assert "developer: example-host/codex" in written
        assert "planner: example-host/down" in written


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--self-check" in argv:
        self_check()
        print("self-check: ok")
        return 0
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _roster import agents_dir  # noqa: E402

    return run(argv, agents_dir())


if __name__ == "__main__":
    sys.exit(main())
