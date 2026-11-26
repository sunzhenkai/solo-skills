from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_worktree.py"


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if proc.returncode:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


class PrepareWorktreeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.workspace = self.root / "workspace"
        self.source = self.root / "source"
        self.source.mkdir()
        git(self.source, "init", "-b", "main")
        git(self.source, "config", "user.email", "tests@example.invalid")
        git(self.source, "config", "user.name", "Tests")
        (self.source / "README.md").write_text("base\n", encoding="utf-8")
        git(self.source, "add", "README.md")
        git(self.source, "commit", "-m", "base")
        self.workspace.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_prepare(self, task: str = "demo-task", repo: str = "app") -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.workspace), task, repo, str(self.source), "--json"],
            text=True, capture_output=True,
        )

    def test_create_and_resume_without_remote(self) -> None:
        created = self.run_prepare()
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        payload = json.loads(created.stdout)
        self.assertEqual(payload["action"], "created")
        worktree = Path(payload["worktree"])
        self.assertTrue(worktree.is_dir())
        self.assertEqual(git(worktree, "branch", "--show-current"), "task/demo-task")
        self.assertEqual(git(self.source, "branch", "--show-current"), "main")
        resumed = self.run_prepare()
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertEqual(json.loads(resumed.stdout)["action"], "resumed")

    def test_dirty_worktree_is_preserved_and_rejected(self) -> None:
        created = json.loads(self.run_prepare().stdout)
        worktree = Path(created["worktree"])
        (worktree / "README.md").write_text("user work\n", encoding="utf-8")
        result = self.run_prepare()
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertEqual((worktree / "README.md").read_text(encoding="utf-8"), "user work\n")

    def test_unregistered_branch_collision_is_rejected(self) -> None:
        git(self.source, "branch", "task/demo-task", "HEAD")
        result = self.run_prepare()
        self.assertEqual(result.returncode, 4, result.stdout)
        self.assertFalse((self.workspace / "worktrees" / "demo-task" / "app").exists())

    def test_workspace_inside_source_adds_exclude(self) -> None:
        self.workspace = self.source
        result = self.run_prepare(task="nested-task")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        exclude = self.source / ".git" / "info" / "exclude"
        self.assertIn("worktrees/", exclude.read_text(encoding="utf-8").splitlines())

    def test_invalid_ids_cannot_escape_workspace(self) -> None:
        result = self.run_prepare(task="../escape")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "escape").exists())


    def make_second_repo(self) -> Path:
        second = self.root / "second"
        second.mkdir()
        git(second, "init", "-b", "main")
        git(second, "config", "user.email", "tests@example.invalid")
        git(second, "config", "user.name", "Tests")
        (second / "app.txt").write_text("second base\n", encoding="utf-8")
        git(second, "add", "app.txt")
        git(second, "commit", "-m", "base")
        return second

    def test_two_repositories_get_independent_worktrees_and_registrations(self) -> None:
        second = self.make_second_repo()
        first = self.run_prepare(repo="backend")
        self.assertEqual(first.returncode, 0, first.stdout)
        second_result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.workspace), "demo-task", "frontend", str(second), "--json"],
            text=True, capture_output=True,
        )
        self.assertEqual(second_result.returncode, 0, second_result.stdout)
        first_payload = json.loads(first.stdout)
        second_payload = json.loads(second_result.stdout)
        self.assertNotEqual(first_payload["worktree"], second_payload["worktree"])
        self.assertEqual(git(Path(first_payload["worktree"]), "branch", "--show-current"), "task/demo-task")
        self.assertEqual(git(Path(second_payload["worktree"]), "branch", "--show-current"), "task/demo-task")
        self.assertEqual(git(second, "branch", "--show-current"), "main")
        registry = json.loads((self.workspace / "worktrees" / "demo-task" / "registry.json").read_text(encoding="utf-8"))
        self.assertEqual(set(registry["repos"]), {"backend", "frontend"})
        self.assertEqual(Path(registry["repos"]["frontend"]["source_repo"]), second.resolve())

    def test_repo_id_cannot_be_rebound_to_another_source(self) -> None:
        second = self.make_second_repo()
        self.assertEqual(self.run_prepare().returncode, 0)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.workspace), "demo-task", "app", str(second), "--json"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 4, result.stdout)
        registry = json.loads((self.workspace / "worktrees" / "demo-task" / "registry.json").read_text(encoding="utf-8"))
        self.assertEqual(Path(registry["repos"]["app"]["source_repo"]), self.source.resolve())

    def test_dirty_source_is_preserved_and_not_copied_into_worktree(self) -> None:
        (self.source / "README.md").write_text("source user work\n", encoding="utf-8")
        result = self.run_prepare()
        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual((Path(payload["worktree"]) / "README.md").read_text(encoding="utf-8"), "base\n")
        self.assertEqual((self.source / "README.md").read_text(encoding="utf-8"), "source user work\n")
        self.assertEqual(git(self.source, "branch", "--show-current"), "main")

    def test_subtask_path_isolates_worktree_and_branch_across_parents(self) -> None:
        parent_a = self.run_prepare(task="parent-a")
        self.assertEqual(parent_a.returncode, 0, parent_a.stdout + parent_a.stderr)
        child_a = self.run_prepare(task="parent-a/subtasks/api")
        self.assertEqual(child_a.returncode, 0, child_a.stdout + child_a.stderr)
        child_b = self.run_prepare(task="parent-b/subtasks/api")
        self.assertEqual(child_b.returncode, 0, child_b.stdout + child_b.stderr)
        payload_a = json.loads(child_a.stdout)
        payload_b = json.loads(child_b.stdout)
        self.assertEqual(payload_a["branch"], "task/parent-a--api")
        self.assertEqual(payload_b["branch"], "task/parent-b--api")
        self.assertEqual(payload_a["task_id"], "parent-a--api")
        self.assertEqual(payload_a["task_path"], "parent-a/subtasks/api")
        self.assertTrue(payload_a["worktree"].endswith("worktrees/parent-a--api/app"))
        self.assertTrue(payload_b["worktree"].endswith("worktrees/parent-b--api/app"))
        self.assertEqual(git(Path(payload_a["worktree"]), "branch", "--show-current"), "task/parent-a--api")
        self.assertEqual(git(Path(payload_b["worktree"]), "branch", "--show-current"), "task/parent-b--api")
        resumed = self.run_prepare(task="parent-a/subtasks/api")
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertEqual(json.loads(resumed.stdout)["action"], "resumed")

    def test_parent_integration_worktree_merges_multiple_child_branches_idempotently(self) -> None:
        child_a = json.loads(self.run_prepare(task="checkout/subtasks/pricing").stdout)
        wt_a = Path(child_a["worktree"])
        (wt_a / "pricing.txt").write_text("pricing ok\n", encoding="utf-8")
        git(wt_a, "add", "pricing.txt")
        git(wt_a, "commit", "-m", "add pricing")

        child_b = json.loads(self.run_prepare(task="checkout/subtasks/coupon").stdout)
        wt_b = Path(child_b["worktree"])
        (wt_b / "coupon.txt").write_text("coupon ok\n", encoding="utf-8")
        git(wt_b, "add", "coupon.txt")
        git(wt_b, "commit", "-m", "add coupon")

        cmd = [
            sys.executable, str(SCRIPT), str(self.workspace), "checkout/integration", "app", str(self.source),
            "--integrate", child_a["branch"], "--integrate", child_b["branch"], "--json",
        ]
        integrated = subprocess.run(cmd, text=True, capture_output=True)
        self.assertEqual(integrated.returncode, 0, integrated.stdout + integrated.stderr)
        payload = json.loads(integrated.stdout)
        self.assertEqual(payload["action"], "integrated")
        self.assertEqual(payload["branch"], "task/checkout--integration")
        self.assertEqual(payload["integrated_branches"], [child_a["branch"], child_b["branch"]])
        wt_int = Path(payload["worktree"])
        self.assertTrue((wt_int / "pricing.txt").is_file())
        self.assertTrue((wt_int / "coupon.txt").is_file())
        self.assertEqual(git(self.source, "branch", "--show-current"), "main")
        self.assertEqual(git(self.source, "status", "--porcelain"), "")
        self.assertFalse((self.source / "pricing.txt").exists())

        resumed = subprocess.run(cmd, text=True, capture_output=True)
        self.assertEqual(resumed.returncode, 0, resumed.stdout + resumed.stderr)
        self.assertEqual(json.loads(resumed.stdout)["action"], "resumed")

    def test_parent_integration_conflict_aborts_cleanly_and_reports_files(self) -> None:
        child_a = json.loads(self.run_prepare(task="conflict/subtasks/one").stdout)
        wt_a = Path(child_a["worktree"])
        (wt_a / "README.md").write_text("from one\n", encoding="utf-8")
        git(wt_a, "add", "README.md")
        git(wt_a, "commit", "-m", "change readme in one")

        child_b = json.loads(self.run_prepare(task="conflict/subtasks/two").stdout)
        wt_b = Path(child_b["worktree"])
        (wt_b / "README.md").write_text("from two\n", encoding="utf-8")
        git(wt_b, "add", "README.md")
        git(wt_b, "commit", "-m", "change readme in two")

        proc = subprocess.run(
            [
                sys.executable, str(SCRIPT), str(self.workspace), "conflict/integration", "app", str(self.source),
                "--integrate", child_a["branch"], "--integrate", child_b["branch"], "--json",
            ],
            text=True, capture_output=True,
        )
        self.assertEqual(proc.returncode, 5, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["conflict_branch"], child_b["branch"])
        self.assertIn("README.md", payload["conflict_files"])
        wt_int = self.workspace / "worktrees" / "conflict--integration" / "app"
        self.assertEqual(git(wt_int, "status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
