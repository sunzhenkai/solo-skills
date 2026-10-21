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
        # 意图代审由 taskrail confirm-protocol 派异源模型按 task-intent 清单做，不经本 skill 的角色
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
        self.assertIn("](../../../pretty-ui/references/rules.md)", text)
        self.assertIn("级别仍按本清单", text)
        self.assertIn("X 组（X1–X12）", text)
        self.assertTrue((roles / "../../../pretty-ui/references/rules.md").resolve().is_file())

    def test_no_silent_downgrade(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不静默改成同源自审", text)

    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)


if __name__ == "__main__":
    unittest.main()
