"""task-explore 不可破契约：命令面、phase 禁写入命令名、handoff 指针、无 decide 壳。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(*p: str) -> str:
    return ROOT.joinpath(*p).read_text(encoding="utf-8")


class ExploreContractTest(unittest.TestCase):
    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)

    def test_public_commands(self) -> None:
        skill = read("SKILL.md")
        for cmd in ("explore", "design", "approve", "handoff"):
            self.assertIn(f"`{cmd}`", skill)
        self.assertNotIn("decide", skill)
        self.assertNotIn("plan-review", skill)
        self.assertFalse((ROOT / "references" / "commands.md").exists())

    def test_phase_not_command(self) -> None:
        skill = read("SKILL.md")
        self.assertIn("不是 `phase` 取值", skill)
        self.assertIn("handed-off", skill)
        self.assertIn("phase 置为 propose", skill)

    def test_handoff_pointers_only(self) -> None:
        h = read("references", "handoff.md")
        self.assertIn("指针与判据", h)
        self.assertIn("check_handoff.py", h)
        self.assertNotIn("逐字复制", h)

    def test_approve_exit(self) -> None:
        a = read("references", "approve.md")
        self.assertIn("下一步只写 handoff", a)

    def test_ledger_and_concurrency_split(self) -> None:
        self.assertTrue((ROOT / "references" / "ledger.md").is_file())
        self.assertTrue((ROOT / "references" / "ledger-concurrency.md").is_file())
        self.assertTrue((ROOT / "references" / "large-scope.md").is_file())

    def test_templates_core(self) -> None:
        t = read("references", "templates.md")
        self.assertIn("已做决定", t)
        self.assertIn("skip | full", t)


if __name__ == "__main__":
    unittest.main()
