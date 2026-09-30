"""task-goal 文本契约：完成程度条件、P 级定义、评审者三选一、pending 确认门与退出点。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_frontmatter_fields_present(self) -> None:
        self.assertIn("id: task-goal", self.text)
        self.assertIn("name: task-goal", self.text)
        self.assertIn("description:", self.text)

    def test_id_matches_directory(self) -> None:
        self.assertEqual(SKILL_ROOT.name, "task-goal")

    def test_referenced_references_exist(self) -> None:
        for rel in (
            "references/quality-profile.md",
            "references/legacy-plans.md",
            "references/state-machine.md",
            "references/state-file.md",
            "CONTEXT.md",
        ):
            self.assertTrue((SKILL_ROOT / rel).is_file(), rel)


class TestPlanIntake(unittest.TestCase):
    """解耦接口：接到上游 task-wizard 方案原文时逐字采用，不重新摸底。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_intake_verbatim(self) -> None:
        self.assertIn("跳过产方案，逐字采用，不重新摸底、不改写", self.text)

    def test_no_goal_branch_in_task_wizard(self) -> None:
        wizard = (SKILL_ROOT.parent / "task-wizard" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("## Goal 方案", wizard)
        self.assertNotIn("## 先分流", wizard)


class TestCompletionGradeConditions(unittest.TestCase):
    """完成程度写入是显式条件分支，P0/P1 有无优先于审阅者定级。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_explicit_condition_intro(self) -> None:
        self.assertIn("完成程度的写入按显式条件判定，P0/P1 的有无优先于审阅者定级：", self.text)

    def test_branch_with_p0_p1(self) -> None:
        self.assertIn("本轮发现含 P0 或 P1：完成程度取「中或低」。审阅者定级为高 → 写「中」；定级为中或低 → 从其值。", self.text)

    def test_branch_without_p0_p1(self) -> None:
        self.assertIn("本轮无 P0 也无 P1：完成程度写「高」，审阅者定级不参与。", self.text)

    def test_reviewer_grade_not_self_decided(self) -> None:
        self.assertIn("完成程度按本节规则写入，不由它自定", self.text)
        self.assertIn("执行者自己给出的完成程度不算审阅结论", self.text)


class TestSeverityDefinitions(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_p0_p1_p2_defined(self) -> None:
        self.assertIn("**P0**：完成判据不可检查", self.text)
        self.assertIn("**P1**：验证对不住判据", self.text)
        self.assertIn("**P2**：不改道的写法、顺序、两行限制或省略。P2 不参与完成程度", self.text)

    def test_role_reviewer_mapping(self) -> None:
        self.assertIn("Blocker 记 P0，Major 记 P1，Minor / Suggestion 记 P2", self.text)


class TestReviewerSelection(unittest.TestCase):
    """评审者三选一必选，选中唯一，新增「评审者未定」退出点。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")
        self.context = read("CONTEXT.md")

    def test_mandatory_choice(self) -> None:
        self.assertIn("评审者是必选项，每次审阅从三种里选一种，选中即唯一，不叠加", self.text)

    def test_three_ways_named(self) -> None:
        for way in ("role-based-reviewer", "agent-roster", "subagent"):
            self.assertIn(way, self.text)

    def test_old_fallback_wording_replaced(self) -> None:
        self.assertNotIn("其余情况：当前宿主拉起的子 agent", self.text)

    def test_reviewer_recorded(self) -> None:
        self.assertIn("每次审阅的评审者记录到回复里", self.text)

    def test_exit_point_reviewer_undecided(self) -> None:
        self.assertIn("**评审者未定**", self.text)
        self.assertIn("评审者未定；降级未确认", self.text)

    def test_context_reviewer_term_updated(self) -> None:
        self.assertIn("三种之一：subagent、agent-roster Endpoint、role-based-reviewer 编排的角色视角", self.context)


class TestPendingDowngradeGate(unittest.TestCase):
    """降级分级后：A 类硬门不变——confirmed 仍只有用户能写；B 类走临时确认。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_exit_point_wording(self) -> None:
        self.assertIn("只有用户点名接受该项、或明确说按降级表全部确认时，才把该项改为 `confirmed` 并继续；审阅收敛与单独的「继续」都不算确认", self.text)

    def test_quality_profile_reiterates_user_only(self) -> None:
        text = read("references/quality-profile.md")
        self.assertIn("`confirmed` 只有用户能写", text)
        self.assertIn("`provisional` 只有 B 类可经审阅收敛写入（临时确认），A 类任何情况下都不许", text)

    def test_completion_requires_zero_pending(self) -> None:
        self.assertIn("降级表无 `pending` 且无 `provisional`", self.text)
        text = read("references/quality-profile.md")
        self.assertIn("完成门：字段齐全，降级表无 `pending` 且无 `provisional`", text)


class TestExitUnblock(unittest.TestCase):
    """退出点松绑包：降级 A/B 分级、复述生效、无进展轮括号语义修复。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.profile = read("references/quality-profile.md")
        self.grid = read("references/state-machine.md")
        self.state_file = read("references/state-file.md")

    def test_downgrade_ab_classification(self) -> None:
        self.assertIn("**A 类**（使完成判据不成立或收窄交付面；拿不准一律归 A）", self.skill)
        self.assertIn("**B 类**（完成判据与交付面都不缩）", self.skill)
        self.assertIn("拿不准一律归 A", self.profile)
        self.assertIn("回滚说明", self.profile)

    def test_class_b_does_not_stop(self) -> None:
        self.assertIn("不停机、不命中本退出点", self.skill)
        self.assertIn("B 类 `pending` 走审阅临时确认，不停机", self.profile)

    def test_ratification_at_presence_points(self) -> None:
        self.assertIn("到用户在场点（真人门、收口）集中追认", self.skill)
        self.assertIn("否决按该项回滚说明处理后回本退出点重定级", self.skill)

    def test_confirmation_status_enum_extended(self) -> None:
        self.assertIn("<confirmed | provisional | pending>", self.profile)

    def test_echo_back_authorization(self) -> None:
        self.assertIn("理解为授权 <项>，若无纠正即生效", self.skill)
        self.assertIn("不可逆动作除外", self.skill)
        self.assertIn("逐字点名该动作本身", self.skill)
        self.assertIn("单独的「继续」仍不算授权", self.skill)

    def test_no_progress_paren_fixed(self) -> None:
        self.assertIn("任一到达即算新输入", self.skill)
        self.assertIn("任一到达即算新输入", self.grid)
        self.assertNotIn("均不算", self.skill)
        self.assertNotIn("均不算", self.grid)

    def test_grid_and_state_file_synced(self) -> None:
        self.assertIn("复述生效", self.grid)
        self.assertIn("降级无 `pending` 无 `provisional`", self.grid)
        self.assertIn("意图命中", self.state_file)


class TestExitPoints(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_exit_point_labels_defined(self) -> None:
        for label in (
            "**理解不够**",
            "**审阅不通过**",
            "**审阅派不出**",
            "**审阅没有结论**",
            "**评审者未定**",
            "**降级未确认**",
            "**线上动作**",
            "**泄密**",
            "**执行中升档**",
        ):
            self.assertIn(label, self.text)

    def test_exit_list_present_in_template(self) -> None:
        self.assertIn("审阅不通过；审阅派不出；审阅没有结论；评审者未定；降级未确认", self.text)


class TestStateMachine(unittest.TestCase):
    """状态机：事件封闭枚举、四状态各成一行、已停行穷举全部事件、无进展轮兜底。"""

    EVENTS = (
        "用户授权",
        "用户继续",
        "用户改向",
        "goal 自动续跑",
        "审阅收敛",
        "审阅未收敛",
        "退出点命中",
        "判据成立",
        "步骤推进",
        "外部新事实到达",
        "用户补充信息",
    )

    STATES = ("执行中", "已停", "已交接", "已完成")

    def setUp(self) -> None:
        self.text = read("references/state-machine.md")
        self.skill = read("SKILL.md")

    def _row(self, state: str) -> str:
        for line in self.text.splitlines():
            if line.startswith(f"| **{state}**"):
                return line
        self.fail(f"missing row for state {state}")

    def _cells(self, row: str) -> list:
        return [c.strip() for c in row.split("|")[1:-1]]

    def test_reference_file_exists(self) -> None:
        self.assertTrue((SKILL_ROOT / "references/state-machine.md").is_file())

    def test_all_events_named(self) -> None:
        for ev in self.EVENTS:
            self.assertIn(f"**{ev}**", self.text)

    def test_event_enum_is_closed(self) -> None:
        self.assertIn("封闭枚举", self.text)

    def test_each_state_has_a_row(self) -> None:
        for st in self.STATES:
            row = self._row(st)
            cells = self._cells(row)
            # 状态列 + 11 个事件列
            self.assertEqual(len(cells), 1 + len(self.EVENTS), f"row {st} cell count")

    def test_stopped_row_covers_all_events(self) -> None:
        row = self._row("已停")
        cells = self._cells(row)[1:]
        non_empty = [c for c in cells if c and c != "—"]
        # 已停行穷举全部事件；允许「判据成立」「步骤推进」两格为「—」（已停只等授权，不验证步骤）
        self.assertGreaterEqual(len(non_empty), len(self.EVENTS) - 2)

    def test_blocked_defined_as_stopped_form(self) -> None:
        self.assertIn("「已停」的交接形态，不是第五状态", self.text)

    def test_no_progress_round_fallback_present(self) -> None:
        self.assertIn("## 无进展轮", self.text)
        self.assertIn("禁止原样重复", self.text)

    def test_skill_references_state_machine(self) -> None:
        self.assertIn("references/state-machine.md", self.skill)
        self.assertIn("**无进展轮（兜底）**", self.skill)

    def test_skill_no_progress_round_content(self) -> None:
        self.assertIn("状态与退出点与上一轮完全相同", self.skill)
        self.assertIn("禁止原样重复上一轮回复", self.skill)


class TestGoalTransitionScript(unittest.TestCase):
    """迁移判定脚本：存在、可运行、对每个非空格给出已定义迁移。"""

    def setUp(self) -> None:
        self.script = SKILL_ROOT / "scripts" / "goal_transition.py"

    def _run(self, *args: str) -> tuple[int, dict]:
        import json
        import subprocess

        proc = subprocess.run(
            ["python3", str(self.script), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"script did not emit JSON: stdout={proc.stdout!r} stderr={proc.stderr!r}")
        return proc.returncode, out

    def test_script_exists(self) -> None:
        self.assertTrue(self.script.is_file())

    def test_script_stdlib_only(self) -> None:
        src = self.script.read_text(encoding="utf-8")
        # 不允许第三方依赖；顶层 import 只能是 argparse/json/re/sys/pathlib
        import re

        imports = re.findall(r"^(?:import|from)\s+([\w\.]+)", src, flags=re.M)
        allowed = {"argparse", "json", "re", "sys", "pathlib", "__future__"}
        for mod in imports:
            self.assertIn(mod.split(".")[0], allowed, f"unexpected import {mod}")

    def test_defined_combo_returns_next_state(self) -> None:
        code, out = self._run("--state", "已停", "--event", "用户授权")
        self.assertEqual(code, 0)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "执行中")

    def test_autocontinue_third_blocks(self) -> None:
        code, out = self._run(
            "--state", "已停", "--event", "goal 自动续跑", "--autocontinue-count", "3"
        )
        self.assertEqual(code, 0)
        self.assertIn("blocked", out["action"])

    def test_undefined_combo_nonzero_with_note(self) -> None:
        code, out = self._run("--state", "已停", "--event", "判据成立")
        self.assertEqual(code, 1)
        self.assertFalse(out["defined"])
        self.assertIsNone(out["next_state"])
        self.assertIn("无进展轮", out["note"])

    def test_unknown_event_nonzero(self) -> None:
        code, out = self._run("--state", "已停", "--event", "未定义事件")
        self.assertEqual(code, 1)
        self.assertIn("封闭枚举", out["note"])

    def test_state_file_smoke(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            from pathlib import Path as P
            p = P(tmp) / "goal-state.yaml"
            p.write_text(
                "state: 已停\nexit_point: x\nautocontinue_count: 0\nblocked: false\n",
                encoding="utf-8",
            )
            code, out = self._run("--state-file", str(p), "--event", "goal 自动续跑", "--write")
            self.assertEqual(code, 0)
            self.assertTrue(out["wrote_back"])
            text = p.read_text(encoding="utf-8")
            self.assertIn("autocontinue_count: 1", text)

    def test_event_tag_smoke(self) -> None:
        code, out = self._run("--state", "已停", "--event-tag", "auto-continue", "--autocontinue-count", "1")
        self.assertEqual(code, 0)
        self.assertEqual(out["event"], "goal 自动续跑")


class TestQualityProfileContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("references/quality-profile.md")

    def test_ui_four_questions_no_builtin_answers(self) -> None:
        self.assertIn("四问只约束「底线要写清」，不规定具体取值", self.text)
        self.assertIn("icon 形态: <是否收敛到单一 icon primitive 及其来源", self.text)

    def test_adjective_not_allowed(self) -> None:
        self.assertIn("「高质量」「体验好」「足够健壮」这类形容词不算", self.text)

    def test_role_bottom_lines_all_three(self) -> None:
        self.assertIn("`角色底线` 下的 product、design、engineer 三条一条都不能省", self.text)


class TestReviewLoopLossStreak(unittest.TestCase):
    """核对循环：按条计数（连败/恶化闸），不按轮次封顶；回归条有通道。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_per_finding_tracking(self) -> None:
        self.assertIn("核对的单位是「条」不是「轮」", self.text)
        self.assertIn("**已消失**", self.text)
        self.assertIn("**仍在**", self.text)
        self.assertIn("**新增**", self.text)

    def test_loss_streak_cap(self) -> None:
        self.assertIn("连败封顶", self.text)
        self.assertIn("连续两轮核过「仍在」", self.text)

    def test_deterioration_gate(self) -> None:
        self.assertIn("恶化闸", self.text)
        self.assertIn("回归账", self.text)

    def test_no_round_cap_wording(self) -> None:
        self.assertNotIn("第二次核对", self.text)
        self.assertNotIn("再写入一次", self.text)

    def test_exit_point_aligned_with_loss_streak(self) -> None:
        self.assertIn("连续两轮核过仍在（连败封顶）", self.text)
        self.assertIn("旧条全消只有新增条（未达恶化闸），不是这个标签", self.text)

    def test_exit_point_label_set_unchanged(self) -> None:
        self.assertIn("审阅不通过；审阅派不出；审阅没有结论；评审者未定；降级未确认", self.text)

    def test_stopped_means_no_more_writes(self) -> None:
        self.assertIn("已停后不再写入，等授权", self.text)


class TestReviewQueue(unittest.TestCase):
    """审阅排队：资源等待与授权等待分离；已停期间可重试派审。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.grid = read("references/state-machine.md")
        self.suspension = read("references/suspension.md")

    def test_queue_defined(self) -> None:
        self.assertIn("**审阅排队**（资源等待，不是授权等待）", self.skill)
        self.assertIn("连续两轮重试仍派不出", self.skill)
        self.assertIn("路由写「等端点恢复」", self.skill)

    def test_no_conclusion_does_not_queue(self) -> None:
        self.assertIn("「审阅没有结论」（派得出、回不来可用结论）不排队", self.skill)

    def test_stopped_round_dispatch_retry(self) -> None:
        self.assertIn("还允许重试派审（审阅者只读）", self.skill)
        self.assertIn("本退出点的已停期间，goal 自动续跑轮允许重试派审", self.skill)

    def test_grid_cell_synced(self) -> None:
        self.assertIn("审阅类退出点可重试派审", self.grid)

    def test_suspension_whitelist_synced(self) -> None:
        self.assertIn("审阅类等待", self.suspension)
        self.assertIn("重试派审", self.suspension)
        self.assertIn("该\n等待自动解除", self.suspension)


class TestHypothesisStreak(unittest.TestCase):
    """验证连败按假设身份计数：同假设两败、换假设写判伪差异、假设空间封顶。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_per_hypothesis_counting(self) -> None:
        self.assertIn("同一条验证在**同一假设**下连续失败两次", self.text)
        self.assertIn("对失败原因的可判伪解释", self.text)

    def test_hypothesis_switch_writes_falsifier(self) -> None:
        self.assertIn("换假设必须写下新假设及其与旧假设的判伪差异", self.text)

    def test_hypothesis_budget_capped(self) -> None:
        self.assertIn("累计假设已达 3 个仍失败", self.text)

    def test_no_external_condition(self) -> None:
        self.assertNotIn("且没有新事实", self.text)


class TestSuspensionProtocol(unittest.TestCase):
    """挂起子协议：五元组、白名单、blocked 形态、恢复语义统一定义。"""

    def setUp(self) -> None:
        self.skill = read("SKILL.md")
        self.text = read("references/suspension.md")

    def test_reference_file_exists(self) -> None:
        self.assertTrue((SKILL_ROOT / "references" / "suspension.md").is_file())

    def test_five_tuple_fields(self) -> None:
        for field in ("**等待项**", "**授权形状**", "**阻塞面**", "**非依赖面**", "**恢复触发**"):
            self.assertIn(field, self.text)

    def test_whitelist_and_forbidden(self) -> None:
        self.assertIn("只读环境查证、外部原文取证、证据固化", self.text)
        self.assertIn("禁止", self.text)

    def test_blocked_four_sections(self) -> None:
        self.assertIn("已完成、未完成、证据、下一步", self.text)
        self.assertIn("blocked 不是新状态", self.text)

    def test_non_goal_first_stop_presents_tuple(self) -> None:
        self.assertIn("首次停下即按五元组呈现", self.text)

    def test_skill_references_suspension(self) -> None:
        self.assertEqual(self.skill.count("references/suspension.md"), 4)
        self.assertIn("挂起五元组", self.skill)
        self.assertIn("以本节为准", self.skill)


if __name__ == "__main__":
    unittest.main()
