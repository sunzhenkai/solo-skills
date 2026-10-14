"""taskrail 契约：脊柱入口、阶段、目录与完成门。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.contract = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        cls.wizard = (ROOT / "references" / "phase-wizard.md").read_text(encoding="utf-8")

    def test_frontmatter(self) -> None:
        self.assertIn("id: taskrail", self.skill)
        self.assertIn("name: taskrail", self.skill)
        self.assertEqual(ROOT.name, "taskrail")

    def test_references_exist(self) -> None:
        for rel in (
            "references/contract.md",
            "references/phase-wizard.md",
            "references/external-precedent.md",
            "CONTEXT.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_pipeline_named(self) -> None:
        self.assertIn(
            "wizard → explore(+grill) → design → approve → [handoff] → propose → apply → archive",
            self.contract,
        )
        self.assertIn("confirm_mode: human | goal", self.contract)

    def test_task_dir_layout(self) -> None:
        self.assertIn("wizard/plan.md", self.contract)
        self.assertIn("approve/", self.contract)
        self.assertIn("phase:", self.contract)
        self.assertIn("criterion:", self.contract)

    def test_depends_on_confirm_explore_taskflow(self) -> None:
        self.assertIn("references/confirm-protocol.md", self.skill)
        self.assertIn("task-explore", self.skill)
        self.assertIn("taskflow", self.skill)

    def test_completion_gate(self) -> None:
        self.assertIn("完成门", self.skill)
        self.assertIn("`handed-off`", self.skill)
        self.assertIn("**不**标 done", self.skill)

    def test_wizard_has_criterion_and_tiers(self) -> None:
        self.assertIn("## 完成判据", self.wizard)
        self.assertIn("simple", self.wizard)
        self.assertIn("complex", self.wizard)
        self.assertIn("grilling", self.wizard)

    def test_human_gate_aligns_recommend(self) -> None:
        self.assertIn("列选项（含推荐）", self.contract)
        self.assertIn("空问清单", self.wizard)
        self.assertIn("未决口子须已带推荐再交", self.wizard)

    def test_pipeline_includes_handoff_action(self) -> None:
        self.assertIn("[handoff]", self.contract)
        self.assertIn("handoff = 动作，不是 phase", self.contract)

    def test_tier_paths_aligned(self) -> None:
        self.assertIn("explore(仅 grill)", self.contract)
        self.assertIn("handoff → propose", self.contract)
        self.assertNotIn("可单 change", self.contract)
        self.assertIn("explore(仅 grill)", self.wizard)
        self.assertNotIn("→ 实现", self.wizard)

    def test_non_phase_actions_table(self) -> None:
        self.assertIn("## 非 phase 动作", self.contract)
        self.assertIn("| `grill`", self.contract)
        self.assertIn("| `handoff`", self.contract)
        self.assertIn("| `expand`", self.contract)

    def test_single_ledger(self) -> None:
        self.assertIn("**一本账**", self.contract)
        self.assertNotIn("status × phase 合法组合", self.contract)

    def test_simple_direct_implement(self) -> None:
        self.assertIn("### simple 专条", self.contract)
        self.assertIn("simple **不建 driver、不走 OpenSpec**", self.contract)
        self.assertIn("升档为 medium", self.contract)
        self.assertIn("「验证」节", self.skill)


    def test_flow_overview_anchor_and_quality_attrs(self) -> None:
        self.assertIn("## 质量属性", self.wizard)
        self.assertIn("## 流程总览", self.wizard)
        self.assertIn("流程总览映射", self.contract)
        self.assertIn("流程总览快照随交接进 driver", self.contract)
        self.assertIn("human 含强制走查", self.contract)


    def test_approve_exit_is_handoff(self) -> None:
        self.assertIn("### approve 出口", self.skill)
        self.assertIn("唯一推荐下一步是 `handoff`", self.skill)
        self.assertIn("未决不把推荐改成 archive", self.skill)
        self.assertIn("禁止用当轮叙事改写 `criterion`", self.skill)
        self.assertIn("拒绝进入 archive", self.skill)
        self.assertIn("taskflow 子 change", self.skill)
        self.assertIn("### approve 出口", self.contract)
        self.assertIn("未决不阻断交接", self.contract)
        self.assertIn("taskflow 子 change", self.contract)
        self.assertIn("拒绝进入 archive", self.contract)

    def test_optional_worker_seat(self) -> None:
        self.assertIn("## 执行座位", self.contract)
        self.assertIn("**永不派出**", self.contract)
        self.assertIn("只回简短摘要", self.contract)
        self.assertIn("宿主 subagent", self.contract)
        self.assertIn("不回灌工具轨迹", self.contract)
        self.assertIn("Worker 派出为建议", self.skill)

    def test_wizard_delegates_task_intent(self) -> None:
        self.assertIn("委托 `task-intent`", self.wizard)
        self.assertIn("wizard/intent.md", self.wizard)
        self.assertIn("第 1 步委托 `task-intent`", self.skill)
        self.assertIn("`wizard/intent.md`（`status: confirmed` 或 `assumed`", self.contract)
        self.assertIn("roles=intent", self.wizard)



if __name__ == "__main__":
    unittest.main()
