"""task-confirm 契约：双模式确认、审阅与退出点。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.profile = (ROOT / "references" / "quality-profile.md").read_text(
            encoding="utf-8"
        )

    def test_frontmatter(self) -> None:
        self.assertIn("id: task-confirm", self.skill)
        self.assertIn("name: task-confirm", self.skill)
        self.assertEqual(ROOT.name, "task-confirm")

    def test_dual_mode(self) -> None:
        self.assertIn("| human |", self.skill)
        self.assertIn("| goal |", self.skill)
        self.assertIn("不列选项", self.skill)

    def test_trigger_is_single_source(self) -> None:
        self.assertIn("单一真源", self.skill)
        self.assertIn("/goal", self.skill)

    def test_review_severity(self) -> None:
        self.assertIn("**P0**", self.skill)
        self.assertIn("**P1**", self.skill)
        self.assertIn("**P2**", self.skill)

    def test_exit_points(self) -> None:
        for tag in (
            "理解不够",
            "审阅不通过",
            "降级未确认",
            "线上动作",
            "泄密",
            "同一验证连败两次",
        ):
            self.assertIn(tag, self.skill)

    def test_no_orchestration(self) -> None:
        self.assertIn("不定档位", self.skill)
        self.assertIn("不改 `TASK.md.phase`", self.skill)

    def test_quality_profile_present(self) -> None:
        self.assertIn("角色底线", self.profile)
        self.assertIn("显式降级", self.profile)
        self.assertIn("天花板参照集", self.profile)

    def test_auth_section(self) -> None:
        self.assertIn("## 授权", self.skill)

    def test_migrated_assets(self) -> None:
        for rel in (
            "references/suspension.md",
            "references/state-file.md",
            "references/state-machine.md",
            "scripts/goal_transition.py",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
