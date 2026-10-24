"""真阻塞 / 普通取舍 / 已做决定表。"""
from __future__ import annotations
import unittest
from pathlib import Path

UR = (Path(__file__).resolve().parents[1] / "references" / "user-report.md").read_text(encoding="utf-8")


class DecisionBoundaryTest(unittest.TestCase):
    def test_must_stop(self) -> None:
        self.assertIn("真阻塞才停", UR)
        for s in ("删除或迁移数据", "共享配置", "线上", "对外发送", "完成判据"):
            self.assertIn(s, UR)

    def test_ordinary_no_stop(self) -> None:
        self.assertIn("普通可回头取舍", UR)
        self.assertIn("直接定", UR)

    def test_ledger(self) -> None:
        self.assertIn("已做决定写 decisions.md", UR)
        self.assertIn("难回头决定", UR)
        self.assertIn("单独说", UR)


if __name__ == "__main__":
    unittest.main()
