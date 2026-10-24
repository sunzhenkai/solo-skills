"""grill 先自查、自答并记录决定，只有真阻塞才问人。"""
from __future__ import annotations

import unittest
from pathlib import Path

TEXT = (Path(__file__).resolve().parents[1] / "references" / "grill.md").read_text(encoding="utf-8")


class GrillSelfAnswerTest(unittest.TestCase):
    def test_self_answer(self) -> None:
        self.assertIn("先查一手资料", TEXT)
        self.assertIn("自问自答", TEXT)
        self.assertIn("已做决定写 decisions.md", TEXT)
        self.assertIn("user-report.md", TEXT)
        self.assertIn("只有真阻塞", TEXT)


if __name__ == "__main__":
    unittest.main()
