#!/usr/bin/env python3
"""Atomic task-state updates, derived indexes and conservative reconciliation.

Commands:
  task_state.py init <workspace> <task-id> --title TITLE [--criterion TEXT] [--parent PARENT-ID] [--confirm-mode MODE]
  task_state.py update <workspace> <task-path> [--status STATUS] [--current-ref REF] [--confirm-mode MODE]
                     [--execution direct|openspec] [--driver NAME] [--criterion TEXT] [--next TEXT]
  task_state.py rebuild-index <workspace>
  task_state.py reconcile <workspace> <task-path> [--repair] [--json]

<task-path> is a task id or <parent-id>/subtasks/<child-id>, relative to tasks/ongoing/.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import date
import json
import os
from pathlib import Path
import re
import sys
import tempfile

try:
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None

SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
DRIVER = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}-driver$")
STATUSES = {"pending", "active", "blocked", "done", "archived"}
REFS = {"intake", "plan", "explore", "diagnose", "grill", "design", "approve", "decompose", "execute", "review", "verify", "close"}
EXECUTIONS = {"direct", "openspec"}
CONFIRM_MODES = {"human", "goal"}


class StateError(Exception):
    pass


@contextmanager
def state_lock(workspace: Path):
    path = workspace / "tasks" / ".taskrail.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def valid_id(value: str) -> bool:
    return bool(SAFE_ID.fullmatch(value))


def split_task_path(value: str) -> tuple[str, str | None, str]:
    parts = value.strip("/").split("/")
    if len(parts) == 1 and valid_id(parts[0]):
        return parts[0], None, parts[0]
    if len(parts) == 3 and parts[1] == "subtasks" and valid_id(parts[0]) and valid_id(parts[2]):
        return parts[2], parts[0], parts[2]
    raise StateError("task path must be <task-id> or <parent-id>/subtasks/<child-id>")


def task_dir(workspace: Path, value: str) -> Path:
    _, parent, _ = split_task_path(value)
    relative = f"{parent}/subtasks/{Path(value).name}" if parent else value
    return workspace / "tasks" / "ongoing" / relative


def parse_task(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not match:
        raise StateError(f"TASK.md has no valid frontmatter: {path}")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([a-z_-]+):\s*(.*)$", line)
        if item:
            meta[item.group(1)] = item.group(2).strip().strip("\"'")
    return meta, text


def scalar(value: str | None) -> str:
    if value is None:
        return "null"
    return json.dumps(value, ensure_ascii=False)


def render(meta: dict[str, str], body: str) -> str:
    order = ["slug", "parent", "status", "current_ref", "confirm_mode", "execution", "driver", "criterion", "created", "updated"]
    ordered_keys = order + [key for key in meta if key not in order]
    lines = ["---"]
    for key in ordered_keys:
        value = meta[key]
        if key in {"slug", "parent", "status", "current_ref", "confirm_mode", "execution", "driver", "created", "updated"}:
            rendered = "null" if value in {"", "null", "None"} else value
        else:
            rendered = scalar(value)
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines) + "\n" + body


def init_task(workspace: Path, task_id: str, title: str, criterion: str, parent: str | None, confirm_mode: str | None) -> Path:
    if not valid_id(task_id):
        raise StateError("task id must be lowercase kebab-case")
    if confirm_mode is not None and confirm_mode not in CONFIRM_MODES:
        raise StateError(f"invalid confirm_mode: {confirm_mode}")
    inherited_mode = "human"
    if parent:
        if not valid_id(parent):
            raise StateError("parent id must be lowercase kebab-case")
        parent_task = workspace / "tasks" / "ongoing" / parent / "TASK.md"
        if not parent_task.is_file():
            raise StateError(f"parent task does not exist: {parent_task}")
        inherited_mode = parse_task(parent_task)[0].get("confirm_mode", "human")
        if inherited_mode not in CONFIRM_MODES:
            raise StateError(f"parent has invalid confirm_mode: {inherited_mode}")
        if confirm_mode is not None and confirm_mode != inherited_mode:
            raise StateError("child confirm_mode must inherit its parent")
    value = f"{parent}/subtasks/{task_id}" if parent else task_id
    target = task_dir(workspace, value)
    task_md = target / "TASK.md"
    if task_md.exists():
        raise StateError(f"task already exists; resume it instead: {task_md}")
    today = date.today().isoformat()
    meta = {
        "slug": task_id,
        "parent": parent or "null",
        "status": "pending" if parent else "active",
        "current_ref": "null" if parent else "plan",
        "confirm_mode": inherited_mode if parent else (confirm_mode or "human"),
        "execution": "null",
        "driver": "null",
        "criterion": criterion,
        "created": today,
        "updated": today,
    }
    body = f"""
