"""skill-upgrader 三模式契约（update / self-upgrade / evolve，读 SKILL.md + references 全文）。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
CORPUS = "\n".join(
    [SKILL] + [p.read_text(encoding="utf-8") for p in sorted((ROOT / "references").rglob("*.md"))]
)


class ModeGateContract(unittest.TestCase):
    def test_three_modes_in_gate(self) -> None:
        gate = SKILL.split("## 模式门禁（强制）", 1)[1].split("\n## ", 1)[0]
        for mode in ("`update`", "`self-upgrade`", "`evolve`"):
            self.assertIn(mode, gate)

    def test_description_keeps_old_trigger(self) -> None:
        head = SKILL.split("---", 2)[1]
        self.assertIn("skill-evolver", head)
        self.assertIn("evolve", head)

    def test_evolve_reference_loaded_from_skill(self) -> None:
        self.assertIn("references/evolve.md", SKILL)
        self.assertTrue((ROOT / "references" / "evolve.md").is_file())


class EvolveContract(unittest.TestCase):
    def test_evolve_writes_evolutions_and_needs_eval_decision(self) -> None:
        evolve = (ROOT / "references" / "evolve.md").read_text(encoding="utf-8")
        self.assertIn("evolutions/", evolve)
        self.assertIn("eval.md", evolve)
        self.assertIn("decision.md", evolve)

    def test_candidate_body_is_not_named_skill_md(self) -> None:
        evolve = (ROOT / "references" / "evolve.md").read_text(encoding="utf-8")
        self.assertIn("SKILL.md.candidate  # 候选正文", evolve)
        self.assertNotIn("  SKILL.md          # 候选正文", evolve)
        self.assertIn("用候选 `SKILL.md.candidate` 覆盖生产稿", evolve)

    def test_no_auto_evolution(self) -> None:
        self.assertIn("禁止自动进化", CORPUS)
        self.assertIn("禁止单次失败直接改 `SKILL.md`", CORPUS)


class UpdateContract(unittest.TestCase):
    def test_update_uses_patches_and_apply_check(self) -> None:
        self.assertIn("patches/", SKILL)
        self.assertIn("git apply --check", CORPUS)

    def test_missing_patches_dir_created_on_demand(self) -> None:
        self.assertIn("mkdir -p", CORPUS)


if __name__ == "__main__":
    unittest.main()
