"""完成清单与当前计划模板，不依赖旧 wizard 四节。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DoneAndPlanTest(unittest.TestCase):
    def test_done_items(self) -> None:
        done = (ROOT / "references" / "done.md").read_text(encoding="utf-8")
        for text in ("判据成立", "意图未漂移", "交付标准", "知识闭环", "观感验收", "goal", "human"):
            self.assertIn(text, done)

    def test_plan_has_executable_steps_and_verification(self) -> None:
        plan = (ROOT / "references" / "plan.md").read_text(encoding="utf-8")
        templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")
        self.assertIn("当前可执行的一小组动作", plan)
        self.assertIn("## 当前步骤", templates)
        self.assertIn("## 验证策略", templates)
        self.assertIn("## 约束 / 回滚", templates)

    def test_no_verbatim_snapshot_rule(self) -> None:
        for name in ("contract.md", "done.md", "plan.md"):
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("逐字复制", text)
            self.assertNotIn("原文快照", text)


if __name__ == "__main__":
    unittest.main()
