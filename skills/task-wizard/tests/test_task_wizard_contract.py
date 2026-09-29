"""task-wizard 文本契约：方案层只做产出与决策收敛，goal 语义已迁往 task-goal。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_frontmatter_fields_present(self) -> None:
        self.assertIn("id: task-wizard", self.text)
        self.assertIn("name: task-wizard", self.text)
        self.assertIn("description:", self.text)

    def test_id_matches_directory(self) -> None:
        self.assertEqual(SKILL_ROOT.name, "task-wizard")

    def test_referenced_references_exist(self) -> None:
        for rel in (
            "references/external-precedent.md",
            "CONTEXT.md",
        ):
            self.assertTrue((SKILL_ROOT / rel).is_file(), rel)

    def test_moved_references_gone(self) -> None:
        for rel in (
            "references/quality-profile.md",
            "references/legacy-plans.md",
        ):
            self.assertFalse((SKILL_ROOT / rel).exists(), rel)


class TestGoalProtocolRemoved(unittest.TestCase):
    """Goal 方案与审阅语义整体迁往 task-goal，本 skill 不感知 goal。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_goal_sections_gone(self) -> None:
        for marker in (
            "## Goal 方案",
            "## 先分流",
            "## 审阅",
            "## 授权",
            "## 退出点",
            "## 写完之后",
            "### 不套模板",
            "### 旧方案",
        ):
            self.assertNotIn(marker, self.text)

    def test_goal_terms_gone(self) -> None:
        for term in (
            "方案置信度",
            "完成程度",
            "评审收敛",
            "Goal 方案",
        ):
            self.assertNotIn(term, self.text)

    def test_handoff_pointer_to_task_goal(self) -> None:
        self.assertIn("执行中的确认与审阅走 task-goal，本 skill 不参与", self.text)


class TestDecisionConvergence(unittest.TestCase):
    """决策收敛：所有要人拍板的缺口在方案落稿前写进方案。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")
        self.context = read("CONTEXT.md")

    def test_convergence_section(self) -> None:
        self.assertIn("## 决策收敛", self.text)

    def test_three_choice_only(self) -> None:
        self.assertIn("按此执行 / 调整哪步 / 改路由", self.text)

    def test_no_new_gaps_during_execution(self) -> None:
        self.assertIn("方案里没列出的缺口，不允许在执行期冒出来向人要答案", self.text)

    def test_context_term_defined(self) -> None:
        self.assertIn("**决策收敛**", self.context)


class TestComplexityRouting(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_three_tiers_present(self) -> None:
        self.assertIn("| 简单 | 局部修改 |", self.text)
        self.assertIn("| 中等 | 一个中等需求", self.text)
        self.assertIn("| 复杂 | 项目级重构或逻辑重塑", self.text)

    def test_product_hard_criteria(self) -> None:
        self.assertIn("产品交付硬指标，命中任一条即复杂", self.text)

    def test_no_goal_notes_in_routing(self) -> None:
        self.assertNotIn("Goal 方案进入「写完之后」时用同一套", self.text)


if __name__ == "__main__":
    unittest.main()
