"""task-intent 文本契约测试。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class TestTaskIntentContract(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.tpl = read("references/statement-template.md")
        self.loop = read("references/correction-loop.md")
        self.goal = read("references/goal-review.md")
        self.probe = read("references/probe.md")

    def test_frontmatter(self) -> None:
        self.assertTrue(self.skill.startswith("---\nid: task-intent\nname: task-intent\n"))
        self.assertIn("不要用", self.skill)

    def test_size(self) -> None:
        self.assertLess(len(self.skill.encode("utf-8")), 8192)

    def test_template_six_fields_max_8_lines(self) -> None:
        block = re.search(r"```markdown\n(.*?)```", self.tpl, re.S).group(1)
        lines = [l for l in block.splitlines() if l.strip()]
        self.assertLessEqual(len(lines), 8)
        for f in ("你要的是", "为什么要", "做完的样子", "不做", "我的假设", "要你拍板的"):
            self.assertIn(f, block)

    def test_correction_loop_exit(self) -> None:
        for s in ("明确确认", "第 3 轮", "二选一", "硬上限 5 轮", "只改被指出的行", "不得再错"):
            self.assertIn(s, self.loop)
        self.assertIn("没回话", self.loop)

    def test_goal_review(self) -> None:
        self.assertIn("roles=intent", self.goal)
        self.assertIn("≥0.8", self.goal)
        self.assertIn("最多 2 轮", self.goal)
        self.assertIn("显式降级", self.goal)
        self.assertIn("不可逆", self.goal)

    def test_probe_dispatch(self) -> None:
        self.assertIn("并行", self.probe)
        self.assertIn("交接契约", self.probe)
        self.assertIn("Digest（≤10 行）", self.probe)
        self.assertIn("只读", self.probe)
        self.assertIn("不回灌工具轨迹", self.probe)

    def test_skill_gates(self) -> None:
        for s in ("先查后问", "推荐答案", "忠于用户原话", "wizard/intent.md", "宿主无 subagent"):
            self.assertIn(s, self.skill)

    def test_evals_count(self) -> None:
        self.assertGreaterEqual(read("evals/cases.yaml").count("  - id: "), 20)


if __name__ == "__main__":
    unittest.main()
