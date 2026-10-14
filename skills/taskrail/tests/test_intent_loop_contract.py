"""意图闭环：task-intent ↔ taskrail ↔ task-explore ↔ taskflow ↔ role-based-reviewer 的跨 skill 文本契约（审计 10 条缺口）。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]


def r(rel: str) -> str:
    return (SKILLS / rel).read_text(encoding="utf-8")


class IntentLoopTest(unittest.TestCase):
    def test_01_reviewer_unavailable_consistent(self) -> None:
        self.assertIn("可用性由本 skill 先判断", r("task-intent/references/intent.md"))
        self.assertIn("**不调用** role-based-reviewer", r("task-intent/references/intent.md"))
        self.assertIn("例外：调用方已判定不可用、未调用本 skill 并自行登记降级", r("role-based-reviewer/SKILL.md"))

    def test_02_intent_change_rule(self) -> None:
        c = r("taskrail/references/contract.md")
        for s in ("## 意图变更", "重跑 `task-intent`", "纠偏记录追加一行", "**显式**改 `criterion`", "phase 回退", "经 taskflow 开修订子 change"):
            self.assertIn(s, c)
        self.assertIn("「意图变更」", r("task-explore/references/explore-design.md"))

    def test_03_done_gate_reads_intent(self) -> None:
        self.assertIn("8. 对照 `wizard/intent.md`", r("taskrail/SKILL.md"))
        self.assertIn("「不做」未被越界", r("taskrail/SKILL.md"))
        self.assertIn("另附 `wizard/intent.md`", r("taskflow/references/acceptance-rubric.md"))

    def test_04_wizard_gate_checks_criterion(self) -> None:
        self.assertIn("`criterion` 与 `wizard/intent.md`「做完的样子」一致", r("taskrail/references/phase-wizard.md"))

    def test_05_taskflow_points_to_seat(self) -> None:
        self.assertIn("执行座位", r("taskflow/SKILL.md"))

    def test_06_layout_has_intent_dirs(self) -> None:
        c = r("taskrail/references/contract.md")
        self.assertIn("wizard/intent.md         #", c)
        self.assertIn("evidence/intent/", c)

    def test_07_resume_skips_assumed(self) -> None:
        self.assertIn("`status: confirmed` 或 `assumed` 时不重做", r("task-intent/SKILL.md"))

    def test_08_goal_threshold_single(self) -> None:
        self.assertIn("通过线按 task-intent `references/intent.md`", r("taskrail/references/confirm-protocol.md"))

    def test_09_skip_rule_single_source(self) -> None:
        self.assertIn("跳过条件见 task-intent「何时跳过」", r("taskrail/references/contract.md"))
        self.assertIn("唯一真源", r("task-intent/SKILL.md"))

    def test_10_cross_skill_evals(self) -> None:
        e = r("taskrail/evals/cases.yaml")
        self.assertIn("id: intent-closed-loop", e)
        self.assertIn("id: intent-change-mid-task", e)

    def test_severity_moved(self) -> None:
        self.assertIn("**Blocker**：必须修复", r("role-based-reviewer/references/severity.md"))
        self.assertIn("references/severity.md", r("role-based-reviewer/SKILL.md"))


class PlainTalkTest(unittest.TestCase):
    def test_shared_guideline_with_examples(self) -> None:
        c = r("taskrail/references/contract.md")
        self.assertIn("## 对用户说话", c)
        sec = c.split("## 对用户说话", 1)[1].split("\n## ", 1)[0]
        self.assertGreaterEqual(sec.count("前：「"), 3)
        self.assertGreaterEqual(sec.count("后：「"), 3)

    def test_skills_point_to_guideline(self) -> None:
        for rel in ("taskrail/SKILL.md", "task-explore/SKILL.md", "taskflow/SKILL.md",
                    "taskrail/references/confirm-protocol.md", "role-based-reviewer/references/protocol.md",
                    "task-intent/references/intent.md"):
            self.assertIn("「对用户说话」", r(rel), rel)


if __name__ == "__main__":
    unittest.main()
