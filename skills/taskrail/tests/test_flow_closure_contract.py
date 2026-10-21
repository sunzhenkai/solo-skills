"""流程闭环：交接后的位置可推导、终点有完成通知与任务归档、full 档执行条件在定档时查。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent
CONTRACT = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class PostHandoffPositionTest(unittest.TestCase):
    def test_contract_derives_phase_from_driver(self) -> None:
        self.assertIn("## 交接后的位置", CONTRACT)
        for row in ("| `tasks.md` 还没有 | `propose` |", "| 有未勾项 | `apply` |",
                    "| 全勾、driver 未归档 | `archive` |", "| driver 已归档 | `done` |"):
            self.assertIn(row, CONTRACT)

    def test_resume_uses_derivation(self) -> None:
        self.assertIn("交接后的位置", SKILL)


class TerminalTest(unittest.TestCase):
    def test_full_path_ends_with_done(self) -> None:
        self.assertIn("propose → apply → archive → done", CONTRACT)

    def test_archive_term_disambiguated(self) -> None:
        self.assertIn("`phase: archive` 只指归档 driver", CONTRACT)
        self.assertIn("完成清单过为 `done`（做完归档后仍是 `done`）", CONTRACT)

    def test_done_sends_notice_then_archives(self) -> None:
        self.assertIn("发完成通知", SKILL)
        self.assertIn("同轮任务归档", SKILL)
        ur = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")
        self.assertIn("## 8. 完成通知", ur)
        self.assertIn("合入时", ur)

    def test_skip_upgrade_leftovers_reported(self) -> None:
        self.assertIn("完成通知里写明它已带进任务分支", CONTRACT)


class ReadinessAndDelegationTest(unittest.TestCase):
    def test_full_readiness_checked_at_tiering(self) -> None:
        w = (ROOT / "references" / "phase-wizard.md").read_text(encoding="utf-8")
        self.assertIn("定为 `full` 时当场查执行条件", w)
        self.assertIn("openspec init --tools none", w)

    def test_stock_stops_answered_by_orchestrator(self) -> None:
        cp = (ROOT / "references" / "confirm-protocol.md").read_text(encoding="utf-8")
        self.assertIn("不算停点", cp)
        self.assertIn("经 taskrail 委托时", cp)
        tf = (FAMILY / "taskflow" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## 经 taskrail 委托时", tf)

    def test_gate_checks_approval(self) -> None:
        self.assertIn("核对已批准、判据非空、driver 名、交接载荷", CONTRACT)


if __name__ == "__main__":
    unittest.main()
