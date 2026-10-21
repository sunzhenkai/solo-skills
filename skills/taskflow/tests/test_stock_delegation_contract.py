"""经 taskrail 委托 stock openspec-* 时由编排者代答，停不停只看停点表。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class StockDelegationTest(unittest.TestCase):
    def test_section_and_stop_table_pointer(self) -> None:
        self.assertIn("## 经 taskrail 委托时", SKILL)
        self.assertIn("confirm-protocol.md", SKILL)
        self.assertIn("停点", SKILL)

    def test_propose_then_apply(self) -> None:
        self.assertIn("approve 放行即授权 propose 与 apply", SKILL)

    def test_existing_change_continue(self) -> None:
        self.assertIn("选继续，不问", SKILL)

    def test_apply_pause_follows_driver_protocol(self) -> None:
        self.assertIn("该项保持未勾", SKILL)

    def test_sub_change_archive_noninteractive(self) -> None:
        self.assertIn("openspec archive {task}-<slice> --yes", SKILL)
        t = (ROOT / "references" / "driver-template.md").read_text(encoding="utf-8")
        self.assertIn("openspec archive {task}-<slice> --yes", t)


if __name__ == "__main__":
    unittest.main()
