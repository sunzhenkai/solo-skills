"""ui_evidence_check.py：manifest 校验、report schema、评审文件核对，及可选真实浏览器冒烟。

真实浏览器冒烟需要 playwright（含 chromium）与 axe-core：设置 UI_EVIDENCE_AXE_JS 指向 axe.min.js；
缺任一项则 skip（CI 只跑纯标准库部分）。
"""

from __future__ import annotations

import importlib.util
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ui_evidence_check.py"
spec = importlib.util.spec_from_file_location("ui_evidence_check", SCRIPT)
uec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uec)  # type: ignore[union-attr]

STATES = {s: {"path": f"/?state={s}"} for s in uec.REQUIRED_STATES}


def manifest(**over):
    m = {"routes": [{"name": "home", "path": "/", "states": dict(STATES)}]}
    m.update(over)
    return m


def fake_report(ok_cell=True, viewports=None):
    vps = viewports or uec.DEFAULT_VIEWPORTS
    cell = {"screenshot": "x.png", "axe": {"violations": []}}
    rep = {
        "schema": uec.SCHEMA, "run_id": "r", "base_url": "http://x", "started_at": "t",
        "viewports": vps,
        "routes": [{"name": "home", "path": "/", "not_applicable": {},
                    "states": {s: {v["name"]: dict(cell) for v in vps} for s in uec.REQUIRED_STATES},
                    "focus_walk": {v["name"]: {"order": ["a"], "invisible": []} for v in vps}}],
    }
    if not ok_cell:
        rep["routes"][0]["states"]["error"]["mobile"] = {
            "screenshot": "e.png", "axe": {"violations": [{"id": "color-contrast", "impact": "serious", "nodes": 2}]}}
    rep["summary"] = uec.summarize(rep)
    return rep


class TestManifest(unittest.TestCase):

    def test_valid(self) -> None:
        self.assertEqual(uec.validate_manifest(manifest()), [])

    def test_missing_state(self) -> None:
        m = manifest()
        del m["routes"][0]["states"]["empty"]
        self.assertTrue(any("缺态 empty" in e for e in uec.validate_manifest(m)))

    def test_not_applicable_needs_reason(self) -> None:
        m = manifest()
        del m["routes"][0]["states"]["loading"]
        m["routes"][0]["not_applicable"] = {"loading": ""}
        self.assertTrue(any("not_applicable.loading" in e for e in uec.validate_manifest(m)))
        m["routes"][0]["not_applicable"] = {"loading": "静态页无异步加载"}
        self.assertEqual(uec.validate_manifest(m), [])

    def test_viewports(self) -> None:
        errs = uec.validate_manifest(manifest(viewports=[{"name": "d", "width": 1280, "height": 800}]))
        self.assertTrue(any("至少 2" in e for e in errs))
        errs = uec.validate_manifest(manifest(viewports=[{"name": "d", "width": 1280, "height": 800},
                                                         {"name": "t", "width": 768, "height": 1024}]))
        self.assertTrue(any("375x812" in e for e in errs))

    def test_bad_action(self) -> None:
        m = manifest()
        m["routes"][0]["states"]["error"] = {"actions": [{"hover": "#x"}]}
        self.assertTrue(any("actions[0]" in e for e in uec.validate_manifest(m)))

    def test_cli_validate_only(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.json"
            p.write_text(json.dumps(manifest()), encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), str(p), "--validate-only"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout)
            p.write_text(json.dumps({"routes": []}), encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), str(p), "--validate-only"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


class TestReport(unittest.TestCase):

    def test_schema_ok(self) -> None:
        rep = fake_report()
        self.assertEqual(uec.validate_report(rep), [])
        self.assertTrue(rep["summary"]["ok"])

    def test_blocking_axe_fails(self) -> None:
        s = fake_report(ok_cell=False)["summary"]
        self.assertFalse(s["ok"])
        self.assertEqual(s["axe_blocking"], 1)

    def test_missing_state_and_viewport(self) -> None:
        rep = fake_report(viewports=[{"name": "desktop", "width": 1280, "height": 800},
                                     {"name": "tablet", "width": 768, "height": 1024}])
        del rep["routes"][0]["states"]["empty"]
        s = uec.summarize(rep)
        self.assertIn("375x812", s["missing_viewports"])
        self.assertGreaterEqual(s["missing_states"], 2)

    def test_invisible_focus_fails(self) -> None:
        rep = fake_report()
        rep["routes"][0]["focus_walk"]["mobile"]["invisible"] = ["step 1: a"]
        self.assertFalse(uec.summarize(rep)["ok"])

    def test_schema_missing_fields(self) -> None:
        self.assertTrue(uec.validate_report({"schema": "x"}))


