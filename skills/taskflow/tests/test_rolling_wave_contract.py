"""滚动展开：依赖满足才展开子 change、逐片提交、片间检查点不停人。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "references" / "driver-template.md").read_text(encoding="utf-8")
PROTO = TEMPLATE.split("## Driver 协议", 1)[1].split("## 验证记录", 1)[0]


class RollingWaveTest(unittest.TestCase):
    def test_protocol_expands_ready_slices_from_worktree_code(self) -> None:
        self.assertIn("依赖的实施项都已勾的切片才建子 change", PROTO)
        self.assertIn("起草时以 `worktrees/{task}` 里的代码为准", PROTO)

    def test_slice_item_checked_after_commit(self) -> None:
        self.assertIn("这一片已提交到任务分支后才勾", PROTO)
        self.assertIn("提交由编排者做，每片一次、收尾一次", PROTO)

    def test_checkpoint_keeps_going(self) -> None:
        self.assertIn("过一次片间检查点，不停人", PROTO)
        self.assertIn("意图变更", PROTO)

    def test_propose_expands_first_batch_only(self) -> None:
        wave = TEMPLATE.split("### 滚动展开", 1)[1]
        self.assertIn("propose 只给依赖已满足的那批切片备齐子 change", wave)
        self.assertIn("属于 approve 已批的范围", wave)
        self.assertIn("一片一条", TEMPLATE)

    def test_runtime_files_point_to_checkpoint(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        disc = (ROOT / "references" / "execution-discipline.md").read_text(encoding="utf-8")
        mw = (ROOT / "references" / "multi-worker.md").read_text(encoding="utf-8")
        for text in (skill, disc, mw):
            self.assertIn("片间检查点", text)
        self.assertIn("提交留给编排者", disc)


if __name__ == "__main__":
    unittest.main()
