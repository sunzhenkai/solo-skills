"""绑定自行判定、grill 自问自答、goal 指针。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BehaviorTest(unittest.TestCase):
    def test_binding_decides(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("自行判定", ledger)

    def test_grill_self_answer(self) -> None:
        ed = (ROOT / "references" / "explore-design.md").read_text(encoding="utf-8")
        self.assertIn("自问自答", ed)
        self.assertIn("grilling", ed)

    def test_goal_points_confirm(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("confirm-protocol.md", skill)


if __name__ == "__main__":
    unittest.main()
