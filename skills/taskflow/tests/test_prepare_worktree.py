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


if __name__ == "__main__":
    unittest.main()
