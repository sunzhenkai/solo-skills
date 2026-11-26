"""user-report：以理解决策为边界、增量同步、按需展开且保留风险。"""
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

    def test_user_understanding_and_decision_drive_content(self) -> None:
        self.assertIn("理解现状、判断风险、作出决定或采取行动", UR)
        self.assertIn("最少证据", UR)
        self.assertIn("不按内部执行顺序复述过程", UR)

    def test_progressive_disclosure(self) -> None:
        self.assertIn("默认摘要，按需展开", UR)
        self.assertIn("足以支持本次判断", UR)
        self.assertIn("不为覆盖所有场景机械套用字段", UR)

    def test_blocker_categories(self) -> None:
        for s in ("删除或迁移数据", "共享配置", "线上", "对外发送", "完成判据", "缺凭据"):
            self.assertIn(s, UR)

    def test_resume_restores_context_without_fixed_script(self) -> None:
        self.assertIn("恢复用户上下文", UR)
        self.assertIn("存在阻塞时才补充", UR)
        self.assertNotIn("这个任务是要", UR)

    def test_contract_points_here(self) -> None:
        self.assertIn("user-report.md", CONTRACT)
        self.assertIn("用户表达", CONTRACT)

    def test_decision_ledger(self) -> None:
        self.assertIn("已做决定", UR)
        self.assertIn("难回头", UR)

    def test_incremental_reporting(self) -> None:
        self.assertIn("有效认知是否需要更新", UR)
        self.assertIn("没有新增结果", UR)
        self.assertIn("只同步最新增量", UR)
        self.assertIn("不构成用户确认", UR)

    def test_brevity_preserves_delivery_risks(self) -> None:
        self.assertIn("不以精简为由省略", UR)
        for s in ("验证缺口", "剩余风险", "未完成项", "必要授权"):
            self.assertIn(s, UR)


    def test_major_plan_plain_language_alignment_guide(self) -> None:
        self.assertIn("### 重大方案人话对齐", UR)
        for item in ("现状与目标", "整体方案", "关键取舍", "影响面、节奏与回退"):
            self.assertIn(item, UR)


if __name__ == "__main__":
    unittest.main()
