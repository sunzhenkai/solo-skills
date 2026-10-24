"""user-report：说决定真源、resume 四行、不堆术语。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UR = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")
CONTRACT = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")


class UserReportTest(unittest.TestCase):
    def test_single_source_label(self) -> None:
        self.assertIn("唯一出处", UR)
        self.assertIn("说决定，不提问", UR)

    def test_blocker_categories(self) -> None:
        for s in ("删除或迁移数据", "共享配置", "线上", "对外发送", "完成判据", "缺凭据"):
            self.assertIn(s, UR)

    def test_resume_four_lines(self) -> None:
        self.assertIn("这个任务是要", UR)
        self.assertIn("目前", UR)
        self.assertIn("还卡着", UR)
        self.assertIn("接下来我会", UR)
        self.assertNotIn("挂起五元组", UR)

    def test_contract_points_here(self) -> None:
        self.assertIn("user-report.md", CONTRACT)
        self.assertIn("用户表达", CONTRACT)

    def test_decision_ledger(self) -> None:
        self.assertIn("已做决定", UR)
        self.assertIn("难回头", UR)


if __name__ == "__main__":
    unittest.main()
