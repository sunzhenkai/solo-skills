"""执行纪律：收尾校核、禁用 --yes、指向 done。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISC = (ROOT / "references" / "execution-discipline.md").read_text(encoding="utf-8")


class ExecutionSpineTest(unittest.TestCase):
    def test_no_yes_flag(self) -> None:
        self.assertIn("勾齐再归档", DISC)
        self.assertIn("未勾齐就不归档", DISC)

    def test_done_pointer(self) -> None:
        self.assertIn("done.md", DISC)

    def test_serial_checkbox(self) -> None:
        self.assertIn("串行", DISC)
        self.assertIn("全勾", DISC)

    def test_multi_worker_appendix(self) -> None:
        mw = (ROOT / "references" / "multi-worker.md").read_text(encoding="utf-8")
        self.assertIn("样板先行", mw)
        self.assertIn("同类失败", mw)
        self.assertIn("广播", mw)


if __name__ == "__main__":
    unittest.main()
