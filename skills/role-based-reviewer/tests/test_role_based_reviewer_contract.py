"""role-based-reviewer：三道门、intent 指针、design 速度节。"""
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

    def test_intent_is_pointer(self) -> None:
        intent = (ROOT / "references" / "roles" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("task-intent/references/intent.md", intent)
        self.assertIn("第 5 节", intent)
        self.assertNotIn("自加限制或缩窄目标", intent)  # 清单已下沉

    def test_design_speed_section(self) -> None:
        text = (ROOT / "references" / "roles" / "design.md").read_text(encoding="utf-8")
        self.assertIn("## 调用范围与速度", text)
        self.assertNotIn("tier=simple", text)

    def test_no_silent_downgrade(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不静默改成同源自审", text)

    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)


if __name__ == "__main__":
    unittest.main()
