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
        self.assertIn("task-confirm", self.skill)
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
        self.assertIn("propose(单切片)", self.contract)
        self.assertIn("handoff → propose", self.contract)
        self.assertNotIn("可单 change", self.contract)
        self.assertIn("explore(仅 grill)", self.wizard)
        self.assertNotIn("→ 实现", self.wizard)

    def test_non_phase_actions_table(self) -> None:
        self.assertIn("## 非 phase 动作", self.contract)
        self.assertIn("| `grill`", self.contract)
        self.assertIn("| `handoff`", self.contract)
        self.assertIn("| `expand`", self.contract)

    def test_status_phase_matrix(self) -> None:
        self.assertIn("status × phase 合法组合", self.contract)
        self.assertIn("handed-off | propose, apply, archive", self.contract)

    def test_simple_requires_taskflow(self) -> None:
        self.assertIn("### simple 专条", self.contract)
        self.assertIn("必须 `handoff` + taskflow", self.contract)
        self.assertIn("禁止**在 taskrail 路径下无 driver", self.contract)
        self.assertIn("凡经 taskrail 的交付均必需，含 simple", self.skill)


if __name__ == "__main__":
    unittest.main()
