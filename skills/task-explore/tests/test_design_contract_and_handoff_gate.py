"""design 门禁精简 + handoff 门与 check_handoff 接线。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DesignAndHandoffTest(unittest.TestCase):
    def test_design_no_force_two_options(self) -> None:
        d = (ROOT / "references" / "explore-design.md").read_text(encoding="utf-8")
        self.assertIn("design/", d)
        detail = (ROOT / "references" / "design-detail.md").read_text(encoding="utf-8")
        self.assertIn("只有一条可行路线时不凑第二个方案", detail)

    def test_no_verbatim_profile_copy(self) -> None:
        for name in ("explore-design.md", "handoff.md", "templates.md"):
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("逐字复制", text)

    def test_handoff_wires_check(self) -> None:
        h = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        self.assertIn("check_handoff.py", h)
        self.assertIn("交付类别", h)
        self.assertIn("适用门包", h)


if __name__ == "__main__":
    unittest.main()
