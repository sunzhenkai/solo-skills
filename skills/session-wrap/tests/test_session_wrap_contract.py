"""session-wrap 文本契约测试：锁定完成度门禁、未完成三选一、先确认后执行、代码合入闭环、说人话输出、零遗留放手结论与逐项授权。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
INCOMPLETE = (ROOT / "references" / "incomplete-abort.md").read_text(encoding="utf-8")
PLAN = (ROOT / "references" / "plan-synthesis.md").read_text(encoding="utf-8")
MERGE = (ROOT / "references" / "branch-merge.md").read_text(encoding="utf-8")
RELEASE = (ROOT / "references" / "release-deploy.md").read_text(encoding="utf-8")
DETOUR = (ROOT / "references" / "detour-review.md").read_text(encoding="utf-8")


class SessionWrapContractTest(unittest.TestCase):
    def test_model_invocation_covers_session_wrap_and_abort_gate(self) -> None:
        self.assertIn("description: 会话收尾", SKILL)
        self.assertIn("准备结束会话或确认是否中止时", SKILL)
        self.assertNotIn("disable-model-invocation: true", SKILL)

    def test_no_action_without_confirmation(self) -> None:
        self.assertIn("只要涉及写文件、改 git、停服务、删资源或外部操作，一律先确认再动手", SKILL)
        self.assertIn("第一轮只做只读排查与列清单", SKILL)
        self.assertIn("即使清单里只有「准备帮你做」而没有选择题，也先亮出来等用户点头", SKILL)
        self.assertIn("只有完全无事可做时才直接结束", SKILL)
        self.assertNotIn("直接执行", SKILL)
        self.assertNotIn("没有需你选择的项时直接执行", SKILL)

    def test_completion_gate_and_incomplete_three_way_abort(self) -> None:
        self.assertIn("完成度裁决（第 0 步）", SKILL)
        self.assertIn("references/incomplete-abort.md", SKILL)
        self.assertIn("跳过合入主分支、打 tag、发版或部署等完成态检查", SKILL)
        for choice in ("继续做完", "暂停挂起", "彻底放弃"):
            self.assertIn(choice, SKILL)
            self.assertIn(choice, INCOMPLETE)
        self.assertIn("退出收尾", INCOMPLETE)
        self.assertIn("跳过完成态的代码合入主分支、打 tag、发版与部署检查", INCOMPLETE)

    def test_pause_preserves_context_and_abort_cleans_up_with_archived(self) -> None:
        self.assertIn("保留当前分支与 worktree", INCOMPLETE)
        self.assertIn("保持任务为 `active`", INCOMPLETE)
        self.assertIn("丢弃未提交改动、关闭草稿 MR/PR、删除临时分支与临时 worktree", INCOMPLETE)
        self.assertIn("状态为 `archived`，而非 `done`", INCOMPLETE)
        self.assertIn("暂停挂起不授权合入或删分支/worktree", SKILL)
        self.assertIn("放弃撤场涉及的丢弃改动、关 MR/PR 或删分支须逐项确认", SKILL)

    def test_code_delivery_loop_requires_merge_or_mr_check(self) -> None:
        self.assertIn("代码交付闭环", SKILL)
        self.assertIn("在非默认分支（或本地默认分支领先远端）且有未推送或未合入主分支的提交", SKILL)
        self.assertIn("references/branch-merge.md", SKILL)
        self.assertIn("推送并提 MR/PR", SKILL)
        self.assertIn("补验当前缺口 → 提交 → 推送与提 MR/PR 或合入主分支", SKILL)
        self.assertIn("repo-manager", SKILL)
        self.assertIn("commit-push", SKILL)

    def test_branch_merge_reference_covers_rules_and_execution(self) -> None:
        self.assertIn("不因工作区干净而跳过", MERGE)
        self.assertIn("逐仓核对", MERGE)
        self.assertIn("仓库硬规则与分支保护 > 用户本次明确选择 > 已确认的长期习惯", MERGE)
        for strategy in ("squash", "merge commit", "rebase merge", "直接合入默认分支"):
            self.assertIn(strategy, MERGE)
        self.assertIn("优先沿用并核对 CI / 评审状态，不重复创建", MERGE)
        self.assertIn("gh pr create", MERGE)
        self.assertIn("glab mr create", MERGE)
        self.assertIn("合并授权不自动包含 push", MERGE)
        self.assertIn("归为外部等待项", MERGE)

    def test_plain_language_and_zero_tail_closure_verdicts(self) -> None:
        self.assertIn("说人话", SKILL)
        self.assertIn("每条一行短句，空区块省略", SKILL)
        self.assertIn("第一轮尽量控制在半屏以内", SKILL)
        self.assertIn("两边不重复列选项", SKILL)
        self.assertIn("第一轮不下结束结论", SKILL)
        self.assertIn("用一句大白话交代现状并点明四种终态之一", SKILL)
        for verdict in ("**彻底收工**", "**本地收尾、剩外部等待**", "**已暂停挂起**", "**已确认中止**"):
            self.assertIn(verdict, SKILL)
        self.assertIn("不生成额外报告文件", SKILL)
        self.assertIn("第一轮示例 A", PLAN)
        self.assertIn("第一轮示例 B", PLAN)
        self.assertIn("第二轮示例 A", PLAN)
        self.assertIn("第二轮示例 B", PLAN)

    def test_original_requirements_and_real_evidence(self) -> None:
        self.assertIn("重读最初目标和最新要求", SKILL)
        self.assertIn("让每项明确要求对应到产物、回答或证据", SKILL)
        self.assertIn("原始场景和每项「必须」都要有结论", SKILL)
        self.assertIn("核心验收缺口留在本次处理", SKILL)
        self.assertIn("编译或静态检查不能替代原始场景验证", SKILL)
        self.assertIn("区分事实、推测和未知", SKILL)
        self.assertIn("纯问答或方案讨论只依据对话收尾", SKILL)
        self.assertIn("非代码交付", SKILL)
        self.assertIn("调试日志、mock、跳过校验开关或临时配置", SKILL)

    def test_findings_classify_and_scope_authorization(self) -> None:
        for group in ("**需要你拍板**", "**准备帮你做**", "**顺手记下的遗留（这次不做）**"):
            self.assertIn(group, SKILL)
        self.assertIn("每个发现只出现一次", SKILL)
        self.assertIn("推荐项放首位并附一句理由", SKILL)
        self.assertIn("外部或不可逆动作一项一题", SKILL)
        self.assertIn("提交不等于授权 push", SKILL)
        self.assertIn("push 不等于授权合入主分支", SKILL)
        self.assertIn("执行中新发现加项或风险升级时，停下来再问一轮", SKILL)
        self.assertIn("题干脱离上下文也能看懂", PLAN)
        self.assertIn("提交属于用户点名才做的动作", PLAN)

    def test_gaps_and_knowledge_routing_with_no_silent_chat_drop(self) -> None:
        self.assertIn("任务未收口：写入 `context/current.md` 的「未决问题」表", PLAN)
        self.assertIn("`解决形式` 写「另开任务」或「不纳入」", PLAN)
        self.assertIn("任务已收口或已归档：在 SUMMARY「剩余风险与后续项」末尾追加一行", PLAN)
        self.assertIn("只追加，不动原文其余部分", PLAN)
        self.assertIn("不默认静默留在聊天里", PLAN)
        self.assertIn("明确确认不跟踪、直接放弃", PLAN)
        self.assertIn("缺口记账不新建任务或子任务", PLAN)
        for route in ("project-atlas", "wiki-data", "skill-upgrader", "当前任务 SUMMARY"):
            self.assertIn(route, PLAN)
        self.assertIn("单次失败先留作经验", PLAN)
        self.assertIn("操作台账只记录有追溯价值的动作、环境、结果、影响和回滚方式", PLAN)

    def test_costly_troubleshooting_becomes_pitfall_candidates(self) -> None:
        self.assertIn("references/detour-review.md", SKILL)
        self.assertIn("做弯路复盘，产出坑候选", SKILL)
        for signal in ("`dead-end`", "用户纠正过排查方向", "最终根因与最初的猜测不同", "明显超出"):
            self.assertIn(signal, DETOUR)
        self.assertIn("都不命中则跳过", DETOUR)
        for question in ("**现象**", "**误判**", "**决定性证据**", "**最短路径**", "**可迁移规律**"):
            self.assertIn(question, DETOUR)
        self.assertIn("`kind: pitfall`", DETOUR)
        self.assertIn("准备帮你做", DETOUR)
        self.assertIn("用户确认后再执行", DETOUR)

    def test_cleanup_and_adjacent_skills_boundaries(self) -> None:
        self.assertIn("清理前先核对无未提交改动、无独有未推提交，未知文件保留", SKILL)
        self.assertIn("`anti-lazy` 负责交付前查意图差距", SKILL)
        self.assertIn("`taskrail` 的 `close` 负责任务 SUMMARY、状态和归档", SKILL)
        self.assertIn("不重复造轮子", SKILL)

    def test_code_delivery_loop_checks_release_and_deploy_on_project_signals(self) -> None:
        for expected in (
            "references/release-deploy.md",
            "命中发布或部署信号",
            "打 tag / 发布 / 部署",
            "打 tag / 发版",
            "合入不等于授权打 tag / 发版或部署",
            "打 tag / 发版不等于授权部署",
        ):
            self.assertIn(expected, SKILL)
        self.assertIn("打 tag / 发版", PLAN)
        self.assertIn("命中项目发布或部署信号时确认是否打 tag、发版或部署", PLAN)

    def test_release_deploy_reference_covers_signals_isolation_and_execution(self) -> None:
        for expected in (
            "未命中则跳过",
            "版本与 tag 现状",
            "渠道与目标环境",
            "生效验证与回滚指向",
            "伴随数据变更",
            "各自一题",
            "测试环境部署不等于授权生产部署",
            "部署不等于授权线上数据清理或迁移",
            "repo-manager",
        ):
            self.assertIn(expected, RELEASE)

    def test_decision_options_cover_execute_and_defer_and_split_data_ops(self) -> None:
        self.assertIn("须含「本次执行」与「暂不执行」", SKILL)
        self.assertIn("部署不等于授权线上数据变更", SKILL)
        for expected in (
            "覆盖完整决策空间（必须包含「本次执行」）",
            "互斥且有实质区分",
            "部署不等于授权线上数据清理/迁移",
            "不把同一结论换个说法拆成多个选项",
        ):
            self.assertIn(expected, PLAN)
        self.assertIn("选项完整性（不省略执行分支）", RELEASE)
        self.assertIn("同时包含「本次执行」与「暂不执行」方向", RELEASE)


    def test_push_gate_and_mock_verification_boundary(self) -> None:
        self.assertIn("必须先读取并遵守 `commit-push`", SKILL)
        self.assertIn("密钥扫描门禁", SKILL)
        self.assertIn("mock/单测环境下通过", RELEASE)
        self.assertIn("显式标注验证边界", RELEASE)


if __name__ == "__main__":
    unittest.main()
