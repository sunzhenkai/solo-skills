"""agent-wizard 文本契约：路径边界、证据门禁、信息落点与行为验证。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
SKILL_AUTHORING = (SKILL_ROOT / "references" / "skill-authoring.md").read_text(
    encoding="utf-8"
)
AGENTS_MD = (SKILL_ROOT / "references" / "agents-md.md").read_text(encoding="utf-8")
REVIEW = (SKILL_ROOT / "references" / "review.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_trio(self) -> None:
        self.assertRegex(
            SKILL,
            r"^---\nid: agent-wizard\nname: agent-wizard\ndescription: .+\n---",
        )

    def test_description_covers_positive_trigger_branches(self) -> None:
        description = SKILL.split("description: ", 1)[1].split("\n", 1)[0]
        for needle in ("从零设计 SKILL.md", "生成或更新 AGENTS.md", "评审", "诊断"):
            self.assertIn(needle, description)


class RoutingContract(unittest.TestCase):
    def test_three_routes_have_completion_criteria(self) -> None:
        for route in ("`skill`", "`instructions`", "`review`"):
            self.assertIn(f"| {route} |", SKILL)
        self.assertIn("完成标志", SKILL)

    def test_existing_skill_changes_use_skill_upgrader(self) -> None:
        self.assertIn("已有 Skill 的正文或配套修改交给 `skill-upgrader`", SKILL)
        self.assertIn("从零创建和只读评审", SKILL)

    def test_main_file_links_each_route_directly(self) -> None:
        links = re.findall(r"\]\((references/[^)]+)\)", SKILL)
        self.assertEqual(
            set(links),
            {
                "references/skill-authoring.md",
                "references/agents-md.md",
                "references/review.md",
            },
        )
        for link in links:
            self.assertTrue((SKILL_ROOT / link).is_file(), link)


class CommonWorkflowContract(unittest.TestCase):
    def test_evidence_and_information_placement_are_required(self) -> None:
        for needle in (
            "收集最小证据",
            "关键行为均有来源",
            "选择信息落点",
            "每项内容只有一个权威落点",
        ):
            self.assertIn(needle, SKILL)

    def test_verification_reports_unrun_behavior_checks(self) -> None:
        self.assertIn("每项验收标准都有通过证据或明确的未通过原因", SKILL)
        self.assertIn("不用文本评审冒充行为验证", SKILL)

    def test_writing_preserves_unrelated_content(self) -> None:
        self.assertIn("写入前说明目标文件与变更范围", SKILL)
        self.assertIn("保留无关内容", SKILL)


class SkillAuthoringContract(unittest.TestCase):
    def test_real_experience_drives_the_draft(self) -> None:
        self.assertIn("真实任务中的有效步骤和用户纠正", SKILL_AUTHORING)
        self.assertIn("标为待验证假设", SKILL_AUTHORING)

    def test_structure_starts_minimal(self) -> None:
        self.assertIn("只创建已有内容的文件和目录", SKILL_AUTHORING)
        self.assertIn("一次性操作保留为指令", SKILL_AUTHORING)

    def test_cases_cover_core_boundary_and_near_miss(self) -> None:
        for needle in ("一个核心场景", "一个边界或变体场景", "一个近似场景"):
            self.assertIn(needle, SKILL_AUTHORING)
        self.assertIn("使用 Skill 与未使用 Skill", SKILL_AUTHORING)
        self.assertIn("尚未独立执行行为案例", SKILL_AUTHORING)


class AgentsMdContract(unittest.TestCase):
    def test_scope_and_repository_facts_are_checked(self) -> None:
        self.assertIn("确认目标运行时的发现与覆盖规则", AGENTS_MD)
        self.assertIn("命令必须来自可定位的来源", AGENTS_MD)
        self.assertIn("根文件保留通用约定，嵌套文件只写局部差异", AGENTS_MD)

    def test_related_commands_are_executed_or_reported(self) -> None:
        self.assertIn("运行与本次改动相关的安全本地命令", AGENTS_MD)
        self.assertIn("无法执行的命令已注明原因和剩余风险", AGENTS_MD)


class ReviewContract(unittest.TestCase):
    def test_review_is_read_only_and_evidence_based(self) -> None:
        self.assertIn("评审保持只读", REVIEW)
        for needle in ("**事实**", "**推断**", "**未知**"):
            self.assertIn(needle, REVIEW)

    def test_findings_are_actionable_and_locatable(self) -> None:
        for needle in ("位置：<文件>:<行或章节>", "影响：", "建议："):
            self.assertIn(needle, REVIEW)
        self.assertIn("已有 Skill 交给 `skill-upgrader`", REVIEW)


if __name__ == "__main__":
    unittest.main()
