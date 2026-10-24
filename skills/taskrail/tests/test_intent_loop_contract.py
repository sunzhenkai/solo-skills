"""意图闭环：动态重入、认知更正和受影响产物失效。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent


class IntentLoopTest(unittest.TestCase):
    def test_router_returns_to_intent_for_missing_or_changed_criterion(self) -> None:
        router = (ROOT / "references" / "router.md").read_text(encoding="utf-8")
        self.assertIn("为空或不可检查，回 [intent.md]", router)
        self.assertIn("criterion 改变 → intent", router)

    def test_done_checks_intent_not_old_snapshot_path(self) -> None:
        done = (ROOT / "references" / "done.md").read_text(encoding="utf-8")
        self.assertIn("意图未漂移", done)
        self.assertIn("输出形态", done)
        self.assertNotIn("wizard/intent.md", done)

    def test_correction_marks_old_beliefs_and_invalidates_only_affected_work(self) -> None:
        contract = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("意图与认知变更", contract)
        for word in ("refuted", "superseded", "只使受影响", "不改写"):
            self.assertIn(word, contract)

    def test_layout_uses_current_context_and_evidence(self) -> None:
        contract = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("context/current.md", contract)
        self.assertIn("evidence/", contract)
        self.assertNotIn("wizard/intent.md", contract)

    def test_intent_does_not_choose_execution_or_decomposition(self) -> None:
        intent = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("实现步骤由 plan 负责", intent)
        self.assertNotIn("tier:", intent)
        self.assertNotIn("`skip` 档", intent)

    def test_plain_talk_pointer(self) -> None:
        for rel in ("taskrail/SKILL.md", "taskrail/references/intent.md", "taskrail/references/design.md", "taskflow/SKILL.md"):
            text = (FAMILY / rel).read_text(encoding="utf-8")
            self.assertIn("user-report.md", text, rel)


if __name__ == "__main__":
    unittest.main()
