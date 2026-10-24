from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "task_state.py"


class TaskStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name) / "workspace"
        self.workspace.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_state(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)

    def init(self, task: str, parent: str | None = None) -> None:
        args = ["init", str(self.workspace), task, "--title", task, "--criterion", "verified outcome"]
        if parent:
            args += ["--parent", parent]
        result = self.run_state(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_init_parent_child_and_derived_index(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        self.assertTrue(child.is_file())
        self.assertIn("status: pending", child.read_text(encoding="utf-8"))
        index = (self.workspace / "tasks" / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("ongoing/parent/subtasks/child", index)
        self.assertTrue((child.parent / "PLAN.md").is_file())
        self.assertTrue((child.parent / "history.md").is_file())

    def test_done_requires_summary_and_children_done(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        parent = self.workspace / "tasks" / "ongoing" / "parent"
        (parent / "SUMMARY.md").write_text("summary\n", encoding="utf-8")
        result = self.run_state("update", str(self.workspace), "parent", "--status", "done")
        self.assertEqual(result.returncode, 1)
        child_path = "parent/subtasks/child"
        result = self.run_state("update", str(self.workspace), child_path, "--status", "done")
        self.assertEqual(result.returncode, 1)
        (parent / "subtasks" / "child" / "SUMMARY.md").write_text("summary\n", encoding="utf-8")
        result = self.run_state("update", str(self.workspace), child_path, "--status", "done")
        self.assertEqual(result.returncode, 0, result.stdout)
        result = self.run_state("update", str(self.workspace), "parent", "--status", "done")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_reconcile_repairs_false_done(self) -> None:
        self.init("parent")
        task = self.workspace / "tasks" / "ongoing" / "parent" / "TASK.md"
        task.write_text(task.read_text(encoding="utf-8").replace("status: active", "status: done"), encoding="utf-8")
        result = self.run_state("reconcile", str(self.workspace), "parent")
        self.assertEqual(result.returncode, 1)
        self.assertIn("done requires SUMMARY.md", result.stdout)
        repaired = self.run_state("reconcile", str(self.workspace), "parent", "--repair")
        self.assertEqual(repaired.returncode, 0, repaired.stdout)
        text = task.read_text(encoding="utf-8")
        self.assertIn("status: active", text)
        self.assertIn("current_ref: close", text)

    def test_reconcile_routes_completed_children_to_parent_verify(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child"
        (child / "SUMMARY.md").write_text("summary\n", encoding="utf-8")
        self.run_state("update", str(self.workspace), "parent/subtasks/child", "--status", "done")
        result = self.run_state("reconcile", str(self.workspace), "parent", "--repair")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["recommended_ref"], "verify")

    def test_update_preserves_unknown_legacy_metadata(self) -> None:
        self.init("parent")
        task = self.workspace / "tasks" / "ongoing" / "parent" / "TASK.md"
        text = task.read_text(encoding="utf-8").replace("updated:", "gate_bypass: \"legacy value\"\nupdated:")
        task.write_text(text, encoding="utf-8")
        result = self.run_state("update", str(self.workspace), "parent", "--current-ref", "explore")
        self.assertEqual(result.returncode, 0, result.stdout)
        updated = task.read_text(encoding="utf-8")
        self.assertIn("gate_bypass: \"legacy value\"", updated)
        self.assertIn("current_ref: explore", updated)


    def test_child_inherits_goal_and_criterion_update_is_consistent(self) -> None:
        created = self.run_state("init", str(self.workspace), "parent", "--title", "parent", "--criterion", "old", "--confirm-mode", "goal")
        self.assertEqual(created.returncode, 0, created.stdout)
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        child = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        self.assertIn("confirm_mode: goal", child.read_text(encoding="utf-8"))
        mismatch = self.run_state("init", str(self.workspace), "other", "--title", "other", "--parent", "parent", "--confirm-mode", "human")
        self.assertEqual(mismatch.returncode, 1)
        updated = self.run_state("update", str(self.workspace), child_path, "--criterion", "new observable outcome")
        self.assertEqual(updated.returncode, 0, updated.stdout)
        text = child.read_text(encoding="utf-8")
        self.assertIn('criterion: "new observable outcome"', text)
        self.assertIn("## 完成判据\nnew observable outcome", text)
        self.assertNotIn("## 完成判据\nverified outcome", text)

    def test_pending_child_can_be_activated_without_completing_parent(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        activated = self.run_state("update", str(self.workspace), child_path, "--status", "active", "--current-ref", "plan")
        self.assertEqual(activated.returncode, 0, activated.stdout)
        parent = self.run_state("reconcile", str(self.workspace), "parent")
        self.assertEqual(parent.returncode, 0, parent.stdout)
        payload = json.loads(parent.stdout)
        self.assertEqual(payload["children"], {"child": "active"})
        self.assertIsNone(payload["recommended_ref"])

    def test_reconcile_does_not_infer_done_from_archived_driver(self) -> None:
        self.init("parent")
        updated = self.run_state("update", str(self.workspace), "parent", "--execution", "openspec", "--current-ref", "review", "--driver", "parent-driver")
        self.assertEqual(updated.returncode, 0, updated.stdout)
        archive = self.workspace / "openspec" / "changes" / "archive" / "parent-driver"
        archive.mkdir(parents=True)
        result = self.run_state("reconcile", str(self.workspace), "parent")
        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "active")
        self.assertEqual(payload["current_ref"], "review")
        self.assertIsNone(payload["recommended_ref"])

    def test_driver_identity_is_validated(self) -> None:
        self.init("parent")
        result = self.run_state("update", str(self.workspace), "parent", "--driver", "another-driver")
        self.assertEqual(result.returncode, 1)
        self.assertIn("parent-driver", result.stdout)
        task = self.workspace / "tasks" / "ongoing" / "parent" / "TASK.md"
        self.assertIn("driver: null", task.read_text(encoding="utf-8"))

    def test_concurrent_init_has_one_winner_and_valid_index(self) -> None:
        from concurrent.futures import ThreadPoolExecutor

        args = ("init", str(self.workspace), "race", "--title", "race", "--criterion", "one task")
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.run_state(*args), range(6)))
        self.assertEqual([result.returncode for result in results].count(0), 1, [r.stdout for r in results])
        self.assertEqual([result.returncode for result in results].count(1), 5)
        for result in results:
            json.loads(result.stdout)
        index = (self.workspace / "tasks" / "INDEX.md").read_text(encoding="utf-8")
        self.assertEqual(index.count("| ongoing/race |"), 1)
        task = self.workspace / "tasks" / "ongoing" / "race" / "TASK.md"
        self.assertTrue(task.is_file())
        self.assertIn("status: active", task.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