# {title}

## 目标
{title}

## 完成判据
{criterion or "待明确；未明确前不得进入 execute。"}

## 下一动作
{"等待父任务路线图中的依赖就绪。" if parent else "评估事实并选择第一个需要的 reference。"}

## 涉及仓库
| repo_id | source_repo | worktree | branch | base |
|---|---|---|---|---|

## 产物指针
- PLAN.md
"""
    with state_lock(workspace):
        if task_md.exists():
            raise StateError(f"task already exists; resume it instead: {task_md}")
        atomic_write(task_md, render(meta, body))
        atomic_write(target / "PLAN.md", f"# 计划：{title}\n\n## 当前步骤\n- [ ] 明确当前最小实施与验证步骤。\n")
        atomic_write(target / "decisions.md", "# 决定\n\n| # | 决定 | 理由 | 状态 | 来源 |\n|---|---|---|---|---|\n")
        atomic_write(target / "history.md", "# 历史\n\n")
        (target / "context").mkdir(exist_ok=True)
        atomic_write(target / "context" / "current.md", "# 当前事实与假设\n\n")
        rebuild_index(workspace)
    return task_md


def update_task(workspace: Path, value: str, changes: dict[str, str], next_action: str | None) -> Path:
    task_md = task_dir(workspace, value) / "TASK.md"
    if not task_md.is_file():
        raise StateError(f"task does not exist: {task_md}")
    with state_lock(workspace):
        meta, text = parse_task(task_md)
        for key, item in changes.items():
            if key == "status" and item not in STATUSES:
                raise StateError(f"invalid status: {item}")
            if key == "current_ref" and item not in REFS | {"null"}:
                raise StateError(f"invalid current_ref: {item}")
            if key == "confirm_mode" and item not in CONFIRM_MODES:
                raise StateError(f"invalid confirm_mode: {item}")
            if key == "execution" and item not in EXECUTIONS | {"null"}:
                raise StateError(f"invalid execution: {item}")
            if key == "driver" and item not in {"null", "None", ""}:
                expected = f"{Path(value).name}-driver"
                if not DRIVER.fullmatch(item) or item != expected:
                    raise StateError(f"driver must be {expected!r} or null")
            meta[key] = item
        if changes.get("status") == "done":
            if not (task_md.parent / "SUMMARY.md").is_file():
                raise StateError("done requires SUMMARY.md with verification and knowledge closure")
            children = child_tasks(task_md)
            if any(parse_task(path)[0].get("status") != "done" for path in children):
                raise StateError("done parent requires every child task to be done")
        meta["updated"] = date.today().isoformat()
        body = text[re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S).end():]
        if "criterion" in changes:
            section = f"## 完成判据\n{changes['criterion'] or '待明确；未明确前不得进入 execute。'}\n\n"
            body, count = re.subn(r"^## 完成判据\n.*?(?=^## |\Z)", section, body, flags=re.S | re.M)
            if not count:
                body = body.rstrip() + "\n\n" + section
        if next_action is not None:
            section = f"## 下一动作\n{next_action}\n\n"
            body, count = re.subn(r"^## 下一动作\n.*?(?=^## |\Z)", section, body, flags=re.S | re.M)
            if not count:
                body = body.rstrip() + "\n\n" + section
        atomic_write(task_md, render(meta, body))
        rebuild_index(workspace)
    return task_md


def row_for(tasks_root: Path, path: Path, archived: bool) -> str:
    meta, _ = parse_task(path)
    relative = path.parent.relative_to(tasks_root).as_posix()
    title = path.read_text(encoding="utf-8").split("# ", 1)[1].split("\n", 1)[0] if "# " in path.read_text(encoding="utf-8") else meta.get("slug", "?")
    if archived:
        return f"| {meta.get('slug', '?')} | {meta.get('updated', '')} | {title} | {meta.get('status', '')} | {relative} |"
    return f"| {meta.get('slug', '?')} | {title} | {meta.get('updated', '')} | {meta.get('status', '')} / {meta.get('current_ref', '')} | {relative} |"


def rebuild_index(workspace: Path) -> Path:
    root = workspace / "tasks"
    ongoing = sorted((root / "ongoing").glob("**/TASK.md")) if (root / "ongoing").is_dir() else []
    archived = sorted((root / "archive").glob("**/TASK.md")) if (root / "archive").is_dir() else []
    lines = [
        "# Tasks", "", "派生索引；由 `task_state.py rebuild-index` 重建，不手改状态。", "",
        "## Ongoing", "", "| 任务 | 标题 | 更新 | 状态 / 当前环节 | 路径 |", "|---|---|---|---|---|",
    ]
    lines += [row_for(root, path, False) for path in ongoing]
    lines += ["", "## Archived", "", "| 任务 | 归档日 | 标题 | 状态 | 路径 |", "|---|---|---|---|---|"]
    lines += [row_for(root, path, True) for path in archived]
    index = root / "INDEX.md"
    atomic_write(index, "\n".join(lines) + "\n")
    return index


def child_tasks(path: Path) -> list[Path]:
    root = path.parent / "subtasks"
    return sorted(root.glob("*/TASK.md")) if root.is_dir() else []


def reconcile(workspace: Path, value: str, repair: bool) -> dict:
    task_md = task_dir(workspace, value) / "TASK.md"
    meta, _ = parse_task(task_md)
    children = child_tasks(task_md)
    child_states = {path.parent.name: parse_task(path)[0].get("status") for path in children}
    errors: list[str] = []
    recommendation: str | None = None
    if children and all(state == "done" for state in child_states.values()) and meta.get("status") not in {"done", "archived"}:
        recommendation = "verify"
    if meta.get("status") == "done":
        if not (task_md.parent / "SUMMARY.md").is_file():
            errors.append("done requires SUMMARY.md")
        if any(state != "done" for state in child_states.values()):
            errors.append("done parent requires every child task to be done")
        if errors:
            recommendation = "close"
    result = {
        "ok": not errors,
        "task": str(task_md),
        "status": meta.get("status"),
        "current_ref": meta.get("current_ref"),
        "children": child_states,
        "recommended_ref": recommendation,
        "errors": errors,
        "repaired": False,
    }
    if repair and recommendation:
        changes = {"current_ref": recommendation}
        if errors:
            changes["status"] = "active"
        update_task(workspace, value, changes, "按恢复校核重新路由。")
        result["repaired"] = True
        result["ok"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("workspace")
    init.add_argument("task_id")
    init.add_argument("--title", required=True)
    init.add_argument("--criterion", default="")
    init.add_argument("--parent")
    init.add_argument("--confirm-mode", choices=sorted(CONFIRM_MODES))
    update = sub.add_parser("update")
    update.add_argument("workspace")
    update.add_argument("task_path")
    update.add_argument("--status")
    update.add_argument("--current-ref")
    update.add_argument("--confirm-mode")
    update.add_argument("--execution")
    update.add_argument("--driver")
    update.add_argument("--criterion")
    update.add_argument("--next")
    rebuild = sub.add_parser("rebuild-index")
    rebuild.add_argument("workspace")
    rec = sub.add_parser("reconcile")
    rec.add_argument("workspace")
    rec.add_argument("task_path")
    rec.add_argument("--repair", action="store_true")
    rec.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        workspace = Path(args.workspace).expanduser().resolve()
        if args.command == "init":
            result = {"ok": True, "task": str(init_task(workspace, args.task_id, args.title, args.criterion, args.parent, args.confirm_mode))}
        elif args.command == "update":
            keys = ("status", "current-ref", "confirm-mode", "execution", "driver", "criterion")
            changes = {key.replace("-", "_"): value for key in keys if (value := getattr(args, key.replace("-", "_"))) is not None}
            result = {"ok": True, "task": str(update_task(workspace, args.task_path, changes, args.next))}
        elif args.command == "rebuild-index":
            with state_lock(workspace):
                result = {"ok": True, "index": str(rebuild_index(workspace))}
        else:
            result = reconcile(workspace, args.task_path, args.repair)
    except (StateError, OSError, json.JSONDecodeError) as exc:
        result = {"ok": False, "error": str(exc)}
        code = 1
    else:
        code = 0 if result.get("ok") else 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
