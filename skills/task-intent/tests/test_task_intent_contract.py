"""task-intent 行为契约（只测关键行为，不锁措辞）。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class TestTaskIntent(unittest.TestCase):
    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.ref = read("references/intent.md")

    def test_frontmatter_and_single_reference(self) -> None:
        self.assertTrue(self.skill.startswith("---\nid: task-intent\nname: task-intent\n"))
        self.assertEqual([p.name for p in (ROOT / "references").glob("*.md")], ["intent.md"])

    def test_checklist_is_internal_and_in_intent_file(self) -> None:
        self.assertIn("不照着打印", self.ref)
        block = re.search(r"## 覆盖清单\n(.*?)\n\n", self.ref, re.S).group(1)
        for f in ("要干嘛", "怎么干", "输出什么", "做完的样子", "上下文", "不做", "我的假设", "要你拍板的"):
            self.assertIn(f, block)

    def test_user_restatement_is_natural_prose(self) -> None:
        sec = re.search(r"## 3\. 给用户的复述[^\n]*\n(.*?)\n## ", self.ref, re.S).group(1)
        for s in ("1–3 句", "第一人称", "接下来", "最多一个问题", "不要标题、不要加粗标签"):
            self.assertIn(s, sec)
        examples = [l for l in sec.splitlines() if l.startswith("- ") and len(l) > 40]
        self.assertGreaterEqual(len(examples), 3)
        self.assertTrue(any("写完告诉你放在哪" in e for e in examples))
        for e in examples:
            self.assertNotIn("**", e)
        self.assertIn("不逐项列字段", self.skill)

    def test_explore_detailed_output_concise(self) -> None:
        for s in ("现状", "约束", "已有工作", "evidence/intent/"):
            self.assertIn(s, self.ref)
        self.assertIn("简洁", self.skill)

    def test_safety_lines(self) -> None:
        self.assertIn("忠于用户原话", self.skill)
        self.assertIn("goal 模式也必须停下等人", self.skill)
        self.assertIn("没回话不算确认", self.skill)

    def test_goal_review_and_fallback(self) -> None:
        self.assertIn("roles=intent", self.ref)
        self.assertIn("无 P0/P1", self.ref)
        self.assertIn("**不调用** role-based-reviewer", self.ref)


if __name__ == "__main__":
    unittest.main()
