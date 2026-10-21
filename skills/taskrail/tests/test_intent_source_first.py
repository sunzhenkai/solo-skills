"""source-first / 注意任务边界。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTENT = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")


class SourceFirstTest(unittest.TestCase):
    def test_boundary_label(self) -> None:
        self.assertIn("注意任务边界", INTENT)

    def test_word_sense_first(self) -> None:
        self.assertIn("先推词义", INTENT)

    def test_read_order(self) -> None:
        self.assertIn("读资料的顺序", INTENT)

    def test_scope_default(self) -> None:
        self.assertIn("目标加它的直接依赖", INTENT)

    def test_correction_reread(self) -> None:
        self.assertIn("先回第 1 节的一手资料重查", INTENT)

    def test_user_report_source_first(self) -> None:
        ur = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")
        self.assertIn("先查资料，能查到的不问", ur)


if __name__ == "__main__":
    unittest.main()
