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

    def test_task_confirm_declares_user_only_confirmation(self) -> None:
        text = (REPO_ROOT / "skills/task-confirm/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("审阅收敛与单独的「继续」都不算确认", text)

    def test_task_explore_approve_declares_user_only_confirmation(self) -> None:
        text = (REPO_ROOT / "skills/task-explore/references/phase-approve.md").read_text(
            encoding="utf-8"
        )
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


class TestSuspendIntegration(unittest.TestCase):
    """「需要用户决策」挂起五元组 + 只停依赖面 + 恢复触发。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_suspension_reference(self) -> None:
        self.assertIn("task-confirm/references/suspension.md", self.text)
        self.assertTrue(
            (REPO_ROOT / "skills/task-confirm/references/suspension.md").is_file(),
            "cross-ref target missing",
        )

    def test_five_tuple_presented(self) -> None:
        self.assertIn("挂起五元组呈现（等待项、授权形状、阻塞面、非依赖面、恢复触发）", self.text)

    def test_only_dependency_surface_stops(self) -> None:
        self.assertIn("「需要用户决策」只停依赖该项的条目，其余条目继续", self.text)
        self.assertIn("不整轮停摆", self.text)

    def test_resume_trigger_with_echo_back(self) -> None:
        self.assertIn("用户输入到达先比对授权形状", self.text)
        self.assertIn("复述生效", self.text)


class TestDowngradeABSync(unittest.TestCase):
    """新降级 A/B 定级与 provisional 追认；收尾门按类拆分。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")
        self.loop = read("references/delivery-quality-loop.md")
        self.rubric = read("references/acceptance-rubric.md")

    def test_ab_classification_in_skill(self) -> None:
        self.assertIn("**A 类**（缩完成判据或交付面；拿不准归 A）", self.text)
        self.assertIn("**B 类**（判据与交付面都不缩）", self.text)
        self.assertIn("task-confirm/references/quality-profile.md", self.text)

    def test_provisional_exception_narrow(self) -> None:
        self.assertIn("B 类 `provisional` 是唯一例外", self.text)
        self.assertIn("追认前不算 `confirmed`", self.text)

    def test_ratification_and_rollback(self) -> None:
        self.assertIn("到用户在场点（真人门、收口）集中追认", self.text)
        self.assertIn("回滚说明处理后回降级确认门重定级", self.text)

    def test_backfill_split_by_class(self) -> None:
        self.assertIn("B 类 `provisional` 期间可回填不依赖该项的验收标准", self.loop)
        self.assertIn("A 类 `pending` 降级为 0、B 类无未追认 `provisional`（全部 `confirmed`）", self.loop)

    def test_rubric_scoring_with_provisional(self) -> None:
        self.assertIn("B 类可按 `provisional` 临时确认的范围评分并标注「待追认」", self.rubric)


class TestSelfEvolutionSingleSource(unittest.TestCase):
    """Self-evolution 注入块为紧凑单一模板：各 skill 逐字同文，只换目录名。

    writing-for-agents 优化：原 84 行样板压成一段指针式短块，常驻 context 只付一次。
    """

    DIRS = ("taskflow", "task-confirm", "repo-manager", "skills-store")

    def _block(self, skill: str) -> str:
        text = (REPO_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        idx = text.find("## Self-evolution")
        self.assertGreater(idx, 0, f"{skill}: 缺 Self-evolution 段")
        return text[idx:].replace(f"skills/{skill}", "<skill-dir>")

    def test_blocks_are_byte_identical(self) -> None:
        blocks = {s: self._block(s) for s in self.DIRS}
        first = blocks[self.DIRS[0]]
        for skill, block in blocks.items():
            self.assertEqual(first, block, f"{skill}: Self-evolution 块与其他 skill 漂移")

    def test_compact_form_kept(self) -> None:
        block = self._block("taskflow")
        self.assertLess(len(block.splitlines()), 30, "样板块过长，应保持指针式短块")
        for kept in ("examples/", "evals/cases.yaml", "experience/", "skill-evolver", "patches/"):
            self.assertIn(kept, block)

    def test_injection_template_matches_blocks(self) -> None:
        tpl = (REPO_ROOT / "skills/skill-upgrader/references/skill-injection.md").read_text(encoding="utf-8")
        tpl_block = tpl[tpl.find("## Self-evolution"):].replace("<skill-dir>", "<skill-dir>")
        self.assertEqual(self._block("taskflow"), tpl_block, "注入模板与生产块漂移")

    def test_long_form_scaffolding_gone(self) -> None:
        block = self._block("taskflow")
        for gone in ("Directly modify SKILL.md", "Improvement Proposal", "不要记录 trivial information"):
            self.assertNotIn(gone, block)


class TestDescriptionTriggerBranches(unittest.TestCase):
    """description 是常驻 context 的顶层 context pointer：只留触发分支，不复述正文。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_trigger_branches_kept(self) -> None:
        for branch in ("taskflow-new", "{task}-driver", "OpenSpec change"):
            self.assertIn(branch, self.text.split("---")[1], f"description 丢了触发分支 {branch}")

    def test_description_drops_body_detail(self) -> None:
        desc = self.text.split("---")[1]
        for detail in ("skip_specs", "零脚本", "第二份任务账本"):
            self.assertNotIn(detail, desc, f"description 复述了正文细节：{detail}")



class TestSimpleSingleSlice(unittest.TestCase):
    def test_simple_single_slice_section(self) -> None:
        text = read("SKILL.md")
        self.assertIn("### simple 单切片", text)
        self.assertIn("实施段默认**仅 1 个子 change**", text)
        self.assertIn("进度仍只认 checkbox", text)


if __name__ == "__main__":
    unittest.main()
