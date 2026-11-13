"""project-atlas 的文档与命令契约。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "atlasctl.py"
sys.path.insert(0, str(SCRIPT.parent))

import atlasctl  # noqa: E402


class ProjectAtlasContractTest(unittest.TestCase):
    def test_commands_match_skill(self) -> None:
        self.assertEqual(atlasctl.COMMANDS, {"init", "status", "verify", "build", "check"})
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for command in atlasctl.COMMANDS:
            self.assertIn(f"`{command}", text)

    def test_pyramid_and_self_healing_are_explicit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        layout = (ROOT / "references" / "layout.md").read_text(encoding="utf-8")
        maintenance = (ROOT / "references" / "maintenance.md").read_text(encoding="utf-8")
        for marker in ("domains/<domain>/index.md", "domains/<domain>/<topic>.md", "source_digest", "stale_pages"):
            self.assertIn(marker, skill)
        self.assertIn("L0", layout)
        self.assertIn("L1", layout)
        self.assertIn("L2", layout)
        self.assertIn("刷新摘要不能替代语义复核", skill)
        self.assertIn("check.ok=true", maintenance)

    def test_static_site_contract(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        maintenance = (ROOT / "references" / "maintenance.md").read_text(encoding="utf-8")
        self.assertIn("Markdown 是可编辑真源", skill)
        self.assertIn("_site/index.html", skill)
        self.assertIn("独立 HTML", maintenance)
        self.assertIn(".md", maintenance)

    def test_references_and_evals_exist(self) -> None:
        for rel in ("references/layout.md", "references/maintenance.md", "evals/cases.yaml"):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
