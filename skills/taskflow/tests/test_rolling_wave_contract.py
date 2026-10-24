"""滚动展开：就绪切片、逐片提交、检查点重路由而非固定停人。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "references" / "driver-template.md").read_text(encoding="utf-8")
PROTO = TEMPLATE.split("## Driver 协议", 1)[1].split("## 验证记录", 1)[0]


class RollingWaveTest(unittest.TestCase):
    def test_only_ready_slices_are_expanded_from_current_worktree(self) -> None:
        self.assertIn("依赖的实施项都已勾的切片才建子 change", PROTO)
        self.assertIn("对应 worktree 当前代码为准", PROTO)
        self.assertIn("propose 只展开依赖已满足的切片", TEMPLATE)

    def test_driver_item_is_checked_after_validation_and_commit(self) -> None:
        self.assertIn("这一片已提交到任务分支", PROTO)
        self.assertIn("validate --strict", PROTO)
        self.assertIn("提交由编排者做，每片一次、收尾一次", PROTO)

    def test_checkpoint_re_routes_without_extra_stop(self) -> None:
        self.assertIn("片间检查点，不停人", PROTO)
        self.assertIn("只增删改未勾项", PROTO)
        self.assertIn("意图变更", PROTO)
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("片间检查点只说决定并继续", skill)

    def test_tasks_are_one_slice_per_item(self) -> None:
        self.assertIn("一片一条", TEMPLATE)
        self.assertIn("已勾项和已归档 changes 不改写", TEMPLATE)
        self.assertIn("父任务不再持一个重复进度的 driver", TEMPLATE)

    def test_execution_discipline_keeps_commit_and_checkpoint_rules(self) -> None:
        discipline = (ROOT / "references" / "execution-discipline.md").read_text(encoding="utf-8")
        self.assertIn("提交由编排者做", discipline)
        self.assertIn("片间检查点", discipline)
        self.assertIn("未勾齐就不归档", discipline)


if __name__ == "__main__":
    unittest.main()
