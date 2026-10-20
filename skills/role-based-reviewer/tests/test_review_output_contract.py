"""评审输出骨架：依据状态、稳定编号、不代判收敛。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
PROTO = (ROOT / "references" / "protocol.md").read_text(encoding="utf-8")


class ReviewOutputTest(unittest.TestCase):
    def test_binding_state(self) -> None:
        self.assertIn("依据状态", SKILL)
        self.assertIn("## 依据状态", PROTO)

    def test_stable_ids(self) -> None:
        self.assertTrue("F-n" in SKILL or "F-" in PROTO)
        self.assertIn("F-1", PROTO)

    def test_no_claim_convergence(self) -> None:
        self.assertIn("不代判收敛", SKILL)

    def test_roles_enum(self) -> None:
        self.assertIn("qa", SKILL)
        self.assertIn("design", SKILL)

    def test_missing_boundary_not_refusal(self) -> None:
        self.assertTrue("缺项不拒审" in SKILL or "不拒审" in SKILL)


if __name__ == "__main__":
    unittest.main()
