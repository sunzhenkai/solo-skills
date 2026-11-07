"""lint_wiki.py 对本地 wiki 工作区的确定性检查。"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lint_wiki.py"


def load_lint_module():
    spec = importlib.util.spec_from_file_location("lint_wiki", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


lint_wiki = load_lint_module()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class LintWikiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.wiki = self.root / "wiki"
        write(
            self.wiki / "log.md",
            "---\ntitle: 操作日志\n---\n\n# 操作日志\n\n## [2026-09-15] init | 工作区初始化\n",
        )
        write(self.wiki / "overview.md", "---\ntitle: 总览\n---\n\n# 总览\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_lint(self, *extra: str) -> tuple[int, str]:
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = lint_wiki.main([str(self.root), *extra])
        return code, buf.getvalue()

    def test_clean_workspace_ok(self) -> None:
        write(
            self.wiki / "entities" / "northwind.md",
            "---\ntitle: Northwind\ntype: entity\ndate: 2026-09-15\nconfidence: medium\n---\n\n见 [[渐进披露]]\n",
        )
        write(
            self.wiki / "concepts" / "渐进披露.md",
            "---\ntitle: 渐进披露\ntype: concept\ndate: 2026-09-15\nconfidence: medium\n---\n\n案例 [[Northwind]]\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)
        self.assertIn("errors: 0", out)

    def test_dead_link_and_missing_frontmatter(self) -> None:
        write(
            self.wiki / "entities" / "orphan.md",
            "无 frontmatter\n\n[[Missing Page]]\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("dead_link", out)
        self.assertIn("missing_frontmatter", out)

    def test_duplicate_page_same_dir_only(self) -> None:
        body = "---\ntitle: Demo\ntype: concept\ndate: 2026-09-15\nconfidence: medium\n---\n\n# x\n"
        write(self.wiki / "concepts" / "A_Player.md", body.replace("Demo", "A"))
        write(self.wiki / "concepts" / "A Player.md", body.replace("Demo", "B"))
        write(
            self.wiki / "entities" / "A_Player.md",
            "---\ntitle: A Player\ntype: entity\ndate: 2026-09-15\nconfidence: medium\n---\n\n# e\n",
        )
        _, out = self.run_lint()
        self.assertIn("duplicate_page", out)
        self.assertRegex(out, r"concepts/.*归一化重名")

    def test_entity_concept_coupling_and_type_mismatch(self) -> None:
        write(
            self.wiki / "entities" / "青禾实验室.md",
            "---\ntitle: 青禾实验室\ntype: entity\ndate: 2026-09-15\nconfidence: medium\n---\n\n# e\n",
        )
        write(
            self.wiki / "concepts" / "青禾实验室方法论.md",
            "---\ntitle: 青禾实验室方法论\ntype: concept\ndate: 2026-09-15\nconfidence: medium\n---\n\n# c\n",
        )
        write(
            self.wiki / "entities" / "wrong-type.md",
            "---\ntitle: Wrong\ntype: concept\ndate: 2026-09-15\nconfidence: medium\n---\n\n# x\n",
        )
        write(self.wiki / "stray.md", "---\ntitle: Stray\ntype: entity\ndate: 2026-09-15\nconfidence: medium\n---\n\n# s\n")
        _, out = self.run_lint()
        self.assertIn("entity_concept_coupling", out)
        self.assertIn("type_dir_mismatch", out)
        self.assertIn("misplaced_wiki_page", out)

    def test_log_errors(self) -> None:
        write(
            self.wiki / "log.md",
            "---\ntitle: 操作日志\n---\n\n## [2026-09-16] ingest | newer\n## [2026-09-15] ingest | older\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("log_date_decreasing", out)

        write(
            self.wiki / "log.md",
            "---\ntitle: 操作日志\n---\n\n## [2026-09-15] ingest missing-pipe\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("log_format_invalid", out)

    def test_write_index(self) -> None:
        write(
            self.wiki / "entities" / "northwind.md",
            "---\ntitle: Northwind\ntype: entity\ndate: 2026-09-15\nconfidence: medium\ndescription: 示例组织\n---\n\n# e\n",
        )
        write(
            self.wiki / "experiences" / "verify-before-reuse.md",
            "---\ntitle: Verify before reuse\ntype: experience\ndate: 2026-09-15\nconfidence: high\nstatus: validated\nlast_verified: 2026-09-15\nreview_after: 2999-01-01\n---\n\n案例 [[Northwind]]\n",
        )
        write(
            self.wiki / "ledgers" / "northwind-decision.md",
            "---\ntitle: Northwind decision\ntype: ledger\ndate: 2026-09-15\nconfidence: medium\nstatus: active\n---\n\n对象 [[Northwind]]\n",
        )
        code, out = self.run_lint("--write-index")
        self.assertEqual(code, 0, out)
        index = (self.wiki / "index.md").read_text(encoding="utf-8")
        self.assertIn("实体 (entities)", index)
        self.assertIn("经验 (experiences)", index)
        self.assertIn("业务台账 (ledgers)", index)
        self.assertIn("Northwind", index)
        self.assertIn("Verify before reuse", index)
        self.assertIn("Northwind decision", index)
        self.assertIn("置信度 | 状态 | 核实日期 | 复审日期", index)
        self.assertIn("high | validated | 2026-09-15 | 2999-01-01", index)
        self.assertIn("wiki-data", index)

    def test_experience_and_ledger_require_status(self) -> None:
        for subdir, page_type in (("experiences", "experience"), ("ledgers", "ledger")):
            write(
                self.wiki / subdir / "incomplete.md",
                f"---\ntitle: Incomplete\ntype: {page_type}\ndate: 2026-09-15\nconfidence: medium\n---\n",
            )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertEqual(out.count("missing_frontmatter"), 2)
        self.assertIn("status", out)

    def test_confidence_is_required_and_validated(self) -> None:
        write(
            self.wiki / "concepts" / "missing-confidence.md",
            "---\ntitle: Missing confidence\ntype: concept\ndate: 2026-09-15\n---\n",
        )
        write(
            self.wiki / "concepts" / "invalid-confidence.md",
            "---\ntitle: Invalid confidence\ntype: concept\ndate: 2026-09-15\nconfidence: certain\n---\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("missing_frontmatter", out)
        self.assertIn("confidence", out)
        self.assertIn("confidence_invalid", out)

    def test_verification_requirements(self) -> None:
        write(
            self.wiki / "concepts" / "high-without-verification.md",
            "---\ntitle: High without verification\ntype: concept\ndate: 2026-09-15\nconfidence: high\n---\n",
        )
        write(
            self.wiki / "experiences" / "validated-without-review.md",
            "---\ntitle: Validated without review\ntype: experience\ndate: 2026-09-15\nconfidence: medium\nstatus: validated\nlast_verified: 2026-09-15\n---\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertEqual(out.count("verification_missing"), 2)
        self.assertIn("review_after", out)

    def test_date_validation_and_review_overdue(self) -> None:
        write(
            self.wiki / "concepts" / "invalid-date.md",
            "---\ntitle: Invalid date\ntype: concept\ndate: 2026-02-30\nconfidence: medium\n---\n",
        )
        write(
            self.wiki / "concepts" / "overdue.md",
            "---\ntitle: Overdue\ntype: concept\ndate: 2026-09-15\nconfidence: medium\nlast_verified: 2020-01-01\nreview_after: 2020-02-01\n---\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("date_invalid", out)
        self.assertIn("review_overdue", out)


if __name__ == "__main__":
    unittest.main()
