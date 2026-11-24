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

    def test_overlays_validation(self) -> None:
        m = manifest()
        m["routes"][0]["overlays"] = [
            {"name": "drawer", "trigger": {"click": "#open"}, "container": "[role='dialog']"}
        ]
        self.assertEqual(uec.validate_manifest(m), [])
        m["routes"][0]["overlays"].append({"name": "drawer", "trigger": {"hover": "#x"}, "container": ""})
        errs = uec.validate_manifest(m)
        self.assertTrue(any("name 重复" in e for e in errs))
        self.assertTrue(any("container" in e for e in errs))
        self.assertTrue(any("trigger" in e for e in errs))

    def test_quick_manifest_builder(self) -> None:
        qm = uec.build_quick_manifest("http://127.0.0.1:5173", "/, /settings, settings")
        self.assertEqual(qm["base_url"], "http://127.0.0.1:5173")
        names = [r["name"] for r in qm["routes"]]
        self.assertEqual(len(names), 3)
        self.assertEqual(len(set(names)), 3)
        self.assertIn("default", qm["routes"][0]["states"])

    def test_cli_quick_requires_base_url(self) -> None:
        r = subprocess.run([sys.executable, str(SCRIPT), "--quick"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("--base-url", r.stderr)

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

    def test_obscured_focus_fails(self) -> None:
        rep = fake_report()
        rep["routes"][0]["focus_walk"]["desktop"]["obscured"] = ["step 1: button 被 header.sticky 遮挡"]
        s = uec.summarize(rep)
        self.assertFalse(s["ok"])
        self.assertEqual(s["focus_obscured"], 1)

    def test_runtime_and_dom_blocking_and_warnings(self) -> None:
        rep = fake_report()
        rep["routes"][0]["states"]["success"]["desktop"]["runtime"] = {
            "page_errors": ["TypeError: boom"],
            "console_errors": ["Unhandled error"],
            "http_errors": ["500 http://x/api"],
            "request_failed": [],
        }
        rep["routes"][0]["states"]["success"]["desktop"]["dom"] = {
            "horizontal_overflow": {"overflow": True, "scroll_width": 1400, "inner_width": 1280, "culprits": ["div.wide (right=1400)"]},
            "broken_images": ["/missing.png"],
            "clipped_rings": ["div.card 被裁左，裁它：div.wrap"],
            "tiny_targets_blocking": ["button.x (16x16)"],
            "tiny_targets_warn": ["button.y (32x32)"],
            "long_lines": ["p「abc」 约 60 字"],
            "small_text": [],
            "tight_line_height": [],
        }
        # error 态默认豁免 http_errors / request_failed，但仍拦截 page_errors
        rep["routes"][0]["states"]["error"]["desktop"]["runtime"] = {
            "page_errors": [],
            "console_errors": [],
            "http_errors": ["500 http://x/expected-error"],
            "request_failed": ["http://x/offline (net::ERR_FAILED)"],
        }
        s = uec.summarize(rep)
        self.assertFalse(s["ok"])
        self.assertEqual(s["runtime_errors"], 3)
        self.assertEqual(s["broken_images"], 1)
        self.assertEqual(s["layout_blocking"], 3)
        self.assertEqual(len(s["warnings"]), 2)

    def test_overlay_failures(self) -> None:
        rep = fake_report()
        rep["routes"][0]["overlays"] = {
            "drawer": {
                "desktop": {
                    "visible": True,
                    "padding_clipped": True,
                    "overflow": False,
                    "focus_entered": False,
                    "closed": True,
                    "focus_restored": False,
                }
            }
        }
        s = uec.summarize(rep)
        self.assertFalse(s["ok"])
        self.assertEqual(s["overlay_failures"], 3)

    def test_quick_mode_report_allows_default_state_and_no_axe(self) -> None:
        vps = uec.DEFAULT_VIEWPORTS
        rep = {
            "schema": uec.SCHEMA, "mode": "quick", "run_id": "q", "base_url": "http://x", "started_at": "t",
            "axe_skipped": True, "viewports": vps,
            "routes": [{"name": "home", "path": "/", "not_applicable": {},
                        "states": {"default": {v["name"]: {"screenshot": "x.png"} for v in vps}},
                        "focus_walk": {v["name"]: {"order": ["a"], "invisible": [], "obscured": []} for v in vps}}],
        }
        rep["summary"] = uec.summarize(rep)
        self.assertEqual(uec.validate_report(rep), [])
        self.assertTrue(rep["summary"]["ok"])

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


def _playwright_only_ready() -> bool:
    if importlib.util.find_spec("playwright") is None:
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


@unittest.skipUnless(_playwright_only_ready(), "需要 playwright+chromium")
class TestBrowserBadFixtures(unittest.TestCase):
    """坏页 fixture 实测：验证 --quick 准确拦截运行时报错、裂图、横向溢出、外扩环裁切与极小热区。"""

    def test_quick_catches_bad_page_and_passes_good_page(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            site = Path(d) / "site"
            site.mkdir()
            (site / "bad.html").write_text(
                '<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>Bad</title>'
                '<style>'
                'body{margin:0;color:#111;background:#fff}:focus-visible{outline:3px solid #036}'
                '.wide{width:2000px;height:20px;background:#eee}'
                '.clip{overflow:hidden;width:120px}.ring{box-shadow:0 0 0 1px #000;width:120px;height:30px}'
                '.tiny{width:14px;height:14px;padding:0;border:0}'
                '</style></head><body>'
                '<div class="wide">overflow</div>'
                '<div class="clip"><div class="ring">ring</div></div>'
                '<img src="/nope.png" width="40" height="40" alt="missing">'
                '<button class="tiny">x</button>'
                '<script>console.error("fixture boom");</script>'
                '</body></html>',
                encoding="utf-8",
            )
            (site / "good.html").write_text(
                '<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>Good</title>'
                '<style>body{margin:16px;color:#111;background:#fff}:focus-visible{outline:3px solid #036}'
                'button{min-width:44px;min-height:44px}</style></head>'
                '<body><main><h1>OK</h1><button>Go</button></main></body></html>',
                encoding="utf-8",
            )
            with socket.socket() as s:
                s.bind(("127.0.0.1", 0))
                port = s.getsockname()[1]
            cmd = [
                sys.executable, str(SCRIPT), "--quick",
                "--base-url", f"http://127.0.0.1:{port}",
                "--start-cmd", f"{sys.executable} -m http.server {port} -d {site}",
                "--out", str(Path(d) / "ev"),
            ]
            r_bad = subprocess.run(cmd + ["--routes", "/bad.html", "--run-id", "bad"], capture_output=True, text=True, timeout=180)
            self.assertEqual(r_bad.returncode, 1, r_bad.stdout + r_bad.stderr)
            rep_bad = json.loads((Path(d) / "ev" / "bad" / "report.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(rep_bad["summary"]["runtime_errors"], 1)
            self.assertGreaterEqual(rep_bad["summary"]["broken_images"], 1)
            self.assertGreaterEqual(rep_bad["summary"]["layout_blocking"], 3)

            r_good = subprocess.run(cmd + ["--routes", "/good.html", "--run-id", "good"], capture_output=True, text=True, timeout=180)
            self.assertEqual(r_good.returncode, 0, r_good.stdout + r_good.stderr)


class TestGateWiring(unittest.TestCase):

    def test_ui_delivery_requires_script(self) -> None:
        packs = (ROOT / "references" / "ui-delivery.md").read_text(encoding="utf-8")
        self.assertIn("scripts/ui_evidence_check.py", packs)
        self.assertIn("--validate-review", packs)
        self.assertIn("观感交付", packs)
        self.assertIn("L1 快检", packs)
        self.assertIn("--quick", packs)
        self.assertIn("L2 完整证据门", packs)
        self.assertIn("overlays", packs)


if __name__ == "__main__":
    unittest.main()
