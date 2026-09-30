"""task-delivery 文本契约：挂起五元组接入、降级 A/B 分级、修复按 finding 连败计数。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class TestPartialSuspend(unittest.TestCase):
    """等用户类停机：五元组呈现 + 只冻结依赖面。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.loop = read("references/loop-protocol.md")

    def test_suspension_reference(self) -> None:
        self.assertIn("task-goal/references/suspension.md", self.loop)
        self.assertIn("task-goal/references/suspension.md", self.skill)
        self.assertTrue(
            (SKILL_ROOT.parent / "task-goal" / "references" / "suspension.md").is_file(),
            "cross-ref target missing",
        )

    def test_freeze_only_dependency_surface(self) -> None:
        self.assertIn("只冻结依赖面", self.loop)
        self.assertIn("环境准备、脚手架、只读取证、与该项无关的切片继续", self.loop)
        self.assertIn("不全局停摆", self.loop)
        self.assertIn("等用户类停机只冻结依赖面", self.skill)

    def test_user_waits_presented_as_five_tuple(self) -> None:
        self.assertIn("挂起五元组", self.loop)
        self.assertIn("异源选择", self.loop)


class TestDowngradeABSync(unittest.TestCase):
    """降级 A/B 分级与真人门追认点。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.loop = read("references/loop-protocol.md")

    def test_stop_condition_split_by_class(self) -> None:
        self.assertIn("A 类 pending 降级未确认", self.loop)
        self.assertIn("B 类经审阅临时确认不停机", self.loop)

    def test_human_gate_is_ratification_point(self) -> None:
        self.assertIn("真人门同时是 B 类降级的集中追认点", self.skill)
        self.assertIn("回滚说明", self.skill)

    def test_decide_freeze_gate(self) -> None:
        self.assertIn("A 类 pending 降级未确认不得冻结，B 类 `provisional` 不阻塞冻结", self.loop)

    def test_full_chain_gate(self) -> None:
        self.assertIn("provisional 已全部追认", self.loop)


class TestRepairLossStreak(unittest.TestCase):
    """Stage 9 修复：按 finding 连败计数，不按轮次封顶。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.loop = read("references/loop-protocol.md")

    def test_per_finding_tracking(self) -> None:
        self.assertIn("修复按 finding 计数，不按轮次封顶", self.loop)
        self.assertIn("已消失 / 仍在 / 新增", self.loop)

    def test_loss_streak_and_deterioration(self) -> None:
        self.assertIn("同一条 P0/P1 连续两轮修复仍「仍在」", self.loop)
        self.assertIn("恶化闸", self.loop)
        self.assertIn("回归账", self.loop)

    def test_no_round_cap_wording(self) -> None:
        self.assertNotIn("每个窄切片最多两轮修复", self.loop)
        self.assertNotIn("同一窄切片两轮修复后仍有 P0/P1", self.loop)
        self.assertNotIn("repairs-per-slice", self.loop)

    def test_budget_semantics_updated(self) -> None:
        self.assertIn("repairs-per-finding<=2", self.loop)

    def test_hard_boundary_synced(self) -> None:
        self.assertIn("同一条 P0/P1 连续两轮修复仍在、或单轮修复新增达恶化闸", self.skill)


class TestBudgetExhaustionRecovery(unittest.TestCase):
    def test_recovery_path_defined(self) -> None:
        loop = read("references/loop-protocol.md")
        self.assertIn("预算耗尽的「下一步」写恢复路径与授权形状", loop)


if __name__ == "__main__":
    unittest.main()
