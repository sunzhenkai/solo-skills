"""观感验收：goal 自迭代、human 给用户看图；方向卡、取证与评审手册来自 pretty-ui。"""
from __future__ import annotations
import re
import unittest
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "references"
DONE = (REF / "done.md").read_text(encoding="utf-8")
UI = (REF / "ui-delivery.md").read_text(encoding="utf-8")


class AestheticGoalTest(unittest.TestCase):
    def test_section_present(self) -> None:
        self.assertIn("## 观感验收", DONE)

    def test_direction_path(self) -> None:
        self.assertIn("pretty-ui/references/direction.md", DONE)
        self.assertIn("轻量方向卡", DONE)

    def test_review_follows_pretty_ui_critique(self) -> None:
        self.assertIn("pretty-ui/references/critique.md", DONE)
        self.assertIn("问题带规则号，P0 / P1 即观感 Blocker / Major", DONE)

    def test_goal_vs_human(self) -> None:
        self.assertIn("goal：不停下问人", DONE)
        self.assertIn("human：", DONE)
        self.assertIn("用户说可以才算完成", DONE)

    def test_screenshot_and_demo_data(self) -> None:
        self.assertIn("演示数据", DONE)
        self.assertIn("改前 / 改后", DONE)

    def test_active_instance_content_from_pretty_ui(self) -> None:
        self.assertIn("pretty-ui/references/system.md", UI)
        self.assertIn("two-pass", UI)

    def test_pretty_ui_links_resolve(self) -> None:
        for name, text in (("done.md", DONE), ("ui-delivery.md", UI)):
            for target in re.findall(r"\]\((\.\./\.\./pretty-ui/[^)#]+)\)", text):
                self.assertTrue((REF / target).resolve().is_file(), f"{name} → {target}")


if __name__ == "__main__":
    unittest.main()
