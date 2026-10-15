"""注意任务边界：先推词义、按序读一手资料、默认范围、纠偏先重查（原则在 intent.md）。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class TestSourceFirst(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.ref = read("references/intent.md")

    def test_skill_boundary_line(self) -> None:
        self.assertIn("注意任务边界", self.skill)
        self.assertIn("references/intent.md", self.skill)

    def test_principles_in_intent_ref(self) -> None:
        for k in ("先推词义", "读资料的顺序", "目标加它的直接依赖", "不硬套现有数据模型"):
            self.assertIn(k, self.ref, k)

    def test_reading_order(self) -> None:
        sec = self.ref.split("**读资料的顺序（固定）：**", 1)[1].split("**范围默认", 1)[0]
        keys = ("用户原话", "CLAUDE.md", "compose", "`tasks/`", "要改的代码", "更大范围的台账")
        idx = [sec.index(k) for k in keys]
        self.assertEqual(idx, sorted(idx))
        self.assertIn("不得把其中能查到的内容当成未知、写成假设或拿去问用户", self.ref)

    def test_scope_and_citation(self) -> None:
        self.assertIn("目标加它的直接依赖", self.ref)
        self.assertIn("每条结论带出处", self.ref)

    def test_artifact_from_meaning(self) -> None:
        self.assertIn("不硬套现有数据模型", self.ref)
        self.assertIn("只读现状图", self.ref)

    def test_correction_rereads_and_frustration_stops(self) -> None:
        self.assertIn("先回第 1 节的一手资料重查", self.ref)
        self.assertIn("立刻停止提问", self.ref)
        self.assertIn("立刻停止提问", self.skill)

    def test_intent_reviewer_checks(self) -> None:
        t = (SKILLS / "role-based-reviewer/references/roles/intent.md").read_text(encoding="utf-8")
        for k in ("🔴 产物形态与词义不符", "🔴 该查没查", "🟡 范围失当"):
            self.assertIn(k, t)


if __name__ == "__main__":
    unittest.main()
