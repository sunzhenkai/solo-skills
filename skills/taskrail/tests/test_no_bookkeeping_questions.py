"""记账不问人：绑定自行判定并陈述。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UR = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")
LEDGER = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")


class NoBookkeepingQuestionsTest(unittest.TestCase):
    def test_binding_decides(self) -> None:
        self.assertIn("自行判定", LEDGER)
        self.assertIn("一句话说出决定和理由", LEDGER)

    def test_bookkeeping_listed(self) -> None:
        self.assertIn("记账", UR)
        self.assertIn("直接做", UR)

    def test_no_trailing_invitation_rule(self) -> None:
        self.assertIn("理解偏了请纠正", UR)


if __name__ == "__main__":
    unittest.main()
