"""观感验收：goal 自迭代、human 给用户看图；方向卡、取证与评审手册来自 pretty-ui（可选跨 skill 锚点）。"""
from __future__ import annotations
import re
import unittest
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "references"
SKILLS = Path(__file__).resolve().parents[2]
DONE = (REF / "done.md").read_text(encoding="utf-8")
UI = (REF / "ui-delivery.md").read_text(encoding="utf-8")
CONFIRM = (REF / "confirm-protocol.md").read_text(encoding="utf-8")


class AestheticGoalTest(unittest.TestCase):
    def test_section_present(self) -> None:
        self.assertIn("## 观感验收", DONE)

    def test_direction_path(self) -> None:
        self.assertIn("`pretty-ui/references/direction.md`", DONE)
        self.assertIn("轻量方向卡", DONE)

    def test_light_card_from_pretty_ui_skill(self) -> None:
        self.assertIn("`pretty-ui/SKILL.md`", DONE)
        self.assertIn("「轻量方向卡」", DONE)

    def test_evidence_and_single_stop_rule(self) -> None:
        self.assertIn("`pretty-ui/references/evidence.md`", DONE)
        self.assertIn("critique.md", DONE)
        self.assertIn("「迭代与停止」", DONE)
        self.assertIn("「迭代与停止」为准", CONFIRM)

    def test_review_follows_pretty_ui_critique(self) -> None:
        self.assertIn("`pretty-ui/references/critique.md`", DONE)
        self.assertIn("问题带规则号，P0 / P1 即观感 Blocker / Major", DONE)

    def test_goal_vs_human(self) -> None:
        self.assertIn("goal：不停下问人", DONE)
        self.assertIn("human：", DONE)
        self.assertIn("用户说可以才算完成", DONE)

    def test_screenshot_and_demo_data(self) -> None:
        self.assertIn("演示数据", DONE)
        self.assertIn("改前 / 改后", DONE)

    def test_active_instance_content_from_pretty_ui(self) -> None:
        self.assertIn("`pretty-ui/references/system.md`", UI)
        self.assertIn("two-pass", UI)

    def test_ui_kit_selects_route_before_implementation(self) -> None:
        self.assertIn("`ui-kit/SKILL.md`", UI)
        self.assertTrue((SKILLS / "ui-kit/SKILL.md").is_file())
        for phrase in ("既有/非 React", "ui-template lock", "像素保真", "无（ui-template）"):
            self.assertIn(phrase, UI)

    def test_optional_ui_anchors_exist_without_hard_relative_links(self) -> None:
        for name, text in (("done.md", DONE), ("ui-delivery.md", UI), ("confirm-protocol.md", CONFIRM)):
            self.assertNotRegex(text, r"\]\(\.\./\.\./(?:pretty-ui|ui-kit)/", f"{name} 不应保留跨 skill 相对硬链接")
            for target in re.findall(r"`((?:pretty-ui|ui-kit)/(?:SKILL\.md|references/[A-Za-z0-9_.-]+\.md))`", text):
                self.assertTrue((SKILLS / target).is_file(), f"{name} -> {target}")


if __name__ == "__main__":
    unittest.main()
