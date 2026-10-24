"""task 族边界：taskrail 编排，taskflow 执行，术语与确认协议单真源。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent


class FamilyTest(unittest.TestCase):
    def test_skills_exist(self) -> None:
        for name in ("taskrail", "taskflow"):
            self.assertTrue((FAMILY / name / "SKILL.md").is_file(), name)

    def test_orchestration_references_live_in_taskrail(self) -> None:
        for name in ("intent.md", "router.md", "explore.md", "diagnose.md", "grill.md", "design.md", "approve.md", "decompose.md", "handoff.md"):
            self.assertTrue((ROOT / "references" / name).is_file(), name)
        for name in ("task-intent", "task-explore"):
            self.assertFalse((FAMILY / name).exists(), name)

    def test_contract_is_glossary(self) -> None:
        contract = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("术语", contract)
        self.assertIn("criterion", contract)
        self.assertFalse((ROOT / "CONTEXT.md").exists())

    def test_confirm_is_thin(self) -> None:
        size = len((ROOT / "references" / "confirm-protocol.md").read_bytes())
        self.assertLess(size, 4000)

    def test_ownership_is_explicit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("本 skill 负责事实、路由、父子任务和收口", skill)
        self.assertIn("代码实施交给 `taskflow`", skill)
        flow = (FAMILY / "taskflow" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不在 taskflow 自行判 done", flow)


if __name__ == "__main__":
    unittest.main()
