"""task 族：taskrail + taskflow 两个 skill、术语单真源、无 CONTEXT 双真源。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent


class FamilyTest(unittest.TestCase):
    def test_skills_exist(self) -> None:
        for name in ("taskrail", "taskflow"):
            self.assertTrue((FAMILY / name / "SKILL.md").is_file(), name)

    def test_intent_and_explore_live_in_taskrail(self) -> None:
        for name in ("intent.md", "design.md", "approve.md", "handoff.md", "ledger.md", "templates.md"):
            self.assertTrue((ROOT / "references" / name).is_file(), name)
        for name in ("task-intent", "task-explore"):
            self.assertFalse((FAMILY / name).exists(), name)

    def test_contract_is_glossary(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("## 术语", c)
        self.assertIn("完成判据", c)
        self.assertFalse((ROOT / "CONTEXT.md").exists())

    def test_confirm_is_thin(self) -> None:
        n = len((ROOT / "references" / "confirm-protocol.md").read_bytes())
        self.assertLess(n, 4000)

    def test_ownership_table(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertNotIn("## Skill 归属", c)  # 归属只在 taskrail SKILL.md 开头一句
        c = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("意图确认、探索、设计、审批与交接都按本 skill 的阶段细则做", c)
        self.assertIn("交付交给 `taskflow`", c)


if __name__ == "__main__":
    unittest.main()
