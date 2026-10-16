"""taskflow 不可破契约：入口门、driver 协议、串行默认、自进化移出运行路径。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TaskflowContractTest(unittest.TestCase):
    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)

    def test_entry_gate(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("check_handoff.py", skill)
        self.assertIn("入口门", skill)
        self.assertTrue((ROOT / "scripts" / "check_handoff.py").is_file())

    def test_driver_protocol_verbatim_block(self) -> None:
        t = (ROOT / "references" / "driver-template.md").read_text(encoding="utf-8")
        self.assertIn("## Driver 协议", t)
        self.assertIn("skip_specs: true", t)
        self.assertIn("脚手架把 `tasks.md` 留给 propose 阶段", t)

    def test_serial_default(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("串行", skill)
        self.assertTrue((ROOT / "references" / "multi-worker.md").is_file())

    def test_self_evolution_out_of_runtime(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("self-evolution.md", skill)
        self.assertNotIn("## Self-evolution", skill)
        self.assertTrue((ROOT / "references" / "self-evolution.md").is_file())

    def test_old_packs_removed(self) -> None:
        for name in ("acceptance-rubric.md", "delivery-quality-loop.md", "implementer-isolation.md"):
            self.assertFalse((ROOT / "references" / name).exists(), name)

    def test_points_to_done(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("done.md", skill)


if __name__ == "__main__":
    unittest.main()
