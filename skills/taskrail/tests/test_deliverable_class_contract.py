"""taskrail 契约（20261011 轮）：交付类别与门包随 wizard 定稿、完成门机械核对。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestWizardDeliverableClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.wizard = (ROOT / "references" / "phase-wizard.md").read_text(encoding="utf-8")

    def test_phase_action_carries_gate_pack(self) -> None:
        self.assertIn("落 `wizard/plan.md`（含交付类别与适用门包；Web UI 另含 Active Instance 状态）", self.skill)

    def test_principle_present(self) -> None:
        self.assertIn("**交付类别必判**", self.wizard)
        self.assertIn("](gate-packs.md)", self.wizard)

    def test_external_reference_forbidden_as_acceptance(self) -> None:
        self.assertIn("验收方式禁止写「对照外部产品或参考实现」", self.wizard)

    def test_template_section(self) -> None:
        self.assertIn("## 交付类别与门包", self.wizard)
        for field in ("- 交付类别：", "- 适用门包：", "- 基准物：", "- 未覆盖即降级："):
            self.assertIn(field, self.wizard)

    def test_active_instance_section(self) -> None:
        self.assertIn("**Web UI → Active Instance 前置**", self.wizard)
        self.assertIn("## Active Instance（仅 Web UI；其它类别写「不适用」）", self.wizard)
        for field in ("- 状态：", "- 根路径：", "- contract digest：", "- binding digest：", "- projection digest：", "- 前置动作："):
            self.assertIn(field, self.wizard)
        self.assertNotIn("ui-template-", self.wizard)
        self.assertIn("design 阶段建立 Active Instance 至 freeze", self.wizard)

    def test_template_keeps_existing_sections(self) -> None:
        for kept in ("## 完成判据", "## 交付标准", "## 质量属性", "## 流程总览", "## 建议路由"):
            self.assertIn(kept, self.wizard)


class TestCompletionGateMechanical(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_gate_pack_item(self) -> None:
        self.assertIn("5. 命中交付类别门包时", self.skill)
        self.assertIn("](references/gate-packs.md)", self.skill)
        self.assertIn("未覆盖条目均已按「[references/confirm-protocol.md](references/confirm-protocol.md) 未覆盖即降级」登记", self.skill)

    def test_disposition_item(self) -> None:
        self.assertIn("6. 各轮评审的 Blocker / Major 全有 disposition", self.skill)
        self.assertIn("`accepted-recorded` 含理由", self.skill)

    def test_web_ui_digest_done_gate(self) -> None:
        self.assertIn("7. Web UI（按档", self.skill)
        self.assertIn("**medium / complex** 须 digest 与仓库 freeze 一致", self.skill)
        self.assertIn("未跑须登记 B 类显式降级", self.skill)

    def test_mechanical_wording(self) -> None:
        self.assertIn("完成门**逐条机械核对**", self.skill)
        self.assertIn("任一条缺证据即不标 `done`", self.skill)

    def test_existing_gate_items_intact(self) -> None:
        for kept in (
            "1. 完成判据成立（`criterion` 原文）。",
            "2. 交付标准全过（方案写「无」则只看判据）。",
            "3. 相关 checkbox 全勾（含 simple 单切片）。",
            "4. 复杂：质量画像字段齐全；显式降级无 `pending`、无未追认的 `provisional`。",
        ):
            self.assertIn(kept, self.skill)

    def test_not_done_rule_intact(self) -> None:
        self.assertIn("`handed-off`、propose 完、checkbox 全勾但判据不成立 → **不**标 done。", self.skill)


class TestContractPayload(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")

    def test_plan_carries_class(self) -> None:
        self.assertIn("有交付产出时含交付类别与适用门包节", self.contract)

    def test_design_carries_contract_file(self) -> None:
        self.assertIn("**契约文件指针**（仓库内已冻结的共享面契约）与证据计划", self.contract)

    def test_web_ui_active_instance_in_contract(self) -> None:
        self.assertIn("**Web UI**：共享面契约 = 交付项目根 `design-system/v1`", self.contract)
        self.assertIn("Web UI 指针必须含 Active Instance 根路径与三条 digest", self.contract)
        self.assertIn("simple 无 freeze 仅当 adopt-only + 已确认显式降级", self.contract)
        self.assertNotIn("ui-template-", self.contract)
        self.assertIn("Web UI 不依赖仓外 skill", self.contract)

    def test_approve_and_propose_carry_gate_pack(self) -> None:
        self.assertIn("命中门包时另附交付类别、适用门包与基准物", self.contract)
        self.assertIn("命中门包时门包与契约文件指针一并进 driver", self.contract)

    def test_design_dir_artifacts(self) -> None:
        self.assertIn("`design/` 落**契约文件指针**", self.contract)

    def test_existing_payload_rows_intact(self) -> None:
        for kept in (
            "| apply | driver `tasks.md` 已由 propose 产出 |",
            "| archive（探索侧） | 用户确认关闭；子任务均已结 |",
            "`status: handed-off` 与 `driver` 已写入",
        ):
            self.assertIn(kept, self.contract)

    def test_phase_enum_untouched(self) -> None:
        self.assertIn(
            "phase: wizard | explore | design | approve | propose | apply | archive | done",
            self.contract,
        )


if __name__ == "__main__":
    unittest.main()
