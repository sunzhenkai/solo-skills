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
        self.assertTrue((child.parent / "context" / "current.md").is_file())
        self.assertFalse((child.parent / "history.md").exists())
        self.assertFalse((child.parent / "decisions.md").exists())

    def test_root_starts_at_intent_with_pending_intent_and_plan_confirm(self) -> None:
        for mode in ("human", "goal"):
            with self.subTest(mode=mode):
                task = f"root-{mode}"
                created = self.run_state(
                    "init", str(self.workspace), task, "--title", task,
                    "--criterion", "verified outcome", "--confirm-mode", mode,
                )
                self.assertEqual(created.returncode, 0, created.stdout)
                root = self.workspace / "tasks" / "ongoing" / task
                self.assertIn("current_ref: intent", (root / "TASK.md").read_text(encoding="utf-8"))
                self.assertIn("确认状态：pending", (root / "context" / "current.md").read_text(encoding="utf-8"))
                plan_text = (root / "PLAN.md").read_text(encoding="utf-8")
                self.assertIn("## 实施确认", plan_text)
                self.assertIn("状态：pending", plan_text)

    def test_child_inherits_intent_without_independent_confirmation(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        context = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "context" / "current.md"
        self.assertIn("确认状态：not-required", context.read_text(encoding="utf-8"))

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
        override = self.run_state("init", str(self.workspace), "other", "--title", "other", "--parent", "parent", "--confirm-mode", "human")
        self.assertEqual(override.returncode, 0, override.stdout)
        other_md = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "other" / "TASK.md"
        self.assertIn("confirm_mode: human", other_md.read_text(encoding="utf-8"))
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

    def test_claim_requires_active_child_and_is_idempotent(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        root_claim = self.run_state("claim", str(self.workspace), "parent", "--owner", "worker-one")
        self.assertEqual(root_claim.returncode, 1)
        pending_claim = self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-one")
        self.assertEqual(pending_claim.returncode, 1)
        self.run_state("update", str(self.workspace), child_path, "--status", "active", "--current-ref", "plan")
        claimed = self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-one")
        self.assertEqual(claimed.returncode, 0, claimed.stdout)
        task = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        text = task.read_text(encoding="utf-8")
        self.assertIn("claimed_by: worker-one", text)
        self.assertRegex(text, r"claimed_at: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00")
        claimed_at = next(line for line in text.splitlines() if line.startswith("claimed_at:"))
        repeated = self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-one")
        self.assertEqual(repeated.returncode, 0, repeated.stdout)
        self.assertIn(claimed_at, task.read_text(encoding="utf-8"))
        other = self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-two")
        self.assertEqual(other.returncode, 1)
        self.assertIn("worker-one", task.read_text(encoding="utf-8"))

    def test_release_checks_owner_and_reconcile_preserves_claim(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        self.run_state("update", str(self.workspace), child_path, "--status", "active", "--current-ref", "plan")
        self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-one")
        wrong_owner = self.run_state("release", str(self.workspace), child_path, "--owner", "worker-two")
        self.assertEqual(wrong_owner.returncode, 1)
        reconciled = self.run_state("reconcile", str(self.workspace), child_path, "--repair")
        self.assertEqual(reconciled.returncode, 0, reconciled.stdout)
        payload = json.loads(reconciled.stdout)
        self.assertEqual(payload["claimed_by"], "worker-one")
        task = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        self.assertIn("claimed_by: worker-one", task.read_text(encoding="utf-8"))
        forced = self.run_state("release", str(self.workspace), child_path, "--force")
        self.assertEqual(forced.returncode, 0, forced.stdout)
        text = task.read_text(encoding="utf-8")
        self.assertIn("claimed_by: null", text)
        self.assertIn("claimed_at: null", text)
        reclaimed = self.run_state("claim", str(self.workspace), child_path, "--owner", "worker-two")
        self.assertEqual(reclaimed.returncode, 0, reclaimed.stdout)

    def test_legacy_child_without_claim_fields_can_be_claimed(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        self.run_state("update", str(self.workspace), child_path, "--status", "active", "--current-ref", "plan")
        task = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        text = task.read_text(encoding="utf-8")
        text = "\n".join(line for line in text.splitlines() if not line.startswith(("claimed_by:", "claimed_at:"))) + "\n"
        task.write_text(text, encoding="utf-8")
        claimed = self.run_state("claim", str(self.workspace), child_path, "--owner", "legacy-worker")
        self.assertEqual(claimed.returncode, 0, claimed.stdout)
        self.assertIn("claimed_by: legacy-worker", task.read_text(encoding="utf-8"))

    def test_concurrent_claim_has_one_winner(self) -> None:
        from concurrent.futures import ThreadPoolExecutor

        self.init("parent")
        self.init("child", "parent")
        child_path = "parent/subtasks/child"
        self.run_state("update", str(self.workspace), child_path, "--status", "active", "--current-ref", "plan")

        def claim(owner: int) -> subprocess.CompletedProcess:
            return self.run_state("claim", str(self.workspace), child_path, "--owner", f"worker-{owner}")

        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(claim, range(6)))
        self.assertEqual([result.returncode for result in results].count(0), 1, [r.stdout for r in results])
        self.assertEqual([result.returncode for result in results].count(1), 5)
        for result in results:
            json.loads(result.stdout)
        task = self.workspace / "tasks" / "ongoing" / "parent" / "subtasks" / "child" / "TASK.md"
        self.assertRegex(task.read_text(encoding="utf-8"), r"claimed_by: worker-\d")


    def confirm_intent(self, task_root: Path, status: str = "confirmed") -> None:
        (task_root / "context" / "current.md").write_text(
            f"# 当前事实与假设\n\n## 意图\n- 确认状态：{status}\n", encoding="utf-8"
        )

    def confirm_plan(self, task_root: Path, status: str = "confirmed") -> None:
        (task_root / "PLAN.md").write_text(
            f"# plan\n\n## 实施确认\n- 状态：{status}\n", encoding="utf-8"
        )

    def test_execute_blocks_when_design_lacks_approval_or_plan_pending(self) -> None:
        self.init("major")
        root = self.workspace / "tasks" / "ongoing" / "major"
        self.confirm_intent(root)
        (root / "design").mkdir()
        (root / "design" / "arch.md").write_text("# arch\n", encoding="utf-8")
        blocked = self.run_state("update", str(self.workspace), "major", "--current-ref", "execute")
        self.assertEqual(blocked.returncode, 1)
        self.assertIn("APPROVED.md", blocked.stdout)
        (root / "reviews").mkdir()
        (root / "reviews" / "APPROVED.md").write_text("   \n", encoding="utf-8")
        empty_approval = self.run_state("update", str(self.workspace), "major", "--current-ref", "execute")
        self.assertEqual(empty_approval.returncode, 1)
        self.assertIn("APPROVED.md", empty_approval.stdout)
        (root / "reviews" / "APPROVED.md").write_text("# approved\n", encoding="utf-8")
        plan_blocked = self.run_state("update", str(self.workspace), "major", "--current-ref", "execute")
        self.assertEqual(plan_blocked.returncode, 1)
        self.assertIn("pending", plan_blocked.stdout)
        self.confirm_plan(root)
        allowed = self.run_state("update", str(self.workspace), "major", "--current-ref", "execute")
        self.assertEqual(allowed.returncode, 0, allowed.stdout)

    def test_child_execute_accepts_parent_approval(self) -> None:
        self.init("parent")
        self.init("child", "parent")
        parent = self.workspace / "tasks" / "ongoing" / "parent"
        child = parent / "subtasks" / "child"
        self.confirm_plan(child)
        (child / "design").mkdir()
        (child / "design" / "detail.md").write_text("# detail\n", encoding="utf-8")
        blocked = self.run_state("update", str(self.workspace), "parent/subtasks/child", "--status", "active", "--current-ref", "execute")
        self.assertEqual(blocked.returncode, 1)
        (parent / "reviews").mkdir()
        (parent / "reviews" / "APPROVED.md").write_text("# parent approved\n", encoding="utf-8")
        allowed = self.run_state("update", str(self.workspace), "parent/subtasks/child", "--status", "active", "--current-ref", "execute")
        self.assertEqual(allowed.returncode, 0, allowed.stdout)

    def test_legacy_intake_alias_normalizes_to_intent(self) -> None:
        self.init("legacy-ref")
        updated = self.run_state("update", str(self.workspace), "legacy-ref", "--current-ref", "intake")
        self.assertEqual(updated.returncode, 0, updated.stdout)
        task = self.workspace / "tasks" / "ongoing" / "legacy-ref" / "TASK.md"
        self.assertIn("current_ref: intent", task.read_text(encoding="utf-8"))

    def test_plan_and_execute_block_on_pending_intent_missing_plan_confirm_or_empty_criterion(self) -> None:
        created = self.run_state("init", str(self.workspace), "strict", "--title", "strict")
        self.assertEqual(created.returncode, 0, created.stdout)
        root = self.workspace / "tasks" / "ongoing" / "strict"
        plan_blocked = self.run_state("update", str(self.workspace), "strict", "--current-ref", "plan")
        self.assertEqual(plan_blocked.returncode, 1)
        self.assertIn("意图确认状态", plan_blocked.stdout)
        exec_blocked = self.run_state("update", str(self.workspace), "strict", "--current-ref", "execute")
        self.assertEqual(exec_blocked.returncode, 1)
        self.assertIn("意图确认状态", exec_blocked.stdout)
        self.confirm_intent(root)
        plan_ok = self.run_state("update", str(self.workspace), "strict", "--current-ref", "plan")
        self.assertEqual(plan_ok.returncode, 0, plan_ok.stdout)
        no_criterion = self.run_state("update", str(self.workspace), "strict", "--current-ref", "execute")
        self.assertEqual(no_criterion.returncode, 1)
        self.assertIn("criterion", no_criterion.stdout)
        (root / "PLAN.md").write_text("# 计划：没有实施确认节\n", encoding="utf-8")
        missing_confirm = self.run_state(
            "update", str(self.workspace), "strict", "--criterion", "verified", "--current-ref", "execute"
        )
        self.assertEqual(missing_confirm.returncode, 1)
        self.assertIn("missing", missing_confirm.stdout)
        self.confirm_plan(root)
        allowed = self.run_state(
            "update", str(self.workspace), "strict", "--criterion", "verified", "--current-ref", "execute"
        )
        self.assertEqual(allowed.returncode, 0, allowed.stdout)

    def test_done_blocks_on_empty_or_headings_only_summary(self) -> None:
        self.init("sumcheck")
        root = self.workspace / "tasks" / "ongoing" / "sumcheck"
        for bad in ("", "   \n", "# 交付总结\n\n## 结果与验证\n", "# 交付总结\n- TODO\n"):
            (root / "SUMMARY.md").write_text(bad, encoding="utf-8")
            blocked = self.run_state("update", str(self.workspace), "sumcheck", "--status", "done")
            self.assertEqual(blocked.returncode, 1, f"should block summary={bad!r}")
        (root / "SUMMARY.md").write_text("# 交付总结\n\n## 结果与验证\n- 测试全过。\n", encoding="utf-8")
        ok = self.run_state("update", str(self.workspace), "sumcheck", "--status", "done")
        self.assertEqual(ok.returncode, 0, ok.stdout)

    def test_criterion_with_quotes_round_trips_cleanly(self) -> None:
        text = '按钮文案由 "提交" 改为 "保存"，且单测全过'
        created = self.run_state("init", str(self.workspace), "quoted", "--title", "quoted", "--criterion", text)
        self.assertEqual(created.returncode, 0, created.stdout)
        for _ in range(2):
            upd = self.run_state("update", str(self.workspace), "quoted", "--current-ref", "explore")
            self.assertEqual(upd.returncode, 0, upd.stdout)
        task_text = (self.workspace / "tasks" / "ongoing" / "quoted" / "TASK.md").read_text(encoding="utf-8")
        self.assertIn(f"criterion: {json.dumps(text, ensure_ascii=False)}", task_text)


if __name__ == "__main__":
    unittest.main()
