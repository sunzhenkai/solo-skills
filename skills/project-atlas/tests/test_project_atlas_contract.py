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
        self.assertIn("独立静态 HTML", maintenance)
        self.assertIn(".md", maintenance)

    def test_archify_is_optional_and_finalize_is_required(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        diagrams = (ROOT / "references" / "diagrams.md").read_text(encoding="utf-8")
        self.assertIn("archify skill", skill)
        self.assertIn("diagrams/<slug>.json", skill)
        self.assertIn("affected_diagrams", skill)
        self.assertIn("可选依赖", diagrams)
        self.assertIn("node <archify-skill>/bin/archify.mjs finalize", diagrams)
        self.assertIn("SHA-256", diagrams)
        self.assertIn("不手改回执", diagrams)
        self.assertIn("--out-dir <review-dir>", diagrams)
        self.assertIn("规范摘要", diagrams)

    def test_default_project_root_is_docs_atlas(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("<project>/docs/atlas", skill)
        self.assertIn("显式 `--root` 可覆盖默认落点", skill)

    def test_complex_system_views_and_reading_acceptance_are_explicit(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        layout = (ROOT / "references" / "layout.md").read_text(encoding="utf-8")
        example = (ROOT / "examples" / "programmatic-advertising.md").read_text(encoding="utf-8")
        for marker in (
            "flows/<flow>.md",
            "architecture/<topic>.md",
            "data/<topic>.md",
            "cross-cutting/<topic>.md",
        ):
            self.assertIn(marker, skill)
        self.assertIn("两条阅读轴", layout)
        self.assertIn("复杂系统阅读验收", layout)
        self.assertIn("广告请求：从流量到反馈", example)
        self.assertIn("首批只保证", example)

    def test_wiki_data_boundary_and_handoff(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        maintenance = (ROOT / "references" / "maintenance.md").read_text(encoding="utf-8")
        for marker in ("wiki-data", "当前系统事实", "不自动写 wiki", "不复制其正文"):
            self.assertIn(marker, skill)
        self.assertIn("不依赖 wiki 外链", skill)
        self.assertIn("代码变化只更新 Atlas 当前事实", maintenance)
        self.assertIn("需 `wiki-data` 复核的主题", maintenance)

    def test_references_evals_and_examples_exist(self) -> None:
        for rel in (
            "references/layout.md",
            "references/maintenance.md",
            "references/diagrams.md",
            "evals/cases.yaml",
            "examples/programmatic-advertising.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
