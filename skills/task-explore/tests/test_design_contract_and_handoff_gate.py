"""task-explore 契约（20261011 轮）：design 落契约指针与证据计划、handoff 前置核对。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestDesignContractArtifact(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.design = (ROOT / "references" / "phase-design.md").read_text(encoding="utf-8")

    def test_gate_requires_contract_and_evidence_plan(self) -> None:
        self.assertIn("**契约文件指针**", self.design)
        self.assertIn("**证据计划**", self.design)
        self.assertIn("缺任一项按缺口停下，不写空心方案", self.design)

    def test_gate_references_gate_packs(self) -> None:
        self.assertIn("../../task-confirm/references/gate-packs.md", self.design)

    def test_output_table_has_contract_row(self) -> None:
        self.assertIn("| `design/contract.md` |", self.design)
        self.assertIn("命中交付类别门包时必需；只存指针，契约本体落交付仓", self.design)

    def test_boundary_no_body_copy(self) -> None:
        self.assertIn("本 skill 只留指针，契约本体落交付仓并由交付仓维护", self.design)

    def test_command_mentions_artifact(self) -> None:
        self.assertIn("本阶段另落 `design/contract.md`", self.skill)

    def test_existing_design_gates_intact(self) -> None:
        for kept in (
            "目标能一句话说清",
            "成功标准可检验",
            "能形成至少两个可行方案",
            "## 画像展开（上游含质量画像时）",
            "不写实现代码，不创建 OpenSpec `tasks.md`",
        ):
            self.assertIn(kept, self.design)


class TestHandoffContractGate(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.handoff = (ROOT / "references" / "phase-handoff.md").read_text(encoding="utf-8")

    def test_gate_five_present(self) -> None:
        self.assertIn("5. 命中交付类别门包时：`design/contract.md` 的契约文件指针与证据计划已就绪", self.handoff)
        self.assertIn("先回 `design` 补，不创建 driver", self.handoff)

    def test_payload_carries_gate_pack_and_pointer(self) -> None:
        self.assertIn("`--goal` 再附交付类别、适用门包与基准物", self.handoff)
        self.assertIn("不把契约本体复制进 `tasks/`", self.handoff)

    def test_command_mentions_gate(self) -> None:
        self.assertIn("交接门禁含：命中交付类别门包时", self.skill)

    def test_existing_gates_intact(self) -> None:
        for kept in (
            "1. 该任务已批准：`approve/APPROVED.md` 存在",
            "2. driver change 名 = 任务 slug + `-driver`",
            "3. 任务已是 `handed-off` 且 driver 已存在",
            "4. 显式降级原文快照里确认状态为 `pending` 的条目为 0",
            "**不要写 `tasks.md`。**",
        ):
            self.assertIn(kept, self.handoff)


if __name__ == "__main__":
    unittest.main()
