"""确认协议薄契约：两种模式 + 真阻塞不停审阅放行。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfirmContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (ROOT / "references" / "confirm-protocol.md").read_text(encoding="utf-8")
        cls.ur = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")

    def test_dual_mode(self) -> None:
        self.assertIn("human", self.text)
        self.assertIn("goal", self.text)
        self.assertIn("另一个模型", self.text)

    def test_true_blocker_not_auto(self) -> None:
        self.assertIn("真阻塞", self.text)
        self.assertIn("不放行真阻塞", self.text.replace("**", ""))

    def test_points_to_user_report(self) -> None:
        self.assertIn("user-report.md", self.text)
        self.assertIn("说决定，不提问", self.ur)

    def test_no_suspension_five_tuple(self) -> None:
        self.assertFalse((ROOT / "references" / "suspension.md").exists())
        self.assertNotIn("挂起五元组", self.text)
        self.assertNotIn("五元组", self.ur)


if __name__ == "__main__":
    unittest.main()
