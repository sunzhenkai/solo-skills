"""Skill 加载器递归扫描 SKILL.md：根目录以外的 SKILL.md 会被重复注册成 Skill。

进化快照用 SKILL.md.candidate，内置子参考用 REFERENCE.md。
"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / "skills"


class TestNoNestedSkillMd(unittest.TestCase):
    def test_only_skill_root_has_skill_md(self) -> None:
        nested = sorted(
            str(p.relative_to(SKILLS))
            for p in SKILLS.glob("*/**/SKILL.md")
            if p.parent.parent != SKILLS
        )
        self.assertEqual(nested, [], "Skill 根目录以外不得有 SKILL.md：快照改名 SKILL.md.candidate，子参考改名 REFERENCE.md")


if __name__ == "__main__":
    unittest.main()
