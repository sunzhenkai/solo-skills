"""project-patterns 的文本契约测试：模式库结构、索引与沉淀规则。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
PATTERN = (ROOT / "references" / "agent-api-access.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_fields(self) -> None:
        self.assertIn("id: project-patterns", SKILL)
        self.assertIn("name: project-patterns", SKILL)
        self.assertTrue(SKILL.lstrip().startswith("---"), "SKILL.md 须以 YAML frontmatter 开头")

    def test_versioned(self) -> None:
        self.assertRegex(SKILL, r"(?m)^version: \d+\.\d+\.\d+$")

    def test_description_positive(self) -> None:
        """description 只写正向 WHAT+WHEN，关键词前置。"""
        desc_line = next(l for l in SKILL.splitlines() if l.startswith("description:"))
        self.assertIn("设计模式", desc_line)
        self.assertIn("agent 数据接入", desc_line)


class StructureContract(unittest.TestCase):
    def test_pattern_card_link_registered(self) -> None:
        """索引表登记模式卡链接；链接目标存在。"""
        self.assertIn("references/agent-api-access.md", SKILL)
        self.assertTrue((ROOT / "references" / "agent-api-access.md").is_file())

    def test_card_sections(self) -> None:
        """模式卡含动机 / 参与者 / 落地件 / 边界 / 先例 / 更正记录。"""
        for section in ["## 动机", "## 参与者", "## 落地件", "## 边界", "## 先例", "## 更正记录"]:
            self.assertIn(section, PATTERN, f"模式卡缺少 {section}")

    def test_ops_reference_named(self) -> None:
        """操作规范是同 skill 的引用件，SKILL.md 直链，安装/升级走 project-patterns。"""
        self.assertIn("references/agent-api-ops.md", SKILL)
        self.assertTrue((ROOT / "references" / "agent-api-ops.md").is_file())
        self.assertIn("npx skills add sunzhenkai/solo-skills -s project-patterns -g -y", PATTERN)
        self.assertNotIn("-s agent-api-ops", PATTERN)

    def test_key_boundary(self) -> None:
        self.assertIn("Key 不能管理凭证与登出", PATTERN)
        self.assertIn("明文", PATTERN)

    def test_deposit_rule(self) -> None:
        """沉淀门槛：至少两处独立落地或一次落地 + 一次明确复用意图。"""
        self.assertIn("至少两处独立落地", SKILL)

    def test_model_provider_pattern_registered(self) -> None:
        """模型供应商管理模式卡与实现 prompt 均已直链登记，且含标准章节与联动约束。"""
        self.assertIn("references/model-provider-management.md", SKILL)
        self.assertIn("references/model-provider-impl-prompt.md", SKILL)
        card_path = ROOT / "references" / "model-provider-management.md"
        prompt_path = ROOT / "references" / "model-provider-impl-prompt.md"
        self.assertTrue(card_path.is_file())
        self.assertTrue(prompt_path.is_file())
        card = card_path.read_text(encoding="utf-8")
        prompt = prompt_path.read_text(encoding="utf-8")
        for section in ["## 动机", "## 参与者", "## 落地件", "## 边界", "## 先例", "## 更正记录"]:
            self.assertIn(section, card, f"模型供应商模式卡缺少 {section}")
        self.assertIn("models.dev", card)
        self.assertIn("两级联动", card)
        self.assertIn("{{技术栈}}", prompt)
        self.assertIn("验收清单", prompt)

    def test_api_access_stats_pattern_registered(self) -> None:
        """接口访问统计模式卡已直链登记，且含标准章节与核心不变量。"""
        self.assertIn("references/api-access-stats.md", SKILL)
        card_path = ROOT / "references" / "api-access-stats.md"
        self.assertTrue(card_path.is_file())
        card = card_path.read_text(encoding="utf-8")
        for section in ["## 动机", "## 参与者", "## 落地件", "## 多栈适配器对照", "## 边界", "## 先例", "## 更正记录"]:
            self.assertIn(section, card, f"接口访问统计模式卡缺少 {section}")
        for invariant in ["/_unmatched", "2048", "403", "LANOnly", "__invalid__", "API_STATS_ENABLED"]:
            self.assertIn(invariant, card, f"接口访问统计模式卡缺少不变量 {invariant}")
        desc_line = next(l for l in SKILL.splitlines() if l.startswith("description:"))
        self.assertIn("接口访问统计", desc_line)

    def test_agent_friendly_api_pattern_registered(self) -> None:
        """Agent 友好 API 设计模式卡已直链登记，含标准六节与六件套关键词。"""
        self.assertIn("references/agent-friendly-api.md", SKILL)
        card_path = ROOT / "references" / "agent-friendly-api.md"
        self.assertTrue(card_path.is_file())
        card = card_path.read_text(encoding="utf-8")
        for section in ["## 动机", "## 参与者", "## 落地件", "## 边界", "## 先例", "## 更正记录"]:
            self.assertIn(section, card, f"Agent 友好 API 模式卡缺少 {section}")
        for marker in ["乐观锁", "dry_run", "effective_mode", "deny-by-default"]:
            self.assertIn(marker, card)


class SizeContract(unittest.TestCase):
    def test_skill_md_under_8kb(self) -> None:
        self.assertLess(len(SKILL.encode("utf-8")), 8 * 1024, "SKILL.md 超过 check-style 的 8KB 上限")


if __name__ == "__main__":
    unittest.main()
