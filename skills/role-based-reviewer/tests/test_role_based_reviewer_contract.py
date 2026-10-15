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
            "skill",
            "intent",
        ):
            self.assertIn(f"`{role}`", self.text)


class TestRoleFilesStructure(unittest.TestCase):
    """加厚角色：判据 + 不算问题 + redirect（第一批 engineer/qa/product，第二批 algo/data/sre/ops/biz/design，第三批 skill）。"""

    THICKENED_FULL = ("engineer", "qa", "product", "algo", "data", "sre", "ops", "biz", "skill", "intent")

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

    def test_design_has_speed_scope_section(self) -> None:
        text = read("references/roles/design.md")
        self.assertIn("## 调用范围与速度", text)
        self.assertIn("何时只扫 floor（保速度）", text)
        self.assertIn("tier=simple", text)

    def test_design_has_ceiling_reference_section(self) -> None:
        text = read("references/roles/design.md")
        self.assertIn("## 天花板参照集", text)
        self.assertIn("不受下面「不算问题」节", text)

    def test_design_has_not_a_problem_section(self) -> None:
        # design 已有完整判据清单，第二批只补「不算问题」小节。
        text = read("references/roles/design.md")
        self.assertIn("## 不算问题", text)
        self.assertIn("## 跨角色 redirect", text)

    def test_engineer_checks_structure_rationale(self) -> None:
        text = read("references/roles/engineer.md")
        self.assertIn("结构选择的依据", text)
        self.assertIn("具体变化点或重复点", text)
        self.assertIn("模式命名", text)


class TestRedirectSingleSource(unittest.TestCase):
    """角色文件的「跨角色 redirect」只留指针，边界表唯一真源在 constraints.md。"""

    def test_roles_point_to_constraints(self) -> None:
        table = read("references/protocol.md")
        for f in sorted((ROOT / "references" / "roles").glob("*.md")):
            text = f.read_text(encoding="utf-8")
            sec = text.split("## 跨角色 redirect", 1)[1].split("\n## ", 1)[0]
            self.assertNotIn("↔", sec, f.name)
            self.assertIn("](../protocol.md)", sec, f.name)
            self.assertRegex(table, rf"\| (\w+ ↔ {f.stem}|{f.stem} ↔ \w+) \|", f.name)


class TestIntentRole(unittest.TestCase):
    def test_intent_role_contract(self) -> None:
        text = read("references/roles/intent.md")
        for s in ("用户原话", "无 🔴/🟡 即通过", "上下文不支撑做法", "不参与视角推断"):
            self.assertIn(s, text)
        self.assertIn("intent ↔ product", read("references/protocol.md"))


class TestIntentNarrowingCheck(unittest.TestCase):
    def test_intent_role_flags_added_constraints(self) -> None:
        text = read("references/roles/intent.md")
        self.assertIn("自加限制或缩窄目标", text)

if __name__ == "__main__":
    unittest.main()
