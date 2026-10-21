"""绑定自行判定、grill 自问自答、任务归档、goal 指针。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BehaviorTest(unittest.TestCase):
    def test_binding_decides(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("自行判定", ledger)

    def test_grill_self_answer(self) -> None:
        ed = (ROOT / "references" / "design.md").read_text(encoding="utf-8")
        self.assertIn("自问自答", ed)
        self.assertIn("设计树", ed)
        self.assertIn("每题由自己回答", ed)
        self.assertNotIn("委托 `grilling`", ed)  # grilling 要求逐条问用户并等回答，与 design 不停人相反

    def test_done_archives_same_round(self) -> None:
        ar = (ROOT / "references" / "archive-reopen.md").read_text(encoding="utf-8")
        self.assertIn("做完归档", ar)
        self.assertIn("同轮归档", ar)
        self.assertIn("未完成关闭", ar)

    def test_resume_derives_post_handoff(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("交接后的位置", ledger)

    def test_gate_script_path_placeholder(self) -> None:
        h = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        self.assertIn("<taskflow>/scripts/check_handoff.py", h)

    def test_goal_points_confirm(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("confirm-protocol.md", skill)


if __name__ == "__main__":
    unittest.main()
