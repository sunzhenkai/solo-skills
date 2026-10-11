"""role-based-reviewer 契约（20261011 轮）：输出绑定产物状态、findings 编号与未覆盖降级建议。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestStructuredBoundaryContract(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_gate_one_lists_gate_pack_and_runtime_evidence(self) -> None:
        self.assertIn("命中交付类别门包时的门包与运行态证据", self.text)

    def test_missing_boundary_not_grounds_for_refusal(self) -> None:
        self.assertIn("边界缺项（含门包缺失、运行态证据缺失）不构成拒审理由", self.text)
        self.assertIn("不得把缺项当通过", self.text)

    def test_input_accepts_artifact_state(self) -> None:
        self.assertIn("- `产物状态`：`mode=review` 时由调用方给出所审产物的状态标识", self.text)
        self.assertIn("报告与 findings 只对该状态有效", self.text)


class TestOutputContract(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.brief = (ROOT / "references" / "brief-protocol.md").read_text(encoding="utf-8")

    def test_skill_requires_binding_state_line(self) -> None:
        self.assertIn("依据状态：所审产物的状态标识（提交号 / dirty 摘要）与审阅边界齐备性", self.text)

    def test_skill_requires_stable_ids(self) -> None:
        self.assertIn("Blocker / Major 带稳定编号（供调用方处置台账引用）", self.text)

    def test_skill_forbids_claiming_convergence(self) -> None:
        self.assertIn("findings 的处置（`fixed` / `accepted-recorded`）由调用方记录，本 skill 不代替调用方判收敛", self.text)

    def test_brief_has_binding_state_section(self) -> None:
        self.assertIn("## 依据状态", self.brief)
        self.assertIn("审阅边界齐备性", self.brief)

    def test_brief_findings_numbered(self) -> None:
        self.assertIn("- F-1 [角色] 问题描述", self.brief)

    def test_brief_uncovered_becomes_downgrade_advice(self) -> None:
        self.assertIn("## 未覆盖项与降级建议", self.brief)
        self.assertIn("建议处置（按调用方的「未覆盖即降级」登记，含 A/B 定级）", self.brief)

    def test_brief_field_conventions(self) -> None:
        for kept in ("**状态绑定**", "**编号稳定**", "**缺项不担保**"):
            self.assertIn(kept, self.brief)

    def test_existing_conventions_intact(self) -> None:
        for kept in (
            "**结论绑定**：每条 finding MUST 有 `path:line`",
            "**建议而非执行**",
            "**无问题就说无**",
            "**默认不报毛刺**",
        ):
            self.assertIn(kept, self.brief)


class TestTriggerAndGatesIntact(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_gates_kept(self) -> None:
        for kept in ("三道门禁", "收窄触发", "角色确认", "发现克制", "默认只开 **engineer**"):
            self.assertIn(kept, self.text)

    def test_no_silent_downgrade_rule_kept(self) -> None:
        self.assertIn("禁止静默降级为同源自审", self.text)

    def test_roles_enum_kept(self) -> None:
        for role in ("engineer", "design", "product", "sre", "skill"):
            self.assertIn(f"`{role}`", self.text)


if __name__ == "__main__":
    unittest.main()
