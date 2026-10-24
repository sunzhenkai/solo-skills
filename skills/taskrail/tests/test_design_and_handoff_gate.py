"""design 门禁精简 + handoff 门与 check_handoff 接线。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DesignAndHandoffTest(unittest.TestCase):
    def test_design_no_force_two_options(self) -> None:
        d = (ROOT / "references" / "design.md").read_text(encoding="utf-8")
        self.assertIn("design/", d)
        detail = (ROOT / "references" / "design-detail.md").read_text(encoding="utf-8")
        self.assertIn("只有一条可行路线时不凑第二个方案", detail)

    def test_no_verbatim_profile_copy(self) -> None:
        for name in ("design.md", "handoff.md", "templates.md"):
            text = (ROOT / "references" / name).read_text(encoding="utf-8")
            self.assertNotIn("逐字复制", text)

    def test_handoff_wires_check(self) -> None:
        h = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        self.assertIn("check_handoff.py", h)
        self.assertIn("交付类别", h)
        self.assertIn("适用门包", h)

    def test_handoff_gate_before_driver(self) -> None:
        """新入口门：active + openspec + execute → 跑 check → 建 driver。"""
        h = (ROOT / "references" / "handoff.md").read_text(encoding="utf-8")
        steps = h.split("## 步骤", 1)[1]
        i_status = steps.index("status: active")
        i_check = steps.index("check_handoff.py")
        i_driver = steps.index("建 driver")
        self.assertLess(i_status, i_check)
        self.assertLess(i_check, i_driver)
        self.assertIn("execution: openspec", steps)
        self.assertIn("不写 handed-off / phase", steps)


if __name__ == "__main__":
    unittest.main()
