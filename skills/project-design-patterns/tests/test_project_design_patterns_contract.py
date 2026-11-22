"""project-design-patterns 的文本契约测试：模式库结构、索引与沉淀规则。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
PATTERN = (ROOT / "references" / "agent-api-access.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_fields(self) -> None:
        self.assertIn("id: project-design-patterns", SKILL)
        self.assertIn("name: project-design-patterns", SKILL)
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

    def test_ops_skill_named(self) -> None:
        """操作规范按名指向 agent-api-ops，含安装命令。"""
        self.assertIn("agent-api-ops", PATTERN)
        self.assertIn("npx skills add sunzhenkai/solo-skills -s agent-api-ops -g -y", PATTERN)

    def test_key_boundary(self) -> None:
        self.assertIn("Key 不能管理凭证与登出", PATTERN)
        self.assertIn("明文", PATTERN)

    def test_deposit_rule(self) -> None:
        """沉淀门槛：至少两处独立落地或一次落地 + 一次明确复用意图。"""
        self.assertIn("至少两处独立落地", SKILL)


class SizeContract(unittest.TestCase):
    def test_skill_md_under_8kb(self) -> None:
        self.assertLess(len(SKILL.encode("utf-8")), 8 * 1024, "SKILL.md 超过 check-style 的 8KB 上限")


if __name__ == "__main__":
    unittest.main()
