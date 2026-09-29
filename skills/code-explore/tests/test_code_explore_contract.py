"""code-explore 文本契约：只读边界、安全规则、运行时只读合规、llm-wiki 边界。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_trio(self) -> None:
        self.assertRegex(
            SKILL,
            r"^---\nid: code-explore\nname: code-explore\ndescription: .+\n---",
        )


class EvidenceSafetyRules(unittest.TestCase):
    """「证据与安全规则」八条逐条钉住。"""

    def test_eight_rules_present(self) -> None:
        for needle in (
            "**在检查源代码前优先使用已有知识。**",
            "**采用渐进式披露。**",
            "**让结论有证据支撑。**",
            "**保持探索只读。**",
            "**外部变更必须经过确认。**",
            "**隐去机密信息。**",
            "`<REDACTED>`",
            "**不要过度断言。**",
            "**保护无关工作。**",
        ):
            self.assertIn(needle, SKILL, needle)

    def test_read_only_boundary_statement(self) -> None:
        self.assertIn(
            "探索期间不得修改源代码、配置、基础设施或外部系统", SKILL
        )
        self.assertIn(
            "用户提出“分析”“追踪”“理解”或“审查”请求，并不代表授权编辑源代码。",
            SKILL,
        )


class WriteGateContract(unittest.TestCase):
    def test_write_gate_section(self) -> None:
        self.assertIn(
            "在执行任何 `archive`、`ingest` 或 `project` 写入前", SKILL
        )
        for rule in (
            "说明目标文件和计划中的变更。",
            "当请求存在歧义、具有破坏性或会影响外部系统时，请求确认。",
            "报告最终 diff 或文件列表。",
        ):
            self.assertIn(rule, SKILL, rule)


class StageContract(unittest.TestCase):
    def test_five_stages_with_write_defaults(self) -> None:
        for stage in ("`ask`", "`explore`", "`archive`", "`ingest`", "`project`"):
            self.assertIn(f"| {stage} |", SKILL, stage)
        self.assertEqual(SKILL.count("| 只读 |"), 2, "ask/explore 应为只读")
        self.assertEqual(
            SKILL.count("| 仅在明确请求后写入 |"), 3, "archive/ingest/project 应为明确请求后写入"
        )


class RuntimeReadonlyCompliance(unittest.TestCase):
    """安装镜像是字节复制：正文不得指示向 skill 目录写盘。"""

    def test_experience_backflow_section_exists(self) -> None:
        self.assertIn("## 经验回灌", SKILL)
        self.assertIn("字节复制镜像", SKILL)
        self.assertIn("运行时只读", SKILL)
        self.assertIn("落**工作区**", SKILL)

    def test_no_write_into_skill_dir_instructions(self) -> None:
        for forbidden in (
            "写入 `experience/`",
            "写入 `examples/`",
            "写入 `evals/`",
            "## Self-evolution",
            "## 公共复用清理",
        ):
            self.assertNotIn(forbidden, SKILL, f"不应出现：{forbidden}")

    def test_evolution_via_source_repo_explicit_flow(self) -> None:
        self.assertIn("`skill-evolver`", SKILL)
        self.assertIn("`skill-upgrader`", SKILL)
        self.assertIn("未展示 Proposal 并获用户确认前，不改生产正文。", SKILL)
        self.assertIn("单次失败或单次用户纠正不足以改 skill", SKILL)


class LlmWikiBoundary(unittest.TestCase):
    def test_boundary_declaration(self) -> None:
        self.assertIn("维护知识 wiki 本身", SKILL)
        self.assertIn("已有 llm-wiki 时交给它", SKILL)
