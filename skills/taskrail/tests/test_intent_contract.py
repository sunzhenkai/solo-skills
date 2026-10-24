"""意图确认：任务边界、覆盖清单、goal 代审和轻入口。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTENT = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")


class IntentContractTest(unittest.TestCase):
    def test_note_task_boundary(self) -> None:
        self.assertIn("注意任务边界", INTENT)
        self.assertIn("目标加它的直接依赖", INTENT)
        self.assertIn("不把“顺便优化”扩进任务", INTENT)

    def test_cover_fields(self) -> None:
        for field in ("要干嘛", "输出什么", "做完的样子", "上下文", "不做", "我的假设", "我的决定"):
            self.assertIn(field, INTENT)
        self.assertIn("实现步骤由 plan 负责", INTENT)

    def test_goal_review_uses_shared_confirmation_protocol(self) -> None:
        self.assertIn("confirm-protocol.md", INTENT)
        confirm = (ROOT / "references" / "confirm-protocol.md").read_text(encoding="utf-8")
        self.assertIn("另一个模型", confirm)
        self.assertIn("P0 / P1 挡路", confirm)
        self.assertIn("任何审阅都不放行真阻塞", confirm)

    def test_points_user_report(self) -> None:
        self.assertIn("user-report.md", INTENT)

    def test_light_entry_does_not_create_execution_branch(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("taskrail intent <一句话目标>", skill)
        self.assertIn("只做意图确认", skill)
        self.assertIn("没有任务目录就只在对话里给复述", skill)
        self.assertIn("不建执行分支", skill)


if __name__ == "__main__":
    unittest.main()
