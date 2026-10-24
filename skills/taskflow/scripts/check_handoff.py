#!/usr/bin/env python3
"""OpenSpec-only handoff gate; direct execution never uses this script.

Usage: check_handoff.py <workspace-root> <task-path> [--json]
New tasks require status=active, execution=openspec and an execute/review/verify/close
current_ref. Legacy handed-off/phase tasks remain readable for migration.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_PHASES = ("propose", "apply", "archive", "done")
ALLOWED_REFS = ("execute", "review", "verify", "close")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
REDIRECT = "拒绝建 driver：回 taskrail 补齐 OpenSpec handoff；approve 只在路由要求时执行。"


def valid_task_path(value: str) -> bool:
    parts = value.split("/")
    return ((len(parts) == 1 and SAFE_ID.fullmatch(parts[0]) is not None) or
            (len(parts) == 3 and parts[1] == "subtasks" and
             SAFE_ID.fullmatch(parts[0]) is not None and SAFE_ID.fullmatch(parts[2]) is not None))


def parse_meta(text: str) -> dict[str, str]:
    block = None
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if match:
        block = match.group(1)
    else:
        match = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.S)
        block = match.group(1) if match else text
    meta: dict[str, str] = {}
    for line in block.splitlines():
        item = re.match(r"^[-*]?\s*([a-z_]+)\s*:\s*(.*?)\s*$", line)
        if item and item.group(1) not in meta:
            meta[item.group(1)] = item.group(2).strip().strip("\"'")
    return meta


def section(text: str, title: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(title)}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return match.group(1) if match else None


def field(body: str, name: str) -> str | None:
    match = re.search(rf"^\s*[-*]?\s*{re.escape(name)}\s*[:：]\s*(.*?)\s*$", body, re.M)
    return match.group(1).strip() or None if match else None


def check(root: Path, slug: str) -> dict:
    ongoing = root / "tasks" / "ongoing"
    task_md = ongoing / slug / "TASK.md"
    res: dict = {"task_md": str(task_md), "slug": slug, "errors": [], "warnings": [], "bypass": None}
    if not valid_task_path(slug):
        res["errors"].append("task path 须为 <task-id> 或 <parent>/subtasks/<child>")
        return res
    try:
        task_md.resolve().relative_to(ongoing.resolve())
    except ValueError:
        res["errors"].append("task path 不能离开 workspace tasks/ongoing")
        return res
    if not task_md.is_file():
        res["errors"].append(f"TASK.md 不存在：{task_md}")
        return res
    text = task_md.read_text(encoding="utf-8")
    meta = parse_meta(text)
    res.update(status=meta.get("status"), phase=meta.get("phase"), current_ref=meta.get("current_ref"), execution=meta.get("execution"))

    bypass = meta.get("gate_bypass", "")
    if bypass and bypass.lower() not in ("null", "none", "~"):
        if "user-confirmed" in bypass and len(bypass.replace("user-confirmed", "").strip(" :：-")) >= 4:
            res["bypass"] = bypass
            res["warnings"].append("BYPASS：用户原话确认豁免；未核对项必须在 decisions / SUMMARY 中按实际降级记录。")
            return res
        res["errors"].append("gate_bypass 须含 user-confirmed 与用户原话。")

    body = section(text, "交接")
    if body is None:
        res["errors"].append("缺「## 交接」节（OpenSpec handoff 载荷）")
        return res

    legacy = meta.get("status") == "handed-off"
    if legacy:
        if meta.get("phase") not in ALLOWED_PHASES:
            res["errors"].append(f"legacy phase 须为 {'/'.join(ALLOWED_PHASES)}，实为 {meta.get('phase')!r}")
    else:
        if meta.get("status") != "active":
            res["errors"].append(f"status 须为 active，实为 {meta.get('status')!r}")
        if meta.get("execution") != "openspec":
            res["errors"].append("execution 须为 openspec；direct 不走本入口门")
        if meta.get("current_ref") not in ALLOWED_REFS:
            res["errors"].append(f"current_ref 须为 {'/'.join(ALLOWED_REFS)}，实为 {meta.get('current_ref')!r}")

    if not meta.get("criterion"):
        res["errors"].append("元信息缺 criterion（完成判据原文）")
    want_driver = f"{slug.rstrip('/').rsplit('/', 1)[-1]}-driver"
    if meta.get("driver") != want_driver:
        res["errors"].append(f"driver 须为 {want_driver!r}，实为 {meta.get('driver')!r}")

    approved = (task_md.parent / "reviews" / "APPROVED.md").is_file() or (task_md.parent / "approve" / "APPROVED.md").is_file()
    approval = field(body, "批准") or ""
    not_required = approval.startswith("not-required:") and len(approval.removeprefix("not-required:").strip()) > 0
    if not approved and not not_required:
        res["errors"].append("缺 reviews/APPROVED.md 或 approve/APPROVED.md；router 判定无需 approve 时须在交接节写 `批准：not-required: <理由>`")

    cls = field(body, "交付类别")
    packs = field(body, "适用门包")
    res["delivery_class"], res["gate_packs"] = cls, packs
    if not cls:
        res["errors"].append("交接载荷缺「交付类别」（无交付产出写「不适用」）")
    if not packs:
        res["errors"].append("交接载荷缺「适用门包」（不适用写「无」）")
    if cls and re.search(r"web\s*-?\s*ui", cls, re.I):
        for name in ("Active Instance 根路径", "contract digest", "binding digest", "projection digest"):
            if not field(body, name):
                res["errors"].append(f"Web UI 交接载荷缺「{name}」")
    return res


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace_root")
    parser.add_argument("slug", help="task id or <parent>/subtasks/<child>")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.workspace_root)
    if not root.is_dir():
        print(f"USAGE: workspace_root 不是目录：{root}", file=sys.stderr)
        return 2
    result = check(root, args.slug)
    ok = not result["errors"]
    result["ok"] = ok
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for warning in result["warnings"]:
            print(f"WARN  {warning}")
        for error in result["errors"]:
            print(f"FAIL  {error}")
        print("PASS  OpenSpec handoff 成立" if ok else f"BLOCK  {REDIRECT}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
