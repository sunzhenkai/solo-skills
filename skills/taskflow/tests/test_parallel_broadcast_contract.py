"""并行执行主会话侧协调纪律：共享面变更广播与范围核对（20261011 进化轮文本锁）。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class TestParallelMainSessionCoordination(unittest.TestCase):
    """主会话在并行飞行中写共享面必须广播；补写已分配文件前核对范围。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_broadcast_rule_present(self) -> None:
        self.assertIn("改共享面必广播", self.text)

    def test_broadcast_rule_requires_agent_message(self) -> None:
        self.assertIn("`write agent://all`", self.text)
        self.assertIn("`write agent://<id>`", self.text)

    def test_broadcast_rule_content_shape(self) -> None:
        self.assertIn("广播改动点、影响面与子代理范围是否调整", self.text)
        self.assertIn("按修正后契约继续，不视为打断", self.text)

    def test_scope_check_rule_present(self) -> None:
        self.assertIn("补写已分配文件前核对范围", self.text)
        self.assertIn("对照派发分配表", self.text)
        self.assertIn("立即定向通知该子代理收敛其范围", self.text)

    def test_existing_agent_constraints_intact(self) -> None:
        """新规则追加不削弱子代理侧既有纪律。"""
        self.assertIn("只改自己范围内的代码与自己的 `tasks.md` checkbox", self.text)
        self.assertIn("不勾 driver 编排项", self.text)
        self.assertIn("主会话负责派发、汇总、处理冲突与未勾原因", self.text)


if __name__ == "__main__":
    unittest.main()
