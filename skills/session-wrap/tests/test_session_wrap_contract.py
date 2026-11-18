"""session-wrap 文本契约测试：锁定证据收尾、方案合成、缺口记账与分档授权。"""
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
        self.assertIn("随收尾方案一次确认", DETOUR)

    def test_findings_are_synthesized_into_one_ordered_plan(self) -> None:
        self.assertIn("把前面每一步的发现合成一个有序方案", SKILL)
        self.assertIn("不把问题清单丢回给用户", SKILL)
        self.assertIn("每个发现必须有一个归属", SKILL)
        self.assertIn("补验当前缺口 → 提交 → 台账与知识落点 → 衍生处理", SKILL)
        self.assertIn("同一发现只出现一次", SKILL)

    def test_confirmation_scope_follows_three_tiers(self) -> None:
        self.assertIn("收尾项直接做", SKILL)
        self.assertIn("一次确认覆盖方案内全部编号步骤", SKILL)
        self.assertIn("额外缺口只有用户点名才处理", SKILL)
        self.assertIn("按目标环境逐项明确授权", SKILL)
        self.assertIn("不随方案确认生效", SKILL)
        self.assertIn("中途新发现要加步骤或升级风险，重新确认", SKILL)
        self.assertIn("一次确认等于授权方案内全部编号步骤，不含「需单独授权」项", PLAN)

    def test_low_risk_wrap_up_does_not_wait_for_approval(self) -> None:
        self.assertIn("低风险、结论唯一的收尾记账与本次临时资源清理可以直接完成", SKILL)
        self.assertIn("直接完成并简要报告，不占用用户确认", SKILL)
        self.assertIn("停掉本会话启动的本机临时服务", SKILL)

    def test_unconfirmed_gaps_fall_back_to_the_ledger(self) -> None:
        self.assertIn("用户只授权收尾项时，把缺口写入当前任务的 `context/current.md`「未决问题」，不新建任务", SKILL)
        self.assertIn("写入 `context/current.md` 的「未决问题」表", PLAN)
        self.assertIn("`解决形式` 写「另开任务」或「不纳入」", PLAN)
        self.assertIn("不代写 `SUMMARY.md`", PLAN)
        self.assertIn("没有台账：留在会话交接，不新建文件", PLAN)

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
        self.assertIn("需单独授权", SKILL)
        self.assertIn("<合入 / push / 部署 / 删除>", SKILL)

    def test_output_is_compact_and_routable(self) -> None:
        for section in ("结论", "收尾方案", "额外缺口", "需单独授权", "恢复入口"):
            self.assertIn(section, SKILL)
        self.assertIn("按「证据 → 建议动作或落点」组织，空章节省略", SKILL)
        self.assertIn("每条一行", SKILL)
        self.assertIn("可选项最多三项", SKILL)
        self.assertIn("没有遗留事项时只报可结束，不创建额外报告文件", SKILL)
        self.assertNotIn("待你确认", SKILL)

    def test_adjacent_skills_keep_their_responsibilities(self) -> None:
        self.assertIn("`anti-lazy` 负责交付前的意图与差距检查", SKILL)
        self.assertIn("taskrail 任务的 `close` 负责 SUMMARY、状态和归档", SKILL)
        self.assertIn("不复制它们的产物", SKILL)


if __name__ == "__main__":
    unittest.main()
