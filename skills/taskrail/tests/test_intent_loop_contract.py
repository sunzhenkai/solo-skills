"""意图闭环：wizard 委托、完成对照 intent、意图变更。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent


class IntentLoopTest(unittest.TestCase):
    def test_wizard_delegates(self) -> None:
        w = (ROOT / "references" / "phase-wizard.md").read_text(encoding="utf-8")
        self.assertIn("task-intent", w)

    def test_done_reads_intent(self) -> None:
        d = (ROOT / "references" / "done.md").read_text(encoding="utf-8")
        self.assertIn("wizard/intent.md", d)

    def test_intent_change_in_contract(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("意图变更", c)
        self.assertIn("重跑 `task-intent`", c)

    def test_layout_has_intent_dirs(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("wizard/intent.md", c)
        self.assertIn("evidence/intent/", c)

    def test_skip_rule_in_intent(self) -> None:
        skill = (FAMILY / "task-intent" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("何时跳过", skill)
        self.assertIn("skip", skill)

    def test_plain_talk_pointer(self) -> None:
        for rel in ("taskrail/SKILL.md", "task-intent/SKILL.md", "task-explore/SKILL.md", "taskflow/SKILL.md"):
            text = (FAMILY / rel).read_text(encoding="utf-8")
            self.assertIn("user-report.md", text, rel)


if __name__ == "__main__":
    unittest.main()
