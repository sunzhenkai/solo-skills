"""交付类别与 UI 包：下沉后只锁文件存在与入口指针。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


class OptionalPacksTest(unittest.TestCase):
    def test_ui_delivery_exists(self) -> None:
        text = (REF / "ui-delivery.md").read_text(encoding="utf-8")
        self.assertIn("ui_evidence_check.py", text)
        self.assertIn("--validate-review", text)
        self.assertIn("观感交付", text)

    def test_quality_appendix_exists(self) -> None:
        text = (REF / "quality-appendix.md").read_text(encoding="utf-8")
        self.assertIn("Web UI", text)
        self.assertIn("服务 / 后端", text)

    def test_gate_packs_removed(self) -> None:
        self.assertFalse((REF / "gate-packs.md").exists())
        self.assertFalse((REF / "quality-profile.md").exists())

    def test_skill_points_to_ui_pack(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ui-delivery.md", skill)
        self.assertIn("done.md", skill)


if __name__ == "__main__":
    unittest.main()