class TestReview(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "report.json").write_text(json.dumps(fake_report()), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def review(self, reviewer="rev-b", implementer="impl-a", roles="design", report="report.json"):
        p = self.d / "review.md"
        p.write_text(f"---\nroles: {roles}\nreviewer: {reviewer}\nimplementer: {implementer}\nreport: {report}\n---\n\n"
                     "- F1 Major: header hierarchy weak on mobile; disposition fixed in rev 2.\n", encoding="utf-8")
        return p

    def test_ok(self) -> None:
        self.assertEqual(uec.validate_review(self.review()), [])

    def test_self_review_rejected(self) -> None:
        self.assertTrue(any("implementer" in e for e in uec.validate_review(self.review(reviewer="impl-a"))))

    def test_role_required(self) -> None:
        self.assertTrue(uec.validate_review(self.review(roles="engineer")))

    def test_failing_report_rejected(self) -> None:
        (self.d / "bad.json").write_text(json.dumps(fake_report(ok_cell=False)), encoding="utf-8")
        self.assertTrue(any("不通过" in e for e in uec.validate_review(self.review(report="bad.json"))))

    def test_missing_file(self) -> None:
        self.assertTrue(uec.validate_review(self.d / "nope.md"))


def _browser_ready() -> bool:
    axe = os.environ.get("UI_EVIDENCE_AXE_JS")
    if not axe or not Path(axe).is_file() or importlib.util.find_spec("playwright") is None:
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


@unittest.skipUnless(_browser_ready(), "需要 playwright+chromium 与 UI_EVIDENCE_AXE_JS")
class TestBrowserSmoke(unittest.TestCase):

    def test_static_page(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            site = Path(d) / "site"
            site.mkdir()
            (site / "index.html").write_text(
                '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>T</title>'
                '<style>body{color:#111;background:#fff}:focus-visible{outline:3px solid #036}</style></head>'
                '<body><main><h1>T</h1><p id="s" aria-live="polite"></p><a href="#">Link</a> <button>Go</button></main>'
                '<script>document.getElementById("s").textContent=new URLSearchParams(location.search).get("state")||"ok"</script>'
                '</body></html>', encoding="utf-8")
            with socket.socket() as s:
                s.bind(("127.0.0.1", 0))
                port = s.getsockname()[1]
            m = Path(d) / "m.json"
            m.write_text(json.dumps({"routes": [{"name": "home", "path": "/index.html",
                                                 "states": {k: {"path": "/index.html?state=" + k} for k in uec.REQUIRED_STATES},
                                                 "tab_steps": 5}]}), encoding="utf-8")
            r = subprocess.run([sys.executable, str(SCRIPT), str(m), "--base-url", f"http://127.0.0.1:{port}",
                                "--start-cmd", f"{sys.executable} -m http.server {port} -d {site}",
                                "--out", str(Path(d) / "ev"), "--run-id", "smoke"],
                               capture_output=True, text=True, timeout=180)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            rep = json.loads((Path(d) / "ev" / "smoke" / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(uec.validate_report(rep), [])
            self.assertEqual(len(list((Path(d) / "ev" / "smoke").glob("*.png"))), 8)


class TestGateWiring(unittest.TestCase):

    def test_ui_delivery_requires_script(self) -> None:
        packs = (ROOT / "references" / "ui-delivery.md").read_text(encoding="utf-8")
        self.assertIn("scripts/ui_evidence_check.py", packs)
        self.assertIn("--validate-review", packs)
        self.assertIn("观感交付", packs)


if __name__ == "__main__":
    unittest.main()
