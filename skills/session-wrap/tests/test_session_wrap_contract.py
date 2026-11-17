"""session-wrap 文本契约测试：锁定证据收尾、衍生任务路由与写入确认。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


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

    def test_every_write_or_external_action_requires_scoped_confirmation(self) -> None:
        self.assertIn("「收尾」只授权只读检查与建议", SKILL)
        self.assertIn("执行任何建议前，先说明目标和范围并获得确认", SKILL)
        self.assertIn("创建任务、更新台账、写文档 / wiki、修改 skill", SKILL)
        self.assertIn("按目标环境逐项明确授权", SKILL)
        self.assertIn("一次确认只覆盖用户点名的动作或同范围动作组", SKILL)

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
        self.assertIn("分支合入：", SKILL)

    def test_output_is_compact_and_routable(self) -> None:
        for section in ("必须处理", "衍生问题", "值得沉淀", "待你确认", "交接"):
            self.assertIn(section, SKILL)
        self.assertIn("按「证据 → 建议动作或落点」组织，空章节省略", SKILL)
        self.assertIn("可选优化最多三项", SKILL)
        self.assertIn("没有遗留事项时只报可结束，不创建额外报告文件", SKILL)

    def test_adjacent_skills_keep_their_responsibilities(self) -> None:
        self.assertIn("`anti-lazy` 负责交付前的意图与差距检查", SKILL)
        self.assertIn("taskrail 任务的 `close` 负责 SUMMARY、状态和归档", SKILL)
        self.assertIn("不复制它们的产物", SKILL)


if __name__ == "__main__":
    unittest.main()
