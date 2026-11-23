"""role-based-reviewer：三道门、意图审不在本 skill、design 速度节与视觉规则号。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RbrContractTest(unittest.TestCase):
    def test_three_gates(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## 三道门", text)
        self.assertIn("触发要窄", text)
        self.assertIn("角色要少", text)
        self.assertIn("发现要克制", text)

    def test_default_engineer(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("只开 `engineer`", text)

    def test_no_intent_role(self) -> None:
        # 意图代审由 taskrail confirm-protocol 派异源模型按 taskrail intent.md 清单做，不经本 skill 的角色
        self.assertFalse((ROOT / "references" / "roles" / "intent.md").exists())
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("`intent`", text)

    def test_design_speed_section(self) -> None:
        text = (ROOT / "references" / "roles" / "design.md").read_text(encoding="utf-8")
        self.assertIn("## 调用范围与速度", text)
        self.assertNotIn("tier=simple", text)

    def test_design_visual_rule_ids(self) -> None:
        roles = ROOT / "references" / "roles"
        text = (roles / "design.md").read_text(encoding="utf-8")
        self.assertIn("`pretty-ui/references/rules.md`", text)
        self.assertNotIn("../../../pretty-ui/", text)
        self.assertIn("级别仍按本清单", text)
        self.assertIn("X 组（X1–X12）", text)
        self.assertTrue((ROOT.parent / "pretty-ui/references/rules.md").is_file())

    def test_design_visual_rework_returns_to_ui_kit(self) -> None:
        roles = ROOT / "references" / "roles"
        text = (roles / "design.md").read_text(encoding="utf-8")
        self.assertIn("`ui-kit/SKILL.md`", text)
        self.assertNotIn("../../../ui-kit/", text)
        self.assertIn("通用路线由 pretty-ui 承接", text)
        self.assertIn("模板路线沿用 ui-template 契约", text)
        self.assertTrue((ROOT.parent / "ui-kit/SKILL.md").is_file())

    def test_adjacent_skill_boundaries(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("solo-code-review", text)
        self.assertIn("role-chat", text)

    def test_no_silent_downgrade(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不静默改成同源自审", text)

    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)

    def test_skill_role_follows_repo_description_convention(self) -> None:
        text = (ROOT / "references" / "roles" / "skill.md").read_text(encoding="utf-8")
        self.assertIn("description 应是正向的 WHAT + WHEN", text)
        self.assertIn("与相邻 skill 的边界写在正文一句", text)
        self.assertIn("high / medium / low 依次对应这三级", text)
        self.assertIn("`agent-docs-writer` → 从零新建 skill", text)
        self.assertNotIn("何时不用", text)


if __name__ == "__main__":
    unittest.main()
