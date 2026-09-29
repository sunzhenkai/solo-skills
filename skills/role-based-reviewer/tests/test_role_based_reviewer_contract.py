"""role-based-reviewer 文本契约：三道门禁与角色文件的「判据 + 不算问题」结构。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class TestGates(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_three_gates_present(self) -> None:
        self.assertIn("三道门禁", self.text)
        self.assertIn("收窄触发", self.text)
        self.assertIn("角色确认", self.text)
        self.assertIn("发现克制", self.text)

    def test_default_engineer_only(self) -> None:
        self.assertIn("默认只开 **engineer**", self.text)

    def test_roles_enum_unchanged(self) -> None:
        for role in (
            "engineer",
            "algo",
            "data",
            "sre",
            "ops",
            "biz",
            "product",
            "design",
            "qa",
        ):
            self.assertIn(f"`{role}`", self.text)


class TestRoleFilesStructure(unittest.TestCase):
    """加厚角色：判据 + 不算问题 + redirect（第一批 engineer/qa/product，第二批 algo/data/sre/ops/biz/design）。"""

    THICKENED_FULL = ("engineer", "qa", "product", "algo", "data", "sre", "ops", "biz")

    def test_thickened_roles_have_criteria(self) -> None:
        for role in self.THICKENED_FULL:
            text = read(f"references/roles/{role}.md")
            self.assertIn("命中判据", text, role)
            self.assertIn("## 不算问题", text, role)
            self.assertIn("## 跨角色 redirect", text, role)
            self.assertIn("## 优先锚点", text, role)

    def test_thickened_roles_keep_level_marks(self) -> None:
        for role in self.THICKENED_FULL:
            text = read(f"references/roles/{role}.md")
            self.assertIn("🔴", text, role)
            self.assertIn("🟡", text, role)

    def test_design_has_not_a_problem_section(self) -> None:
        # design 已有完整判据清单，第二批只补「不算问题」小节。
        text = read("references/roles/design.md")
        self.assertIn("## 不算问题", text)
        self.assertIn("## 跨角色 redirect", text)


if __name__ == "__main__":
    unittest.main()
