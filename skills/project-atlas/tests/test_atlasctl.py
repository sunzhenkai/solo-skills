"""atlasctl 的端到端行为，使用临时目录而非真实项目。"""

from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "atlasctl.py"
sys.path.insert(0, str(SCRIPT.parent))

import atlasctl  # noqa: E402


class AtlasctlTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        (self.project / "src").mkdir()
        (self.project / "src" / "orders.py").write_text("def submit():\n    return 'created'\n", encoding="utf-8")
        self.atlas = self.project / "docs" / "atlas"
        self.run_cli("init", "--root", str(self.atlas), "--source", str(self.project), "--confirm")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, dict]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = atlasctl.main(list(args))
        return code, json.loads(output.getvalue())

    def write_page(self, rel: str, content: str) -> None:
        path = self.atlas / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def make_main_flow(self) -> None:
        (self.atlas / "domains" / "core" / "index.md").unlink()
        (self.atlas / "domains" / "core").rmdir()
        self.write_page(
            "index.md",
            """---
title: 商店
level: 0
status: draft
sources: []
source_digest:
verified_commit:
---
# 商店

- [交易领域](domains/trade/index.md)
""",
        )
        self.write_page(
            "domains/trade/index.md",
            """---
title: 交易
level: 1
status: draft
sources:
  - src/orders.py
source_digest:
verified_commit:
---
# 交易

- [下单](submit.md)
- [架构图](../../assets/diagrams/trade.html)

[返回总览](../../index.md)
""",
        )
        self.write_page(
            "domains/trade/submit.md",
            """---
title: 下单
level: 2
status: draft
sources:
  - src/orders.py
source_digest:
verified_commit:
---
# 下单

提交后创建订单，失败时不产生订单。

[返回交易](index.md)
""",
        )
        self.write_page(
            "assets/diagrams/trade.html",
            '<html><body><a href="../../domains/trade/submit.md">下单详情</a></body></html>',
        )

    def verify_all(self) -> None:
        code, result = self.run_cli(
            "verify",
            "--root",
            str(self.atlas),
            "--page",
            "index.md",
            "domains/trade/index.md",
            "domains/trade/submit.md",
        )
        self.assertEqual(code, 0, result)

    def refresh_archify_receipts(self, slug: str = "trade") -> None:
        artifact = self.atlas / "diagrams" / f"{slug}.html"
        source = artifact.with_suffix(".json")

        def binding(path: Path) -> dict[str, object]:
            content = path.read_bytes()
            return {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}

        specification = binding(source)
        diagram = binding(artifact)
        self.write_page(
            f"diagrams/{slug}.delivery.json",
            json.dumps(
                {
                    "status": "current",
                    "command": "deliver",
                    "specification": specification,
                    "artifact": diagram,
                }
            ),
        )
        self.write_page(
            f"diagrams/{slug}.finalize-summary.json",
            json.dumps(
                {
                    "ok": True,
                    "command": "finalize",
                    "specification": specification,
                    "artifact": diagram,
                }
            ),
        )

    def make_archify_diagram(self, slug: str = "trade") -> None:
        self.write_page(
            f"diagrams/{slug}.json",
            json.dumps({"meta": {"output": f"diagrams/{slug}.html"}, "nodes": []}),
        )
        self.write_page(f"diagrams/{slug}.html", "<html><body>interactive diagram</body></html>")
        self.refresh_archify_receipts(slug)
        domain = self.atlas / "domains/trade/index.md"
        domain.write_text(
            domain.read_text(encoding="utf-8").replace(
                "\n[返回总览]", f"\n- [交互图](../../diagrams/{slug}.html)\n\n[返回总览]"
            ),
            encoding="utf-8",
        )

    def test_build_static_site_and_rewrite_links(self) -> None:
        self.make_main_flow()
        self.verify_all()
        code, result = self.run_cli("build", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)
        index = (self.atlas / "_site" / "index.html").read_text(encoding="utf-8")
        topic = (self.atlas / "_site" / "domains" / "trade" / "submit.html").read_text(encoding="utf-8")
        diagram = (self.atlas / "_site" / "assets" / "diagrams" / "trade.html").read_text(encoding="utf-8")
        self.assertIn('href="domains/trade/index.html"', index)
        self.assertIn('href="index.html"', topic)
        self.assertIn('href="../../domains/trade/submit.html"', diagram)
        self.assertIn("由 project-atlas 生成", topic)
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)

    def test_archify_build_publishes_only_html(self) -> None:
        self.make_main_flow()
        self.make_archify_diagram()
        self.verify_all()
        code, result = self.run_cli("build", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["diagrams"], 1)
        self.assertTrue((self.atlas / "_site" / "diagrams" / "trade.html").is_file())
        self.assertFalse((self.atlas / "_site" / "diagrams" / "trade.json").exists())
        self.assertFalse((self.atlas / "_site" / "diagrams" / "trade.delivery.json").exists())
        self.assertFalse((self.atlas / "_site" / "diagrams" / "trade.finalize-summary.json").exists())
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)

    def test_archify_source_change_requires_finalize(self) -> None:
        self.make_main_flow()
        self.make_archify_diagram()
        self.verify_all()
        (self.project / "src" / "orders.py").write_text("def submit():\n    return 'pending'\n", encoding="utf-8")
        code, result = self.run_cli("status", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)
        self.assertEqual(result["affected_diagrams"], ["diagrams/trade.html"])
        source = self.atlas / "diagrams" / "trade.json"
        source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        code, result = self.run_cli(
            "verify", "--root", str(self.atlas), "--page", "domains/trade/index.md"
        )
        self.assertEqual(code, 1)
        self.assertIn("diagram_specification_mismatch:diagrams/trade.html", result["errors"])
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.refresh_archify_receipts()
        self.verify_all()
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)

    def test_archify_pending_or_missing_receipt_blocks_delivery(self) -> None:
        self.make_main_flow()
        self.make_archify_diagram()
        self.write_page("diagrams/trade.delivery-pending.json", "{}")
        code, result = self.run_cli(
            "verify", "--root", str(self.atlas), "--page", "domains/trade/index.md"
        )
        self.assertEqual(code, 1)
        self.assertIn("diagram_delivery_pending:diagrams/trade.html", result["errors"])
        (self.atlas / "diagrams" / "trade.delivery-pending.json").unlink()
        (self.atlas / "diagrams" / "trade.finalize-summary.json").unlink()
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.assertIn("diagram_finalize_missing:diagrams/trade.html", result["errors"])

    def test_source_change_requires_semantic_reverification(self) -> None:
        self.make_main_flow()
        self.verify_all()
        (self.project / "src" / "orders.py").write_text("def submit():\n    return 'pending'\n", encoding="utf-8")
        code, result = self.run_cli("status", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)
        self.assertEqual(
            set(result["stale_pages"]),
            {"domains/trade/index.md", "domains/trade/submit.md"},
        )
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.verify_all()
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 0, result)

    def test_missing_mapping_and_broken_link_fail(self) -> None:
        self.make_main_flow()
        self.verify_all()
        (self.project / "src" / "orders.py").unlink()
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.assertTrue(any("source_mapping_missing" in error for error in result["errors"]))
        code, result = self.run_cli(
            "verify", "--root", str(self.atlas), "--page", "domains/trade/index.md"
        )
        self.assertEqual(code, 1)
        self.write_page(
            "domains/trade/submit.md",
            (self.atlas / "domains/trade/submit.md").read_text(encoding="utf-8") + "\n[缺失](missing.md)\n",
        )
        code, result = self.run_cli("build", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.assertTrue(any("broken_link" in error for error in result["errors"]))

    def test_new_topic_must_join_pyramid(self) -> None:
        self.make_main_flow()
        self.verify_all()
        self.write_page(
            "domains/trade/refund.md",
            """---
title: 退款
level: 2
status: draft
sources:
  - src/orders.py
source_digest:
verified_commit:
---
# 退款

[返回交易](index.md)
""",
        )
        code, result = self.run_cli("check", "--root", str(self.atlas))
        self.assertEqual(code, 1)
        self.assertIn("topic_not_linked_from_domain:domains/trade/refund.md", result["errors"])

    def test_default_root_is_docs_atlas_and_explicit_root_wins(self) -> None:
        other_project = Path(self.tmp.name) / "other-project"
        other_project.mkdir()
        code, result = self.run_cli("init", "--source", str(other_project), "--confirm")
        self.assertEqual(code, 0, result)
        self.assertEqual(Path(result["root"]), other_project / "docs" / "atlas")
        self.assertEqual(atlasctl.parser().parse_args(["status"]).root, "docs/atlas")
        self.assertEqual(atlasctl.parser().parse_args(["verify", "--page", "index.md"]).root, "docs/atlas")
        custom = Path(self.tmp.name) / "custom-atlas"
        code, result = self.run_cli(
            "init", "--source", str(other_project), "--root", str(custom), "--confirm"
        )
        self.assertEqual(code, 0, result)
        self.assertEqual(Path(result["root"]), custom)

    def test_init_requires_confirmation_and_preserves_existing_directory(self) -> None:
        other = Path(self.tmp.name) / "other-atlas"
        code, result = self.run_cli("init", "--root", str(other), "--source", str(self.project))
        self.assertEqual(code, 2)
        self.assertTrue(result["confirmation_required"])
        occupied = Path(self.tmp.name) / "occupied"
        occupied.mkdir()
        (occupied / "keep.txt").write_text("keep", encoding="utf-8")
        code, result = self.run_cli(
            "init", "--root", str(occupied), "--source", str(self.project), "--confirm"
        )
        self.assertEqual(code, 1)
        self.assertEqual((occupied / "keep.txt").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
