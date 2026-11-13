"""project-explore 文本契约：只读取证、持久化路由、运行时只读合规。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
PHASES = (SKILL_ROOT / "references" / "phases.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_trio(self) -> None:
        self.assertRegex(
            SKILL,
            r"^---\nid: project-explore\nname: project-explore\ndescription: .+\n---",
        )
        self.assertEqual(SKILL_ROOT.name, "project-explore")


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
            "用户提出“分析”“追踪”“理解”或“审查”请求，并不代表授权编辑源代码或持久化文档。",
            SKILL,
        )


class PersistenceRoutingContract(unittest.TestCase):
    def test_all_persistence_stages_handoff_without_writing(self) -> None:
        self.assertEqual(SKILL.count("| 只读；按需交接 |"), 3)
        self.assertIn("本 skill 只取证和路由", SKILL)
        self.assertIn("本阶段生成持久化计划并交接，不直接写文档", PHASES)
        self.assertIn("本阶段不直接创建来源页或业务页", PHASES)
        self.assertIn("不创建独立 profile", PHASES)

    def test_single_writer_and_mixed_order(self) -> None:
        self.assertIn("当前系统说明交给 `project-atlas`", SKILL)
        self.assertIn("决策背景、经验、台账和跨项目知识交给 `wiki-data`", SKILL)
        self.assertIn("混合内容先完成 Atlas，再由 `wiki-data`", SKILL)
        self.assertIn("两个工作区分别遵守各自的写盘确认", SKILL)
        self.assertIn("不在下游 skill 缺失时自行落盘", SKILL)

    def test_no_competing_storage_or_profile_schema(self) -> None:
        self.assertNotIn("KNOWLEDGE_ROOT", SKILL)
        self.assertNotIn("PROJECT_ROOT", SKILL)
        self.assertNotIn("### 最小 profile", PHASES)
        self.assertNotIn("type: code-map", PHASES)


class StageContract(unittest.TestCase):
    def test_five_stages_with_readonly_defaults(self) -> None:
        for stage in ("`ask`", "`explore`", "`archive`", "`ingest`", "`project`"):
            self.assertIn(f"| {stage} |", SKILL, stage)
        self.assertEqual(SKILL.count("| 只读 |"), 2, "ask/explore 应为只读")

    def test_exploration_brief_has_optional_persistence_advice(self) -> None:
        self.assertIn("## 持久化建议", PHASES)
        self.assertIn("它只是交接建议，不触发写入", PHASES)
        for field in ("页面：", "依据：", "主题：", "保存价值：", "不纳入："):
            self.assertIn(field, PHASES)


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
        self.assertIn("`evolve`", SKILL)
        self.assertIn("`skill-upgrader`", SKILL)
        self.assertIn("未展示 Proposal 并获用户确认前，不改生产正文。", SKILL)
        self.assertIn("单次失败或单次用户纠正不足以改 skill", SKILL)


class KnowledgeBoundary(unittest.TestCase):
    def test_atlas_and_wiki_are_execution_owners(self) -> None:
        self.assertIn("`project-atlas`", SKILL)
        self.assertIn("`wiki-data`", SKILL)
        self.assertIn("query 本身不自动更新 Atlas 或 wiki", SKILL)
        self.assertIn("由 project-atlas、wiki-data 或任务台账按职责保存", SKILL)


if __name__ == "__main__":
    unittest.main()
