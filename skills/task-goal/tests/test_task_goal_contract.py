"""task-goal 文本契约：完成程度条件、P 级定义、评审者三选一、pending 确认门与退出点。"""

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
        self.assertIn("id: task-goal", self.text)
        self.assertIn("name: task-goal", self.text)
        self.assertIn("description:", self.text)

    def test_id_matches_directory(self) -> None:
        self.assertEqual(SKILL_ROOT.name, "task-goal")

    def test_referenced_references_exist(self) -> None:
        for rel in (
            "references/quality-profile.md",
            "references/legacy-plans.md",
            "CONTEXT.md",
        ):
            self.assertTrue((SKILL_ROOT / rel).is_file(), rel)


class TestPlanIntake(unittest.TestCase):
    """解耦接口：接到上游 task-wizard 方案原文时逐字采用，不重新摸底。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_intake_verbatim(self) -> None:
        self.assertIn("跳过产方案，逐字采用，不重新摸底、不改写", self.text)

    def test_no_goal_branch_in_task_wizard(self) -> None:
        wizard = (SKILL_ROOT.parent / "task-wizard" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("## Goal 方案", wizard)
        self.assertNotIn("## 先分流", wizard)


class TestCompletionGradeConditions(unittest.TestCase):
    """完成程度写入是显式条件分支，P0/P1 有无优先于审阅者定级。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_explicit_condition_intro(self) -> None:
        self.assertIn("完成程度的写入按显式条件判定，P0/P1 的有无优先于审阅者定级：", self.text)

    def test_branch_with_p0_p1(self) -> None:
        self.assertIn("本轮发现含 P0 或 P1：完成程度取「中或低」。审阅者定级为高 → 写「中」；定级为中或低 → 从其值。", self.text)

    def test_branch_without_p0_p1(self) -> None:
        self.assertIn("本轮无 P0 也无 P1：完成程度写「高」，审阅者定级不参与。", self.text)

    def test_reviewer_grade_not_self_decided(self) -> None:
        self.assertIn("完成程度按本节规则写入，不由它自定", self.text)
        self.assertIn("执行者自己给出的完成程度不算审阅结论", self.text)


class TestSeverityDefinitions(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_p0_p1_p2_defined(self) -> None:
        self.assertIn("**P0**：完成判据不可检查", self.text)
        self.assertIn("**P1**：验证对不住判据", self.text)
        self.assertIn("**P2**：不改道的写法、顺序、两行限制或省略。P2 不参与完成程度", self.text)

    def test_role_reviewer_mapping(self) -> None:
        self.assertIn("Blocker 记 P0，Major 记 P1，Minor / Suggestion 记 P2", self.text)


class TestReviewerSelection(unittest.TestCase):
    """评审者三选一必选，选中唯一，新增「评审者未定」退出点。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")
        self.context = read("CONTEXT.md")

    def test_mandatory_choice(self) -> None:
        self.assertIn("评审者是必选项，每次审阅从三种里选一种，选中即唯一，不叠加", self.text)

    def test_three_ways_named(self) -> None:
        for way in ("role-based-reviewer", "agent-roster", "subagent"):
            self.assertIn(way, self.text)

    def test_old_fallback_wording_replaced(self) -> None:
        self.assertNotIn("其余情况：当前宿主拉起的子 agent", self.text)

    def test_reviewer_recorded(self) -> None:
        self.assertIn("每次审阅的评审者记录到回复里", self.text)

    def test_exit_point_reviewer_undecided(self) -> None:
        self.assertIn("**评审者未定**", self.text)
        self.assertIn("评审者未定；降级未确认", self.text)

    def test_context_reviewer_term_updated(self) -> None:
        self.assertIn("三种之一：subagent、agent-roster Endpoint、role-based-reviewer 编排的角色视角", self.context)


class TestPendingDowngradeGate(unittest.TestCase):
    """`pending` 降级只有用户能确认，审阅收敛与「继续」都不算。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_exit_point_wording(self) -> None:
        self.assertIn("只有用户点名接受该项、或明确说按降级表全部确认时，才把该项改为 `confirmed` 并继续；审阅收敛与单独的「继续」都不算确认", self.text)

    def test_quality_profile_reiterates_user_only(self) -> None:
        text = read("references/quality-profile.md")
        self.assertIn("只有用户能改 `confirmed`：点名接受该项，或明确说按降级表全部确认。执行者、审阅者、评审收敛都不算确认", text)

    def test_completion_requires_zero_pending(self) -> None:
        self.assertIn("`pending` 降级数为 0", self.text)
        text = read("references/quality-profile.md")
        self.assertIn("完成门：字段齐全，`pending` 降级数为 0", text)


class TestExitPoints(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_exit_point_labels_defined(self) -> None:
        for label in (
            "**理解不够**",
            "**审阅不通过**",
            "**审阅派不出**",
            "**审阅没有结论**",
            "**评审者未定**",
            "**降级未确认**",
            "**线上动作**",
            "**泄密**",
            "**执行中升档**",
        ):
            self.assertIn(label, self.text)

    def test_exit_list_present_in_template(self) -> None:
        self.assertIn("审阅不通过；审阅派不出；审阅没有结论；评审者未定；降级未确认", self.text)


class TestQualityProfileContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("references/quality-profile.md")

    def test_ui_four_questions_no_builtin_answers(self) -> None:
        self.assertIn("四问只约束「底线要写清」，不规定具体取值", self.text)
        self.assertIn("icon 形态: <是否收敛到单一 icon primitive 及其来源", self.text)

    def test_adjective_not_allowed(self) -> None:
        self.assertIn("「高质量」「体验好」「足够健壮」这类形容词不算", self.text)

    def test_role_bottom_lines_all_three(self) -> None:
        self.assertIn("`角色底线` 下的 product、design、engineer 三条一条都不能省", self.text)


if __name__ == "__main__":
    unittest.main()
