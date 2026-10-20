"""task 族：归属、术语单真源、无 CONTEXT 双真源。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT.parent


class FamilyTest(unittest.TestCase):
    def test_skills_exist(self) -> None:
        for name in ("taskrail", "task-explore", "taskflow", "task-intent"):
            self.assertTrue((FAMILY / name / "SKILL.md").is_file(), name)

    def test_contract_is_glossary(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("## 术语", c)
        self.assertIn("完成判据", c)
        self.assertFalse((ROOT / "CONTEXT.md").exists())

    def test_confirm_is_thin(self) -> None:
        n = len((ROOT / "references" / "confirm-protocol.md").read_bytes())
        self.assertLess(n, 4000)

    def test_ownership_table(self) -> None:
        c = (ROOT / "references" / "contract.md").read_text(encoding="utf-8")
        self.assertNotIn("## Skill 归属", c)  # 归属只在 taskrail SKILL.md 开头一句
        c = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for s in ("taskrail", "task-intent", "task-explore", "taskflow"):
            self.assertIn(s, c)


if __name__ == "__main__":
    unittest.main()
