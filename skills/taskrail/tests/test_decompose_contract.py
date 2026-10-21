"""拆分：默认不拆、两种拆法、路线图三条、子任务继承与范围内不停、父任务收尾、续跑取就绪项、explore 并入 design。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def read(name: str) -> str:
    return (REF / name).read_text(encoding="utf-8")


class WizardSplitTest(unittest.TestCase):
    def test_split_step_defaults_to_no_split(self) -> None:
        w = read("phase-wizard.md")
        self.assertIn("**拆分（仅 `full`，默认不拆）**", w)
        self.assertIn("## 路线图", w)
        self.assertIn("| 项 | 类型 | 目标 | 子判据 | 依赖 |", w)

    def test_roadmap_rides_the_wizard_stop(self) -> None:
        cp = read("confirm-protocol.md")
        self.assertIn("拆了再加路线图，一行一项", cp)
        self.assertIn("子判据合起来覆盖总判据、彼此不重叠、依赖无环", cp)


class SplitKindsTest(unittest.TestCase):
    def test_slices_by_default_children_only_when_independent(self) -> None:
        ls = read("large-scope.md")
        self.assertIn("切片（默认）", ls)
        self.assertIn("要分别交付，或在不同修改仓，且互不用对方的代码", ls)
        self.assertIn("两块之间有代码依赖，就是同一个 driver 的切片", ls)
        self.assertIn("只拆一层", ls)

    def test_children_live_under_subtasks_dir(self) -> None:
        self.assertIn("和父任务的 `wizard/`、`design/`、`approve/` 并列", read("large-scope.md"))
        self.assertIn("`ongoing/{parent}/subtasks/{sub}/TASK.md`", read("large-scope.md"))
        self.assertIn("subtasks/{sub}/", read("contract.md"))
        self.assertIn("`{parent}/subtasks/{sub}`", read("handoff.md"))
        self.assertIn("<parent>/subtasks/<sub>", (ROOT.parent / "taskflow" / "scripts" / "check_handoff.py").read_text(encoding="utf-8"))

    def test_roadmap_requirements(self) -> None:
        ls = read("large-scope.md")
        self.assertIn("子判据合起来覆盖总判据，彼此不重叠，依赖没有环", ls)
        self.assertIn("approve 冻结的是方案和路线图", ls)


class ChildTaskTest(unittest.TestCase):
    def test_child_inherits_parent_intent(self) -> None:
        self.assertIn("不重跑意图确认", read("large-scope.md"))
        self.assertIn("子任务（`TASK.md` 有 `parent:`）", read("intent.md"))
        self.assertIn("意图沿用父任务", read("phase-wizard.md"))

    def test_child_within_roadmap_keeps_going(self) -> None:
        self.assertIn("子任务的 wizard 与 approve", read("confirm-protocol.md"))
        a = read("approve.md")
        self.assertIn("在父任务路线图范围内", a)
        self.assertIn("超出范围或要改子判据，才按 approve 行停", a)

    def test_parent_closes_on_total_criterion(self) -> None:
        ls = read("large-scope.md")
        self.assertIn("验一次总判据", ls)
        self.assertIn("整树同轮归档", ls)
        self.assertIn("拆成子任务的父任务写在父 `TASK.md`「验证」节，且子任务全部 `done`", read("done.md"))
        self.assertIn("父任务走 wizard → apply（推进子任务）→ done", read("contract.md"))


class ResumeTest(unittest.TestCase):
    def test_resume_reports_progress_and_takes_next_ready(self) -> None:
        ls = read("large-scope.md")
        self.assertIn("N 个里做完了 M 个", ls)
        self.assertIn("取依赖已满足、还没做完的下一项，正在做的优先", ls)
        self.assertIn("N 个里做完了 M 个", read("user-report.md"))
        self.assertIn("「续跑」取下一个就绪项", read("ledger.md"))


class DesignFoldTest(unittest.TestCase):
    def test_explore_folded_into_design(self) -> None:
        self.assertIn("`phase: explore` 按 `design` 读", read("contract.md"))
        d = read("design.md")
        self.assertIn("## 第一步：grill 自问自答", d)
        self.assertIn("## 第二步：写方案", d)
        self.assertFalse((REF / "explore-design.md").exists())


if __name__ == "__main__":
    unittest.main()
