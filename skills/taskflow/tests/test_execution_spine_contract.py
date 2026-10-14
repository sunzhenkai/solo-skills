"""taskflow 契约（20261011 执行段脊梁轮）：契约前置、旗舰先行、增量评审、机械收尾。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def skill_corpus(root: Path) -> str:
    """SKILL.md 正文 + references/*.md：细则下沉到 references 后，文本契约按整个 skill 校核。"""
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    parts += [p.read_text(encoding="utf-8") for p in sorted((root / "references").glob("*.md"))]
    return "\n".join(parts)



class TestImplementerInputCarriesSpine(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = skill_corpus(ROOT)

    def test_gate_pack_reference(self) -> None:
        self.assertIn("../taskrail/references/gate-packs.md", self.text)

    def test_three_items_required(self) -> None:
        self.assertIn("MUST 再携带三件，缺任一件不得派发", self.text)
        for item in ("**契约文件**", "**门包**", "**证据要求**"):
            self.assertIn(item, self.text)

    def test_evidence_binding(self) -> None:
        self.assertIn("绑定产物状态（提交号或 dirty 摘要）", self.text)

    def test_web_ui_apply_delegation(self) -> None:
        self.assertIn("## Web UI 实现委托", self.text)
        self.assertNotIn("ui-template-", self.text)
        self.assertIn("无 Active Instance 且无已确认 adopt-only 降级时，先建立 Active Instance 再写页面", self.text)
        self.assertIn("先按代表页 two-pass 方法", self.text)
        self.assertIn("实现并修订一条主流程代表页", self.text)
        self.assertIn("回 design 阶段修订 Active Instance 并重新 freeze", self.text)

    def test_ui_slice_skeleton_mentions_apply(self) -> None:
        self.assertIn("`{task}-ui`：Web UI 切片消费 frozen Active Instance", self.text)


class TestParallelPreconditions(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = skill_corpus(ROOT)

    def test_flagship_first(self) -> None:
        self.assertIn("**旗舰先行**", self.text)
        self.assertIn("经门包「必载专家能力」评审通过后才允许并行铺开", self.text)
        self.assertIn("无样板可循", self.text)

    def test_repeated_failure_escalation(self) -> None:
        self.assertIn("**同类失败升级**", self.text)
        self.assertIn("≥2 个单元报告同一类失败", self.text)
        self.assertIn("契约或计划缺陷", self.text)


class TestClosingReconciliation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = skill_corpus(ROOT)

    def test_section_present(self) -> None:
        self.assertIn("## 收尾机械校核", self.text)

    def test_checks_present(self) -> None:
        for check in (
            "driver 对应实施 checkbox 与子 change 状态一致",
            "显式降级表无 `pending`、无未追认 `provisional`",
            "disposition（`fixed` 或 `accepted-recorded` 含理由）",
        ):
            self.assertIn(check, self.text)

    def test_yes_flag_forbidden(self) -> None:
        self.assertIn("**禁止 `--yes` 掩盖未勾**", self.text)
        self.assertIn("归档后记录不可回改", self.text)

    def test_skeleton_gate_added(self) -> None:
        self.assertIn("3.4 归档前置校核", self.text)
        self.assertIn("3.5 归档全部子 change", self.text)

    def test_existing_skeleton_items_intact(self) -> None:
        for kept in ("3.1 全仓回归与静态检查", "3.2 回填 proposal 验收标准", "3.3 提交交付仓改动"):
            self.assertIn(kept, self.text)


class TestQualityLoopSpine(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.loop = (ROOT / "references" / "delivery-quality-loop.md").read_text(encoding="utf-8")

    def test_contract_first(self) -> None:
        self.assertIn("**契约前置**", self.loop)
        self.assertIn("并行派发只允许发生在契约冻结之后", self.loop)
        self.assertIn("design-system/v1", self.loop)
        self.assertNotIn("ui-template-", self.loop)

    def test_flagship_slice(self) -> None:
        self.assertIn("**旗舰切片**", self.loop)
        self.assertIn("../../taskrail/references/gate-packs.md", self.loop)
        self.assertIn("`ui_evidence_check` report + Gallery", self.loop)

    def test_gate_pack_overlay(self) -> None:
        self.assertIn("**门包叠加**", self.loop)

    def test_incremental_review(self) -> None:
        self.assertIn("## 增量评审", self.loop)
        self.assertIn("无 disposition 的 findings 不得判收敛", self.loop)

    def test_evidence_contract(self) -> None:
        for item in ("**状态绑定**", "**覆盖边界**", "**工具不可用**"):
            self.assertIn(item, self.loop)

    def test_existing_layers_intact(self) -> None:
        for kept in ("| 静态门 |", "| 窄切片 |", "| 全链路 |", "## 失败三分类", "## 只重跑受影响切片"):
            self.assertIn(kept, self.loop)


class TestRubricExecutorBinding(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.rubric = (ROOT / "references" / "acceptance-rubric.md").read_text(encoding="utf-8")

    def test_reviewer_required(self) -> None:
        self.assertIn("打分 MUST 经 `role-based-reviewer`", self.rubric)
        self.assertIn("评审降级未记录", self.rubric)

    def test_roles_from_gate_packs(self) -> None:
        self.assertIn("../../taskrail/references/gate-packs.md", self.rubric)
        self.assertIn("不得少于该表「必载评审」", self.rubric)

    def test_gate_failure_caps_score(self) -> None:
        self.assertIn("**可自动化门**任一失败 → 对应维度不得 ≥2.5", self.rubric)

    def test_web_ui_evidence_binding(self) -> None:
        self.assertIn("scan_design_constraints", self.rubric)
        self.assertIn("`ui_evidence_check` current-build", self.rubric)
        self.assertIn("Gallery", self.rubric)

    def test_uncovered_counts_as_downgrade(self) -> None:
        self.assertIn("**未覆盖条目**按显式降级计", self.rubric)

    def test_heterogeneous_review(self) -> None:
        self.assertIn("SHOULD 异源", self.rubric)

    def test_existing_pass_line_intact(self) -> None:
        self.assertIn("五维均 ≥2", self.rubric)
        self.assertIn("UI/UX 六子项均值 ≥2.5", self.rubric)


if __name__ == "__main__":
    unittest.main()
