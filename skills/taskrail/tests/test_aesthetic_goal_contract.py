"""观感验收：goal 自迭代、human 给用户看图；frontend-design 路径保留。"""
from __future__ import annotations
import unittest
from pathlib import Path

DONE = (Path(__file__).resolve().parents[1] / "references" / "done.md").read_text(encoding="utf-8")


class AestheticGoalTest(unittest.TestCase):
    def test_section_present(self) -> None:
        self.assertIn("## 观感验收", DONE)

    def test_frontend_design_path(self) -> None:
        self.assertIn("pretty-view-html/references/frontend-design/REFERENCE.md", DONE)

    def test_goal_vs_human(self) -> None:
        self.assertIn("goal：不停下问人", DONE)
        self.assertIn("human：", DONE)
        self.assertIn("用户说可以才算完成", DONE)

    def test_screenshot_and_demo_data(self) -> None:
        self.assertIn("演示数据", DONE)
        self.assertIn("改前 / 改后", DONE)


if __name__ == "__main__":
    unittest.main()
