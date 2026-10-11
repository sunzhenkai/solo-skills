"""task-confirm 契约（20261011 轮）：评审执行器绑定、门包真源与未覆盖即降级。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestReviewerBinding(unittest.TestCase):
    """评审命中门包必载专家能力时不得静默降级为普通 subagent。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_binding_section_present(self) -> None:
        self.assertIn("**执行器绑定**（防静默降级）", self.skill)

    def test_structured_invocation_required(self) -> None:
        self.assertIn("`mode=review` + 完整 `roles=` + 审阅边界", self.skill)

    def test_silent_downgrade_forbidden(self) -> None:
        self.assertIn("静默降级等同审阅未做", self.skill)
        self.assertIn("不得以图快为由退普通 subagent", self.skill)

    def test_downgrade_must_be_recorded(self) -> None:
        self.assertIn("写明不可用的具体原因", self.skill)
        self.assertIn("**评审降级未记录**", self.skill)

    def test_heterogeneous_review_required(self) -> None:
        self.assertIn("SHOULD 异源", self.skill)
        self.assertIn("`model=` 与实现者不同，或 `endpoint=` 走名册", self.skill)

    def test_runtime_evidence_required_before_design_role(self) -> None:
        self.assertIn("先给运行证据", self.skill)
        self.assertIn("「⚠ 需运行态验证」提示", self.skill)

    def test_three_choice_table_intact(self) -> None:
        """三选一表保留，且 subagent 不再是无条件默认回退。"""
        self.assertIn("评审者三选一（选中即唯一）", self.skill)
        self.assertIn("| role-based-reviewer |", self.skill)
        self.assertIn("| agent-roster |", self.skill)
        self.assertIn("| subagent | 仅在无对应角色", self.skill)


class TestUncoveredBecomesDowngrade(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def test_rule_present(self) -> None:
        self.assertIn("**未覆盖即降级**", self.skill)
        self.assertIn("A 类走「降级未确认」退出点", self.skill)
        self.assertIn("B 类可经审阅记 `provisional`", self.skill)

    def test_no_pass_by_appearance(self) -> None:
        self.assertIn("「未测但看起来没问题」不构成通过", self.skill)


class TestGatePacksSingleSource(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.packs = (ROOT / "references" / "gate-packs.md").read_text(encoding="utf-8")

    def test_linked_from_skill(self) -> None:
        self.assertIn("references/gate-packs.md", self.skill)
        self.assertIn("唯一真源", self.skill)

    def test_external_reference_forbidden_as_baseline(self) -> None:
        self.assertIn("禁止把外部产品或参考实现当验收基准", self.packs)

    def test_classes_covered(self) -> None:
        for cls_name in ("## Web UI", "## 服务 / 后端", "## 数据 / 口径", "## 部署 / 密钥", "## 文档 / Skill"):
            self.assertIn(cls_name, self.packs)

    def test_web_ui_binds_design_role(self) -> None:
        self.assertIn("role-based-reviewer roles=design", self.packs)
        self.assertIn("role-based-reviewer roles=engineer", self.packs)

    def test_web_ui_binds_active_instance(self) -> None:
        self.assertIn("design-system/v1", self.packs)
        self.assertIn("status: frozen", self.packs)
        self.assertIn("contract / binding / projection", self.packs)
        self.assertIn("ui-template-design", self.packs)
        self.assertIn("ui-template-apply", self.packs)

    def test_web_ui_tier_gate(self) -> None:
        self.assertIn("**Active Instance 档位门**", self.packs)
        self.assertIn("medium / complex", self.packs)
        self.assertIn("adopt published package", self.packs)

    def test_web_ui_automations_hook_ds_runtime(self) -> None:
        self.assertIn("check_active_instance.py validate", self.packs)
        self.assertIn("scan_design_constraints.py", self.packs)

    def test_entry_taxonomy(self) -> None:
        self.assertIn("门包条目三分", self.packs)
        self.assertIn("未覆盖即降级", self.packs)

    def test_references_quality_profile_relatively(self) -> None:
        self.assertIn("[quality-profile.md](quality-profile.md)", self.packs)


if __name__ == "__main__":
    unittest.main()
