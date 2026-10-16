"""完成清单与 wizard 必填四节。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DoneAndWizardTest(unittest.TestCase):
    def test_done_items(self) -> None:
        d = (ROOT / "references" / "done.md").read_text(encoding="utf-8")
        self.assertIn("判据成立", d)
        self.assertIn("做完的样子", d)
        self.assertIn("观感验收", d)
        self.assertIn("goal", d)
        self.assertIn("human", d)

    def test_wizard_required_four(self) -> None:
        w = (ROOT / "references" / "phase-wizard.md").read_text(encoding="utf-8")
        for s in ("## 目标", "## 完成判据", "## 步骤", "## 不做"):
            self.assertIn(s, w)
        self.assertIn("必填四节", w)

    def test_no_verbatim_snapshot_rule(self) -> None:
        for name in ("contract.md", "done.md", "phase-wizard.md"):
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("逐字复制", text)
            self.assertNotIn("原文快照", text)


if __name__ == "__main__":
    unittest.main()
