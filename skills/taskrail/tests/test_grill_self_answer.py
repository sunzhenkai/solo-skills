"""grill 自问自答契约。"""
from __future__ import annotations
import unittest
from pathlib import Path

TEXT = (Path(__file__).resolve().parents[1] / "references" / "design.md").read_text(encoding="utf-8")


class GrillSelfAnswerTest(unittest.TestCase):
    def test_self_answer(self) -> None:
        self.assertIn("自问自答", TEXT)
        self.assertIn("已做决定", TEXT)
        self.assertIn("user-report.md", TEXT)


if __name__ == "__main__":
    unittest.main()
