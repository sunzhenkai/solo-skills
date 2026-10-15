"""观感类目标不分档的收口规则：视觉方向、参照集、演示数据、改前改后截图、异源评审；goal 自判迭代，human 给人看截图。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class TestAestheticGoal(unittest.TestCase):
    def setUp(self) -> None:
        self.packs = read("references/gate-packs.md")

    def test_single_source_section(self) -> None:
        self.assertIn("## 审美目标（不分档）", self.packs)
        for phrase in ("视觉方向", "天花板参照集", "演示数据", "改前 / 改后截图", "异源 design 评审"):
            self.assertIn(phrase, self.packs)

    def test_visual_direction_file_exists(self) -> None:
        self.assertIn("pretty-view-html/references/frontend-design/REFERENCE.md", self.packs)
        self.assertTrue((SKILLS / "pretty-view-html/references/frontend-design/REFERENCE.md").is_file())

    def test_goal_iterates_without_asking_human(self) -> None:
        self.assertIn("goal：不停下问人", self.packs)
        self.assertIn("自动迭代", self.packs)
        self.assertIn("没有未解决的观感 Blocker / Major 才算过", self.packs)

    def test_human_confirms_screenshots(self) -> None:
        self.assertIn("human：异源评审通过后，把改前 / 改后截图给用户看", self.packs)

    def test_no_b_class_downgrade(self) -> None:
        self.assertIn("也不能用 B 类降级放行", self.packs)

    def test_pointers(self) -> None:
        self.assertIn("「审美目标」", read("SKILL.md"))
        self.assertIn("「审美目标（不分档）」", read("references/phase-wizard.md"))
        self.assertIn("天花板参照集不分档", read("references/quality-profile.md"))
        self.assertIn("观感任务收尾", read("references/user-report.md"))
        self.assertIn("「审美目标（不分档）」", (SKILLS / "taskflow/SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
