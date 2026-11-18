"""session-wrap 文本契约测试：锁定证据收尾、收尾清单、两轮确认、缺口记账与逐项授权。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
PLAN = (ROOT / "references" / "plan-synthesis.md").read_text(encoding="utf-8")
DETOUR = (ROOT / "references" / "detour-review.md").read_text(encoding="utf-8")


class SessionWrapContractTest(unittest.TestCase):
    def test_model_invocation_covers_session_wrap_and_review(self) -> None:
        self.assertIn("description: 会话收尾", SKILL)
        self.assertIn("准备结束会话或要求复盘时", SKILL)
        self.assertNotIn("disable-model-invocation: true", SKILL)

    def test_original_requirements_map_to_deliverables_and_evidence(self) -> None:
        self.assertIn("重读最初目标和最新要求", SKILL)
        self.assertIn("让每项明确要求对应到产物、回答或证据", SKILL)
        self.assertIn("已完成且已验证", SKILL)
        self.assertIn("已完成但未验证", SKILL)
        self.assertIn("原始场景和每项「必须」都有结论", SKILL)

    def test_evidence_collection_is_scoped_to_actual_work(self) -> None:
        for signal in ("有代码改动", "有任务台账", "有外部操作", "有后台活动", "纯问答或方案讨论"):
            self.assertIn(signal, SKILL)
        self.assertIn("区分事实、推测和未知", SKILL)
        self.assertIn("验证不足时建议补验", SKILL)

    def test_current_delivery_gaps_stay_in_current_scope(self) -> None:
        self.assertIn("影响当前目标或 criterion 的问题留在当前交付中处理", SKILL)
        self.assertIn("没有转成后续事项来规避本次交付", SKILL)

    def test_unrelated_findings_use_existing_task_mechanism(self) -> None:
        self.assertIn("与本次目标无关的旧 bug、技术债、文档缺漏或环境隐患", SKILL)
        self.assertIn("使用 taskrail：建议新建独立任务", SKILL)
        self.assertIn("已有 Issue 等 tracker：建议使用同一机制", SKILL)
        self.assertIn("先检索相关记录，已有则补充证据与关联来源", SKILL)
        self.assertIn("没有发现任务机制：把问题留在交接信息中", SKILL)
        for field in ("问题、来源、证据、影响", "复现方式", "建议判据", "相关路径"):
            self.assertIn(field, SKILL)

    def test_knowledge_has_specific_reusable_destinations(self) -> None:
        self.assertIn("只沉淀跨任务仍有价值、现有文档尚未表达的内容", SKILL)
        for route in ("project-atlas", "wiki-data", "skill-upgrader", "当前任务 SUMMARY"):
            self.assertIn(route, SKILL)
        self.assertIn("单次失败先留作经验", SKILL)
        self.assertIn("操作台账记录有追溯价值的动作、环境、结果、影响和回滚方式", SKILL)

    def test_costly_troubleshooting_becomes_searchable_pitfall_candidates(self) -> None:
        self.assertIn("references/detour-review.md", SKILL)
        self.assertIn("做弯路复盘，产出坑候选", SKILL)
        for signal in ("`dead-end`", "用户纠正过排查方向", "最终根因与最初的猜测不同", "明显超出"):
            self.assertIn(signal, DETOUR)
        self.assertIn("都不命中则跳过", DETOUR)
        self.assertIn("优先读 `trouble-grill` 已落盘的排查记录", DETOUR)
        for question in ("**现象**", "**误判**", "**决定性证据**", "**最短路径**", "**可迁移规律**"):
            self.assertIn(question, DETOUR)
        for field in ("现象词：", "误判：", "最短判别：", "根因：", "模式候选：", "证据："):
            self.assertIn(field, DETOUR)
        self.assertIn("`kind: pitfall`", DETOUR)
        self.assertIn("建议用 `skill-upgrader` 改进排查 skill", DETOUR)
        self.assertIn("随本轮确认执行", DETOUR)

    def test_findings_become_one_wrap_list(self) -> None:
        self.assertIn("把前面每一步的发现合成一张收尾清单", SKILL)
        self.assertIn("每个发现只有一个归属", SKILL)
        for kind in ("**直接执行**", "**需你选择**", "**缺口**"):
            self.assertIn(kind, SKILL)
        self.assertIn("补验当前缺口 → 提交 → 台账与知识落点 → 衍生处理", SKILL)
        self.assertIn("同一发现只出现一次", PLAN)

    def test_two_rounds_confirm_once_and_scope_each_choice(self) -> None:
        self.assertIn("第一轮只列清单与提问，不执行收尾动作", SKILL)
        self.assertIn("用户一次回答覆盖本轮清单", SKILL)
        self.assertIn("每题的选择只授权该项", SKILL)
        self.assertIn("题干写明目标环境", SKILL)
        self.assertIn("只有用户点名才处理", SKILL)
        self.assertIn("执行中新发现要加项或升级风险，再问一轮", SKILL)
        self.assertIn("选了提交不等于授权 push", PLAN)
        self.assertIn("缺口不因确认而处理", PLAN)

    def test_undecided_items_get_options_with_a_recommendation(self) -> None:
        self.assertIn("推荐项放首位并附一句理由", SKILL)
        self.assertIn("同类事项合成一题", SKILL)
        self.assertIn("宿主有结构化提问工具时", SKILL)
        self.assertIn("题干脱离上下文也能看懂", PLAN)
        self.assertIn("外部或不可逆动作一项一题", PLAN)
        self.assertIn("能由规则、证据或用户已确认的偏好定下来的，归入直接执行，不提问", PLAN)
        self.assertIn("提交属于用户点名才做的动作，始终作为需你选择的一题", PLAN)

    def test_deterministic_items_are_listed_not_asked(self) -> None:
        self.assertIn("只列出，不提问", SKILL)
        self.assertIn("没有需你选择的项时直接执行并进入第二轮", SKILL)
        self.assertIn("停掉本会话启动的本机临时服务", SKILL)

    def test_gaps_are_recorded_by_task_state(self) -> None:
        self.assertIn("记账本身是直接执行项", SKILL)
        self.assertIn("按执行时的任务状态取落点", PLAN)
        self.assertIn("任务未收口：写入 `context/current.md` 的「未决问题」表", PLAN)
        self.assertIn("`解决形式` 写「另开任务」或「不纳入」", PLAN)
        self.assertIn("任务已收口或已归档：在 SUMMARY「剩余风险与后续项」追加一行", PLAN)
        self.assertIn("只追加，不改写 SUMMARY 其余部分", PLAN)
        self.assertIn("都没有：只留在第二轮的缺口列表，不新建文件", PLAN)
        self.assertIn("记账不新建任务或子任务", PLAN)

    def test_cleanup_recommendations_preserve_unique_work(self) -> None:
        self.assertIn("先核对未提交改动、独有提交及使用中的资源，未知文件保留", SKILL)

    def test_merge_recommendation_uses_rules_habits_and_commit_shape(self) -> None:
        self.assertIn("### 4. 推荐分支合入", SKILL)
        for evidence in ("已有 MR / PR", "CI / 评审", "分支保护", "仓库历史合入方式", "提交结构"):
            self.assertIn(evidence, SKILL)
        self.assertIn("用户习惯只采用本次明确选择或已确认的长期偏好", SKILL)
        self.assertIn("仓库硬规则与分支保护 > 用户本次明确选择 > 已确认的长期习惯", SKILL)
        self.assertIn("给出一个主推荐，不只罗列选项", SKILL)

    def test_merge_recommendation_covers_strategy_and_scoped_approval(self) -> None:
        self.assertIn("优先沿用，不重复创建", SKILL)
        for strategy in ("squash", "merge commit", "rebase merge", "直接合入"):
            self.assertIn(strategy, SKILL)
        self.assertIn("推荐包含合入通道与历史处理方式，例如 `MR + squash`", SKILL)
        self.assertIn("共享主分支仍需单独确认，push 不随合并自动授权", SKILL)

    def test_output_has_two_rounds(self) -> None:
        self.assertIn("第一轮（确认前，不下结论）", SKILL)
        self.assertIn("第二轮（执行后）", SKILL)
        for section in ("收尾清单", "将直接执行", "需你选择", "缺口（将记入 <落点>）"):
            self.assertIn(section, SKILL)
        for section in ("结论：可结束 / 仍有阻塞", "收尾结果", "缺口列表", "记在 <路径>", "恢复入口"):
            self.assertIn(section, SKILL)
        self.assertIn("证据只作为条目依据出现，不单列验证流水", SKILL)
        self.assertIn("每条一行", SKILL)
        self.assertIn("2–3 个选项", SKILL)
        self.assertIn("没有遗留事项时只报可结束，不创建额外报告文件", SKILL)
        self.assertNotIn("待你确认", SKILL)

    def test_counterexamples_cover_premature_close_and_unrecorded_gaps(self) -> None:
        self.assertIn("先报「可结束」，再把未定的提交、清理列在后面", PLAN)
        self.assertIn("单列一段「已核对事实」复述验证流水", PLAN)
        self.assertIn("列成被动的「需授权」清单就结束", PLAN)
        self.assertIn("没有实际记账，也没写落点", PLAN)

    def test_adjacent_skills_keep_their_responsibilities(self) -> None:
        self.assertIn("`anti-lazy` 负责交付前的意图与差距检查", SKILL)
        self.assertIn("taskrail 任务的 `close` 负责 SUMMARY、状态和归档", SKILL)
        self.assertIn("不复制它们的产物", SKILL)


if __name__ == "__main__":
    unittest.main()
