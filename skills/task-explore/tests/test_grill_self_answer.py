"""grill 自问自答：结论给用户；说决定见 user-report。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestGrillSelfAnswer(unittest.TestCase):
    def test_grill_self_answers(self) -> None:
        t = (ROOT / "references" / "explore-design.md").read_text(encoding="utf-8")
        self.assertIn("**自问自答**", t)
        self.assertIn("给用户只报结论", t)
        self.assertIn("user-report.md", t)
        self.assertIn("说决定", t)
        self.assertNotIn("决策交给用户", t)
        self.assertNotIn("当面问", t)


if __name__ == "__main__":
    unittest.main()
