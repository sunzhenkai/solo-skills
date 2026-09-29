"""taskflow 文本契约：Driver 协议、一轮结束、dirty 三选一、rubric 通过线。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_frontmatter_fields_present(self) -> None:
        self.assertIn("id: taskflow", self.text)
        self.assertIn("name: taskflow", self.text)
        self.assertIn("description:", self.text)

    def test_id_matches_directory(self) -> None:
        self.assertEqual(SKILL_ROOT.name, "taskflow")

    def test_referenced_references_exist(self) -> None:
        for rel in (
            "references/acceptance-rubric.md",
            "references/delivery-quality-loop.md",
            "references/implementer-isolation.md",
        ):
            self.assertTrue((SKILL_ROOT / rel).is_file(), rel)


class TestDriverProtocol(unittest.TestCase):
    """Driver 协议是固定文本，逐字写入 proposal；skip_specs 必须显式写入。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_protocol_verbatim_gate(self) -> None:
        self.assertIn("`Driver 协议` 小节是固定文本，逐字写入，不要改写或精简", self.text)

    def test_skip_specs_explicit_gate(self) -> None:
        self.assertIn("`skip_specs: true` 必须显式写入", self.text)

    def test_protocol_template_contains_branch_rule(self) -> None:
        self.assertIn("由用户三选一——不切直接在当前分支修改 / 携带改动 `git switch` / `git worktree add`", self.text)
        self.assertIn("不得 stash / reset / 强制切换", self.text)

    def test_branch_rule_single_source(self) -> None:
        self.assertIn("切分支规则的唯一真相是上方 Driver 协议模板（逐字写入每个 driver proposal）", self.text)

    def test_profile_snapshot_verbatim(self) -> None:
        self.assertIn("`Why` 逐字保留该快照，不摘要、不改写、不用小节指针或路径替代", self.text)


class TestRoundEndConditions(unittest.TestCase):
    """一轮结束三条件是固定门禁，模板与纪律节双写同文。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_three_conditions_in_template(self) -> None:
        self.assertIn("只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮", self.text)

    def test_three_conditions_restated_in_discipline(self) -> None:
        self.assertIn("规则的唯一真相是上方 Driver 协议模板：只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮", self.text)

    def test_itemized_unfinished_list(self) -> None:
        self.assertIn("结束时逐条列出未勾项与原因", self.text)


class TestAcceptanceRubric(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("references/acceptance-rubric.md")

    def test_global_pass_line(self) -> None:
        self.assertIn("全量通过线：五维均 ≥2，UI/UX 六子项均值 ≥2.5，任一子项为 0 不通过。", self.text)

    def test_uiux_zero_subitem_blocks(self) -> None:
        self.assertIn("任一子项为 0 则不通过，即使均值达标", self.text)

    def test_skill_body_restates_thresholds(self) -> None:
        text = read("SKILL.md")
        self.assertIn("五维均 ≥2、UI/UX 均值 ≥2.5", text)


class TestPendingConfirmationSyncLock(unittest.TestCase):
    """「pending 降级只有用户能确认」在三个 skill 各有一份文本。

    任一处缺失即 fail：防止三份同源纪律改一处漏两处。
    """

    def test_task_goal_declares_user_only_confirmation(self) -> None:
        text = (REPO_ROOT / "skills/task-goal/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("审阅收敛与单独的「继续」都不算确认", text)

    def test_task_explore_decide_declares_user_only_confirmation(self) -> None:
        text = (REPO_ROOT / "skills/task-explore/references/phase-decide.md").read_text(encoding="utf-8")
        self.assertIn("审阅收敛、单独的「继续」、执行者或评审者的判断都不算确认", text)

    def test_task_explore_handoff_blocks_driver_on_pending(self) -> None:
        text = (REPO_ROOT / "skills/task-explore/references/phase-handoff.md").read_text(encoding="utf-8")
        self.assertIn("只有用户点名接受该项、或明确说按降级表全部确认后才继续", text)
        self.assertIn("不创建 driver", text)

    def test_taskflow_declares_user_only_confirmation(self) -> None:
        text = read("SKILL.md")
        self.assertIn("执行者、子代理与审阅收敛都不算用户确认", text)

    def test_new_downgrade_needs_user_decision(self) -> None:
        text = read("SKILL.md")
        self.assertIn("不静默接受、不自行确认", text)


if __name__ == "__main__":
    unittest.main()
