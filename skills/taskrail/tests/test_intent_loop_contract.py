"""意图闭环：task-intent ↔ taskrail ↔ task-explore ↔ taskflow ↔ role-based-reviewer 的跨 skill 文本契约（审计 10 条缺口）。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]


def r(rel: str) -> str:
    return (SKILLS / rel).read_text(encoding="utf-8")


class IntentLoopTest(unittest.TestCase):
    def test_01_reviewer_unavailable_consistent(self) -> None:
        self.assertIn("可用性由调用方（本 skill）先判断", r("task-intent/references/goal-review.md"))
        self.assertIn("**不调用** role-based-reviewer", r("task-intent/references/goal-review.md"))
        self.assertIn("例外：调用方已判定不可用、未调用本 skill 并自行登记降级", r("role-based-reviewer/SKILL.md"))

    def test_02_intent_change_rule(self) -> None:
        c = r("taskrail/references/contract.md")
        for s in ("## 意图变更", "重跑 `task-intent`", "`version` +1", "**显式**改 `criterion`", "phase 回退", "经 taskflow 开修订子 change"):
            self.assertIn(s, c)
        self.assertIn("「意图变更」", r("task-explore/references/explore-design.md"))

    def test_03_done_gate_reads_intent(self) -> None:
        self.assertIn("8. 对照 `wizard/intent.md`", r("taskrail/SKILL.md"))
        self.assertIn("「不做」未被越界", r("taskrail/SKILL.md"))
        self.assertIn("另附 `wizard/intent.md`", r("taskflow/references/acceptance-rubric.md"))

    def test_04_wizard_gate_checks_criterion(self) -> None:
        self.assertIn("`criterion` 与 `wizard/intent.md`「做完的样子」一致", r("taskrail/references/phase-wizard.md"))

    def test_05_taskflow_points_to_seat(self) -> None:
        self.assertIn("交接 5 项、回 Digest ≤10 行", r("taskflow/SKILL.md"))

    def test_06_layout_has_intent_dirs(self) -> None:
        c = r("taskrail/references/contract.md")
        self.assertIn("wizard/intent.md         #", c)
        self.assertIn("evidence/intent/", c)

    def test_07_resume_skips_assumed(self) -> None:
        self.assertIn("`status: confirmed` 或 `assumed` 时不重做", r("task-intent/SKILL.md"))

    def test_08_goal_threshold_single(self) -> None:
        self.assertIn("通过线按 task-intent `goal-review.md`", r("taskrail/references/confirm-protocol.md"))

    def test_09_skip_rule_single_source(self) -> None:
        self.assertIn("跳过条件见 task-intent「何时跳过」", r("taskrail/references/contract.md"))
        self.assertIn("唯一真源", r("task-intent/SKILL.md"))

    def test_10_cross_skill_evals(self) -> None:
        e = r("taskrail/evals/cases.yaml")
        self.assertIn("id: intent-closed-loop", e)
        self.assertIn("id: intent-change-mid-task", e)

    def test_template_has_version(self) -> None:
        t = r("task-intent/references/statement-template.md")
        self.assertIn("version:", t)
        self.assertIn("## 历史版本", t)

    def test_severity_moved(self) -> None:
        self.assertIn("**Blocker**：必须修复", r("role-based-reviewer/references/severity.md"))
        self.assertIn("references/severity.md", r("role-based-reviewer/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
