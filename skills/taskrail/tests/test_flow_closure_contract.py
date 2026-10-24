"""恢复与收口：driver 归档不等于 done，验证、总结和任务归档独立成立。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent
CONTRACT = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class RecoveryTest(unittest.TestCase):
    def test_resume_reconciles_artifacts_not_driver_phase(self) -> None:
        ledger = (ROOT / "references" / "ledger.md").read_text(encoding="utf-8")
        self.assertIn("reconcile", ledger)
        self.assertIn("不映射回固定双流程", ledger)
        self.assertIn("repair 回 active / close", ledger)
        self.assertIn("driver 归档、目录位置或 checkbox 全勾都不能单独推出 done", SKILL)

    def test_driver_archival_routes_back_to_verify_or_close(self) -> None:
        self.assertIn("driver 归档后若未验收", CONTRACT)
        self.assertIn("绝不能直接推导 done", CONTRACT)
        flow = (FAMILY / "taskflow" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("driver 归档后回 taskrail verify / close", flow)


class TerminalTest(unittest.TestCase):
    def test_close_requires_summary_verification_and_archive(self) -> None:
        close = (ROOT / "references" / "close.md").read_text(encoding="utf-8")
        self.assertIn("SUMMARY.md", close)
        self.assertIn("verify 全过", close)
        self.assertIn("同轮归档整棵任务树", close)
        self.assertIn("未完成关闭不伪写成功总结", close)

    def test_driver_and_task_archive_are_distinct(self) -> None:
        archive = (ROOT / "references" / "archive-reopen.md").read_text(encoding="utf-8")
        self.assertIn("driver 已在 workspace openspec 中归档不等于任务可归档", archive)
        self.assertIn("status done", archive)
        self.assertIn("status archived", archive)

    def test_completion_notice_includes_integration_and_merge(self) -> None:
        report = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")
        self.assertIn("## 6. 完成通知", report)
        self.assertIn("合入时", report)
        self.assertIn("父任务只发一次总完成通知", report)
        self.assertIn("不自动 push 或清理 worktree", report)


class ExecutionReadinessTest(unittest.TestCase):
    def test_openspec_dependencies_checked_only_when_selected(self) -> None:
        handoff = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        flow = (FAMILY / "taskflow" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("只有 `execution: openspec`", handoff)
        self.assertIn("缺 skill / CLI 时说明安装", flow)
        self.assertIn("direct 不建 driver", handoff)

    def test_stock_pauses_are_handled_by_orchestrator(self) -> None:
        confirm = (ROOT / "references" / "confirm-protocol.md").read_text(encoding="utf-8")
        flow = (FAMILY / "taskflow" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("不算额外停点", confirm)
        self.assertIn("## 经 taskrail 委托时", flow)
        self.assertIn("同名 change 选继续，不问", flow)

    def test_gate_checks_approval_or_explicit_not_required_reason(self) -> None:
        self.assertIn("not-required", CONTRACT)
        handoff = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        self.assertIn("criterion 非空", handoff)
        self.assertIn("reviews/APPROVED.md", handoff)


if __name__ == "__main__":
    unittest.main()
