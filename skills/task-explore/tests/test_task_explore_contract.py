"""task-explore：阶段门禁、落点与按需加载的文本契约。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def skill_corpus(root: Path) -> str:
    """SKILL.md 正文 + references/*.md：细则下沉到 references 后，文本契约按整个 skill 校核。"""
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    parts += [p.read_text(encoding="utf-8") for p in sorted((root / "references").glob("*.md"))]
    return "\n".join(parts)



class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_corpus(ROOT)
        cls.explore = (ROOT / "references" / "explore-design.md").read_text(
            encoding="utf-8"
        )
        cls.design = (ROOT / "references" / "explore-design.md").read_text(
            encoding="utf-8"
        )
        cls.decide = (ROOT / "references" / "approve.md").read_text(
            encoding="utf-8"
        )
        cls.approve = (ROOT / "references" / "approve.md").read_text(
            encoding="utf-8"
        )
        cls.handoff = (ROOT / "references" / "handoff.md").read_text(
            encoding="utf-8"
        )
        cls.archive = (ROOT / "references" / "archive-reopen.md").read_text(
            encoding="utf-8"
        )
        cls.reopen = (ROOT / "references" / "archive-reopen.md").read_text(
            encoding="utf-8"
        )
        cls.ledger = (
            ROOT / "references" / "ledger.md"
        ).read_text(encoding="utf-8")
        cls.plan_review = (
            ROOT / "references" / "approve.md"
        ).read_text(encoding="utf-8")
        cls.design_template = (
            ROOT / "references" / "templates.md"
        ).read_text(encoding="utf-8")

    @staticmethod
    def _section(text: str, head: str) -> str:
        return text.split(head, 1)[1].split("## ", 1)[0]

    def test_frontmatter_name_matches_directory(self) -> None:
        self.assertIn("name: task-explore", self.skill)
        self.assertEqual(ROOT.name, "task-explore")

    def test_reference_files_exist(self) -> None:
        for rel in (
            "references/explore-design.md",
            "references/explore-design.md",
            "references/approve.md",
            "references/approve.md",
            "references/handoff.md",
            "references/archive-reopen.md",
            "references/archive-reopen.md",
            "references/approve.md",
            "references/templates.md",
            "references/templates.md",
            "references/templates.md",
            "references/ledger.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_missing_tasks_dir_created_without_asking(self) -> None:
        self.assertIn("没有 `tasks/` 时在仓库根直接创建并一句话说明", self.skill)
        self.assertIn("若没有 `tasks/`：在当前仓库根直接创建", self.skill)
        self.assertNotIn("未确认则停止", self.skill)

    def test_unbound_decides_new_or_resume(self) -> None:
        self.assertIn("自行判定新建或恢复，一句话说出决定和理由，不提问", self.skill)
        self.assertNotIn("应提示创建或者恢复", self.skill)
        self.assertNotIn("用户确认前不进入", self.skill)

    def test_approve_exit_handoff_not_archive(self) -> None:
        self.assertIn("下一步只写 handoff", self.approve)
        self.assertIn("不列 archive", self.approve)
        self.assertIn("禁止用当轮叙事改写 `criterion`", self.approve)
        self.assertIn("taskflow 子 change", self.approve)
        self.assertIn("拒绝进入本阶段，改走 handoff", self.archive)
        self.assertIn("「方案已写完」「还有未决」不是关闭原因", self.archive)
        section = self._section(self.skill, "## `archive`")
        self.assertIn("改走 handoff", section)

    def test_index_sync_on_mutating_phases(self) -> None:
        self.assertIn(
            "`new` / `split` / `expand` / `save` / `approve` / `decide` / `handoff` / `archive` / `reopen` 必须同步对应行",
            self.skill,
        )

    def test_phase_loaded_on_demand(self) -> None:
        self.assertIn("只读该命令详情", self.skill)
        self.assertIn("不要预加载其它 phase", self.skill)
        self.assertIn("references/explore-design.md", self.skill)
        self.assertIn("references/explore-design.md", self.skill)
        self.assertIn("references/approve.md", self.skill)
        self.assertIn("references/approve.md", self.skill)
        self.assertIn("references/handoff.md", self.skill)
        self.assertIn("references/archive-reopen.md", self.skill)
        self.assertIn("references/archive-reopen.md", self.skill)
        self.assertNotIn("| 方案 | 成本 |", (ROOT / "SKILL.md").read_text(encoding="utf-8"))

    def test_explore_does_not_write_repo_glossary(self) -> None:
        self.assertIn("只委托 `grilling`", self.explore)
        self.assertIn("禁止调用 `grill-with-docs` 或 `domain-modeling`", self.explore)
        self.assertIn("禁止写仓库根 `CONTEXT.md`、`docs/adr/`", self.explore)
        self.assertNotIn("使用 `grill-with-docs` 进行", self.explore)
        explore_sec = self._section(self.skill, "## `explore`")
        self.assertIn("禁止调用 `grill-with-docs`", explore_sec)
        self.assertNotIn("委托 `grill-with-docs`", explore_sec)

    def test_resume_task_docs_readonly_index_repair_allowed(self) -> None:
        self.assertIn("任务文档只读", self.skill)
        self.assertIn("INDEX 漂移可重建", self.skill)
        resume = self._section(self.skill, "## `resume`")
        self.assertIn("任务文档只读", resume)
        self.assertIn("INDEX", resume)
        self.assertIn("reopen", resume)

    def test_two_task_kinds_are_named(self) -> None:
        self.assertIn("探索任务", self.skill)
        self.assertIn("taskflow 任务", self.skill)
        self.assertIn("`{task-name}-driver`", self.skill)

    def test_decide_is_required_before_handoff(self) -> None:
        self.assertIn("approve/APPROVED.md", self.handoff)
        self.assertIn("先 `approve`", self.handoff)
        handoff_sec = self._section(self.skill, "## `handoff`")
        self.assertIn("已 `approve`", handoff_sec)

    def test_handoff_delegates_taskflow_same_slug(self) -> None:
        self.assertIn("taskflow-new", self.handoff)
        self.assertIn("driver change 名 = 任务 slug + `-driver`", self.handoff)
        self.assertIn("不发明", self.handoff)
        self.assertIn("不要写 `tasks.md`", self.handoff)
        self.assertIn("保持探索任务在 `ongoing/`", self.handoff)
        self.assertIn("已存在则不要新建", self.handoff)

    def test_handoff_does_not_archive(self) -> None:
        handoff_sec = self._section(self.skill, "## `handoff`")
        self.assertIn("不归档、不搬目录、不清绑定", handoff_sec)
        self.assertIn("不归档、不搬目录、不清绑定", self.handoff)

    def test_split_phase_is_routed_and_gated(self) -> None:
        self.assertIn("## `expand` / `split`", self.skill)
        split = self._section(self.skill, "## `expand` / `split`")
        self.assertIn("必须已绑定", split)
        self.assertIn("全局唯一", split)
        self.assertIn("只一层", split)
        self.assertIn("`parent:`", split)
        self.assertIn("必须评估一次", split)

    def test_subtask_terms_are_named(self) -> None:
        self.assertIn("**子任务**", self.skill)
        self.assertIn("**父任务**", self.skill)
        self.assertIn("**handed-off**", self.skill)
        self.assertIn("子 change", self.skill)

    def test_parent_forbidden_handoff(self) -> None:
        handoff_sec = self._section(self.skill, "## `handoff`")
        self.assertIn("父是纯伞不可交接", handoff_sec)
        self.assertIn("不建 `{parent}-driver`", handoff_sec)
        self.assertIn("不得建 `{parent}-driver`", self.handoff)

    def test_nested_layout_and_index_rows(self) -> None:
        self.assertIn("`{parent}/{sub}`", self.skill)
        tpl = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")
        self.assertIn("parent:", tpl)
        index = (ROOT / "references" / "templates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("{parent}/{sub}", index)

    def test_explore_hints_split_once(self) -> None:
        self.assertIn("提示一次", self.explore)
        self.assertIn("`split`", self.explore)

    def test_ledger_write_discipline_is_gated(self) -> None:
        self.assertIn("references/ledger.md", self.skill)
        self.assertIn("写台账", self.skill)
        for phrase in (
            "锚点串",
            "恰为 1",
            "整行替换",
            "列数与表头一致",
            "精确整行等值",
            "最大编号",
            "不静默改写",
        ):
            self.assertIn(phrase, self.ledger)

    def test_ledger_discipline_carves_out_batch_path_update(self) -> None:
        self.assertIn("父路径前缀", self.ledger)
        self.assertIn("archive-reopen.md", self.ledger)
        self.assertIn("archive-reopen.md", self.ledger)

    def test_goal_confirmations_go_to_review(self) -> None:
        section = self._section(self.skill, "## Goal 里的确认")
        self.assertIn("「审阅」", section)
        self.assertIn("不列选项", section)
        self.assertIn("不交给审阅放行", section)
        self.assertIn("处在 goal 里时不逐条问用户", self.skill)
        self.assertIn("## Goal 里", self.approve)
        self.assertIn("全部按默认冻结", self.decide)
        self.assertIn("不在 goal 里时执行本节", self.decide)
        self.assertIn("按推荐写成决定逐条列出", self.decide)
        self.assertIn("处在 goal 里时，不询问是否交接", self.handoff)

    def test_pending_degrade_gates_in_decide_and_handoff(self) -> None:
        # pending 降级只有用户能确认：approve 不冻结、handoff 不建 driver。
        self.assertIn("存在确认状态为 `pending` 的显式降级时**不得冻结**", self.approve)
        self.assertIn("只有用户点名接受该项、或明确说按降级表全部确认", self.approve)
        self.assertIn("审阅收敛、单独的「继续」、执行者或评审者的判断都不算确认", self.approve)
        self.assertIn("仍有 `pending` 就停在本门禁，**不创建 driver**", self.handoff)
        self.assertIn("只有用户点名接受该项、或明确说按降级表全部确认后才继续", self.handoff)

    def test_profile_snapshot_frozen_verbatim(self) -> None:
        self.assertIn("质量画像与显式降级原文快照", self.approve)
        self.assertIn("不得只留路径指针", self.approve)
        self.assertIn("先 `save` 补回", self.approve)
        self.assertIn("不编造", self.approve)

    def test_design_requires_rationale_for_structure_choices(self) -> None:
        # 架构 / 接口 / 技术栈的选择须有设计依据，写不出即入未决，不算设计完成。
        self.assertIn("## 设计依据（架构 / 接口 / 技术栈）", self.design)
        self.assertIn("选择 → 模式 / 原则 → 为何适用 → 可检后果", self.design)
        self.assertIn("写不出依据的选择列入未决", self.design)
        self.assertIn("写不出就列入未决，不算设计完成", self.design)
        self.assertIn("本任务不涉及这三类选择时写「不适用」并说明", self.design)
        self.assertIn("推荐方案的架构 / 接口 / 技术栈选择按「设计依据」逐条给出", self.design)
        self.assertIn("## 设计依据", self.design_template)
        self.assertIn("设计依据核对", self.plan_review)

    def test_commands_are_not_phase(self) -> None:
        self.assertIn("命令与 `TASK.md.phase`", self.skill)
        self.assertIn("禁止把命令名写入 `phase`", self.skill)
        self.assertIn("## 命令", self.skill)
        # 命令表标题不得再叫「阶段」
        self.assertNotIn("| 阶段 | 何时 | 写入 |", self.skill)

    def test_handoff_sets_phase_propose(self) -> None:
        self.assertIn("`phase` 改为 `propose`", self.handoff)
        self.assertIn("禁止把 `phase` 写成 `handoff`", self.handoff)
        handoff_sec = self._section(self.skill, "## `handoff`")
        self.assertIn("phase: propose", handoff_sec)

    def test_explore_light_vs_full(self) -> None:
        self.assertIn("仅 grill 与完整 explore", self.explore)
        self.assertIn("仅 grill", self.explore)
        explore_sec = self._section(self.skill, "## `explore`")
        self.assertIn("仅 grill", explore_sec)
        self.assertIn("完整 explore", explore_sec)

    def test_cmd_refs_exist(self) -> None:
        for rel in (
            "references/commands.md",
            "references/commands.md",
            "references/commands.md",
            "references/commands.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_explore_grills_quality_goal(self) -> None:
        self.assertIn("质量目标", self.explore)
        self.assertIn("追问验收方式或参照", self.explore)
        self.assertIn("供 design 阶段质量画像草稿吸收", self.explore)
        self.assertIn(
            "未覆盖的预期目标、成功标准、质量目标、范围、约束与未知",
            self.explore,
        )

    def test_template_and_handoff_flow_overview(self) -> None:
        tpl = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")
        self.assertIn("质量属性", tpl)
        self.assertIn("流程总览", tpl)
        self.assertIn("流程总览原文快照写入 driver 的 `proposal.md`", self.handoff)


class TestExternalPrecedentThinReference(unittest.TestCase):
    """外部参照钩子（原 external-precedent.md，已删）：细则唯一真源在 taskrail。"""

    def setUp(self) -> None:
        self.precedent = (ROOT / "references" / "explore-design.md").read_text(
            encoding="utf-8"
        )

    def test_points_to_taskrail(self) -> None:
        self.assertIn("taskrail/references/external-precedent.md", self.precedent)
        self.assertIn("唯一真源", self.precedent)

    def test_no_duplicated_rules(self) -> None:
        # 尝试/写入细则已搬走，不得在本文件复制第二份细则条文。
        self.assertNotIn("只追最会影响", self.precedent)
        self.assertNotIn("阅读最多两处原文", self.precedent)
        self.assertNotIn("对上原文", self.precedent)

    def test_phase_hooks_kept(self) -> None:
        self.assertIn("写对比表之前做一次", self.precedent)
        self.assertIn("会改方案走向", self.precedent)


class TestGrillAfterIntent(unittest.TestCase):
    def test_grill_narrowed(self) -> None:
        text = (ROOT / "references" / "explore-design.md").read_text(encoding="utf-8")
        self.assertIn("**意图已定**", text)
        self.assertIn("grill 不重问", text)
        self.assertIn("回 `task-intent` 纠偏", text)
        cmds = (ROOT / "references" / "commands.md").read_text(encoding="utf-8")
        self.assertIn("grill 在意图确认之后", cmds)


if __name__ == "__main__":
    unittest.main()
