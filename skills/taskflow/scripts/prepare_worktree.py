#!/usr/bin/env python3
"""Prepare or resume one task worktree without touching the source checkout.

Usage: prepare_worktree.py <workspace> <task-id|parent/subtasks/child|parent/integration> <repo-id> <source-repo> [--base REF] [--integrate REF ...] [--json]
Only Python's standard library and the git CLI are required.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None

SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")


class WorktreeError(Exception):
    def __init__(self, message: str, code: int = 1, extra: dict | None = None):
        super().__init__(message)
        self.code = code
        self.extra = extra or {}


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if check and proc.returncode:
        raise WorktreeError(proc.stderr.strip() or proc.stdout.strip() or "git command failed")
    return proc


def git_out(repo: Path, *args: str) -> str:
    return run_git(repo, *args).stdout.strip()


def canonical(path: Path) -> Path:
    return path.expanduser().resolve()


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def workspace_lock(workspace: Path):
    lock_path = workspace / "worktrees" / ".taskrail.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def registry_path(workspace: Path, task_id: str) -> Path:
    return workspace / "worktrees" / task_id / "registry.json"


def load_registry(path: Path, task_id: str) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"version": 1, "task_id": task_id, "repos": {}}


def validate_id(value: str, label: str) -> None:
    if not SAFE_ID.fullmatch(value):
        raise WorktreeError(f"{label} must be lowercase kebab-case (1-80 chars): {value!r}", 2)


def parse_task_ref(value: str) -> tuple[str, str]:
    cleaned = value.strip("/")
    parts = cleaned.split("/")
    if len(parts) == 1 and SAFE_ID.fullmatch(parts[0]):
        return parts[0], parts[0]
    if len(parts) == 2 and parts[1] == "integration" and SAFE_ID.fullmatch(parts[0]):
        return f"{parts[0]}--integration", cleaned
    if len(parts) == 3 and parts[1] == "subtasks" and SAFE_ID.fullmatch(parts[0]) and SAFE_ID.fullmatch(parts[2]):
        return f"{parts[0]}--{parts[2]}", cleaned
    raise WorktreeError(
        f"task-id must be lowercase kebab-case, <parent>/subtasks/<child>, or <parent>/integration: {value!r}",
        2,
    )


def source_root(source: Path) -> Path:
    if not source.is_dir():
        raise WorktreeError(f"source repository does not exist: {source}", 2)
    return canonical(Path(git_out(source, "rev-parse", "--show-toplevel")))


def common_dir(repo: Path) -> Path:
    value = git_out(repo, "rev-parse", "--git-common-dir")
    return canonical((repo / value) if not os.path.isabs(value) else Path(value))


def default_base(source: Path) -> str:
    head = run_git(source, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD", check=False)
    if head.returncode == 0 and head.stdout.strip():
        candidate = head.stdout.strip()
        if run_git(source, "rev-parse", "--verify", candidate + "^{commit}", check=False).returncode == 0:
            return candidate
    return "HEAD"


def ensure_exclude(source: Path, worktree: Path) -> None:
    try:
        relative = worktree.relative_to(source)
    except ValueError:
        return
    if not relative.parts:
        return
    exclude_value = relative.parts[0] + "/"
    exclude_path = Path(git_out(source, "rev-parse", "--git-path", "info/exclude"))
    if not exclude_path.is_absolute():
        exclude_path = source / exclude_path
    exclude_path.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.is_file() else ""
    lines = existing.splitlines()
    if exclude_value not in lines:
        with exclude_path.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(exclude_value + "\n")


def merge_identity_args(repo: Path) -> list[str]:
    args: list[str] = []
    if not run_git(repo, "config", "user.name", check=False).stdout.strip():
        args += ["-c", "user.name=taskflow"]
    if not run_git(repo, "config", "user.email", check=False).stdout.strip():
        args += ["-c", "user.email=taskflow@example.invalid"]
    return args


def integrate_branches(target: Path, refs: list[str]) -> bool:
    merged_any = False
    identity = merge_identity_args(target)
    for ref in refs:
        if run_git(target, "merge-base", "--is-ancestor", ref, "HEAD", check=False).returncode == 0:
            continue
        proc = run_git(target, *identity, "merge", "--no-ff", "--no-edit", ref, check=False)
        if proc.returncode != 0:
            conflicts = [
                line.strip()
                for line in run_git(target, "diff", "--name-only", "--diff-filter=U", check=False).stdout.splitlines()
                if line.strip()
            ]
            run_git(target, "merge", "--abort", check=False)
            detail = proc.stderr.strip() or proc.stdout.strip() or "merge conflict"
            raise WorktreeError(
                f"integration merge conflict on {ref}: {detail}",
                5,
                extra={"conflict_branch": ref, "conflict_files": conflicts},
            )
        merged_any = True
    return merged_any


def prepare(
    workspace: Path,
    task_id: str,
    repo_id: str,
    source: Path,
    base: str | None,
    integrate: list[str] | None = None,
) -> dict:
    worktree_key, task_path = parse_task_ref(task_id)
    validate_id(repo_id, "repo-id")
    integrate_refs = [ref for ref in (integrate or []) if ref]
    workspace.mkdir(parents=True, exist_ok=True)
    workspace = canonical(workspace)
    source = source_root(canonical((workspace / source) if not source.is_absolute() else source))
    for ref in integrate_refs:
        if run_git(source, "rev-parse", "--verify", ref + "^{commit}", check=False).returncode != 0:
            raise WorktreeError(f"integrate ref is not a valid commit: {ref}", 2)
    target = workspace / "worktrees" / worktree_key / repo_id
    branch = f"task/{worktree_key}"
    base = base or default_base(source)
    reg_path = registry_path(workspace, worktree_key)

    with workspace_lock(workspace):
        registry = load_registry(reg_path, worktree_key)
        if task_path != worktree_key:
            registry["task_path"] = task_path
        previous = registry.get("repos", {}).get(repo_id)
        if previous and canonical(Path(previous["source_repo"])) != source:
            raise WorktreeError(f"repo id {repo_id!r} is already bound to another source repository", 4)

        if target.exists():
            if not target.is_dir():
                raise WorktreeError(f"worktree target is not a directory: {target}", 4)
            actual_root = canonical(Path(git_out(target, "rev-parse", "--show-toplevel")))
            if actual_root != canonical(target):
                raise WorktreeError(f"target is not a git worktree root: {target}", 4)
            if common_dir(target) != common_dir(source):
                raise WorktreeError(f"worktree belongs to another repository: {target}", 4)
            if git_out(target, "branch", "--show-current") != branch:
                raise WorktreeError(f"worktree branch mismatch at {target}; expected {branch}", 4)
            if git_out(target, "status", "--porcelain"):
                raise WorktreeError(f"worktree has uncommitted changes; preserve and inspect it first: {target}", 3)
            action = "resumed"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            branch_exists = run_git(source, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False).returncode == 0
            if branch_exists:
                if not previous:
                    raise WorktreeError(f"branch {branch} already exists without a matching task registry entry", 4)
                run_git(source, "worktree", "add", str(target), branch)
                action = "reattached"
            else:
                if run_git(source, "rev-parse", "--verify", base + "^{commit}", check=False).returncode != 0:
                    raise WorktreeError(f"base is not a valid commit: {base}", 2)
                run_git(source, "worktree", "add", str(target), "-b", branch, base)
                action = "created"
        ensure_exclude(source, target)
        if integrate_refs and integrate_branches(target, integrate_refs):
            action = "integrated"
        record = {
            "source_repo": str(source),
            "worktree": str(target),
            "branch": branch,
            "base": base,
            "repo_id": repo_id,
            "task_id": worktree_key,
        }
        if task_path != worktree_key:
            record["task_path"] = task_path
        if integrate_refs:
            record["integrated_branches"] = integrate_refs
        registry.setdefault("repos", {})[repo_id] = record
        registry["updated"] = datetime.now(timezone.utc).isoformat()
        atomic_json(reg_path, registry)
        return {"ok": True, "action": action, **record}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("task_id")
    parser.add_argument("repo_id")
    parser.add_argument("source_repo")
    parser.add_argument("--base")
    parser.add_argument("--integrate", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = prepare(
            Path(args.workspace),
            args.task_id,
            args.repo_id,
            Path(args.source_repo),
            args.base,
            args.integrate,
        )
    except (WorktreeError, json.JSONDecodeError, OSError) as exc:
        result = {"ok": False, "error": str(exc)}
        if isinstance(exc, WorktreeError) and exc.extra:
            result.update(exc.extra)
        code = exc.code if isinstance(exc, WorktreeError) else 1
    else:
        code = 0
    if args.json or not result["ok"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['action']}: {result['worktree']} ({result['branch']})")
    return code


if __name__ == "__main__":
    sys.exit(main())
