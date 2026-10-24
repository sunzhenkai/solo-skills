"""绑定自行判定、grill 自答、任务归档和恢复行为。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BehaviorTest(unittest.TestCase):
    def test_binding_decides(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("自行判定", ledger)
        self.assertIn("一句话说出决定和理由", ledger)

    def test_grill_self_answer(self) -> None:
        grill = (ROOT / "references" / "grill.md").read_text(encoding="utf-8")
        self.assertIn("自问自答", grill)
        self.assertIn("设计树", grill)
        self.assertIn("每题由自己回答", grill)
        self.assertNotIn("委托 `grilling`", grill)

    def test_done_archives_same_round(self) -> None:
        archive = (ROOT / "references" / "archive-reopen.md").read_text(encoding="utf-8")
        self.assertIn("完成归档", archive)
        self.assertIn("同轮把父任务整树移到", archive)
        self.assertIn("未完成关闭", archive)

    def test_resume_reconciles_instead_of_deriving_old_phases(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("reconcile", ledger)
        self.assertIn("不映射回固定双流程", ledger)
        self.assertIn("旧 `phase/tier/status` 按现有产物兼容理解", ledger)

    def test_gate_script_path_placeholder(self) -> None:
        handoff = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        self.assertIn("<taskflow>/scripts/check_handoff.py", handoff)

    def test_goal_points_confirm(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("confirm-protocol.md", skill)


if __name__ == "__main__":
    unittest.main()
