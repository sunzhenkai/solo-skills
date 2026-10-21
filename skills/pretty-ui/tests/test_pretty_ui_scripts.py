"""pretty-ui 脚本：色阶单调、对比度数值、check_page 的报错与提示。"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"pretty_ui_{name}", SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(script: str, *args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True, cwd=cwd
    )


GOOD_PAGE = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>示例</title>
<style>:root { --text: #1f2937; --bg: #ffffff; } body { color: var(--text); background: var(--bg); }</style>
</head><body><a href="./sub/index.html">子页</a><a href="https://example.com">外链</a></body></html>
"""

SUB_PAGE = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>子页</title></head>
<body><a href="../index.html">返回</a></body></html>
"""


class PaletteTest(unittest.TestCase):
    pal = load("palette")

    def test_ramp_lightness_monotonic_and_base_kept(self) -> None:
        ramp = self.pal.build_ramp(self.pal.parse_color("#0f7b6c"))
        stops = sorted(ramp)
        self.assertEqual(stops, [100, 200, 300, 400, 500, 600, 700, 800, 900])
        lightness = [ramp[s]["l"] for s in stops]
        self.assertEqual(lightness, sorted(lightness, reverse=True))
        self.assertEqual(ramp[500]["hex"], "#0f7b6c")

    def test_hue_rotation_capped(self) -> None:
        h0 = self.pal.parse_color("#2563eb")[0]
        ramp = self.pal.build_ramp(self.pal.parse_color("#2563eb"), cap=20.0)
        for c in ramp.values():
            delta = abs((c["h"] - h0 + 180) % 360 - 180)
            self.assertLessEqual(delta, 20.0 + 0.1)

    def test_css_output(self) -> None:
        r = run("palette.py", "--grey", "--css")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("--color-neutral-100:", r.stdout)
        self.assertIn("--color-neutral-900:", r.stdout)

    def test_bad_color_exit_2(self) -> None:
        self.assertEqual(run("palette.py", "--base", "nope").returncode, 2)


class ContrastTest(unittest.TestCase):
    con = load("contrast")

    def test_known_ratios(self) -> None:
        self.assertAlmostEqual(self.con.contrast_ratio("#000000", "#ffffff"), 21.0, places=2)
        self.assertGreaterEqual(self.con.contrast_ratio("#767676", "#ffffff"), 4.5)
        self.assertLess(self.con.contrast_ratio("#777777", "#ffffff"), 4.5)

    def test_exit_codes(self) -> None:
        self.assertEqual(run("contrast.py", "--pair", "#767676", "#ffffff").returncode, 0)
        self.assertEqual(run("contrast.py", "--pair", "#777777", "#ffffff").returncode, 1)
        self.assertEqual(run("contrast.py", "--pair", "#777777", "#ffffff", "--size", "large").returncode, 0)

    def test_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "pairs.json"
            path.write_text(json.dumps({"pairs": [
                {"name": "正文", "fg": "#111827", "bg": "#ffffff"},
                {"name": "弱字", "fg": "#9ca3af", "bg": "#ffffff"},
            ]}), encoding="utf-8")
            r = run("contrast.py", "--matrix", str(path))
            self.assertEqual(r.returncode, 1)
            self.assertIn("1/2 通过", r.stdout)


class CheckPageTest(unittest.TestCase):
    def site(self, d: str, index: str = GOOD_PAGE, sub: str = SUB_PAGE) -> Path:
        root = Path(d) / "out"
        (root / "sub").mkdir(parents=True)
        (root / "index.html").write_text(index, encoding="utf-8")
        (root / "sub" / "index.html").write_text(sub, encoding="utf-8")
        return root

    def test_good_site_passes_offline(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            r = run("check_page.py", "--offline", str(self.site(d)))
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("0 个报错", r.stdout)

    def test_broken_and_absolute_links_fail(self) -> None:
        bad = GOOD_PAGE.replace('href="./sub/index.html"', 'href="./missing.html"').replace(
            "</body>", '<a href="/docs/x.html">根</a><img src="file:///tmp/a.png" alt=""></body>'
        )
        with tempfile.TemporaryDirectory() as d:
            r = run("check_page.py", str(self.site(d, index=bad)))
            self.assertEqual(r.returncode, 1)
            self.assertIn("本地链接目标不存在：./missing.html", r.stdout)
            self.assertIn("站点根路径", r.stdout)
            self.assertIn("file://", r.stdout)

    def test_page_basics_required(self) -> None:
        bare = "<html><head><title></title></head><body></body></html>"
        with tempfile.TemporaryDirectory() as d:
            r = run("check_page.py", str(self.site(d, sub=bare)))
            self.assertEqual(r.returncode, 1)
            for msg in ("缺 lang", "viewport", "<title>"):
                self.assertIn(msg, r.stdout)

    def test_remote_dependency_is_error_only_offline(self) -> None:
        cdn = GOOD_PAGE.replace(
            "</head>", '<script type="module">import m from "https://cdn.example.com/m.mjs";</script></head>'
        )
        with tempfile.TemporaryDirectory() as d:
            root = self.site(d, index=cdn)
            self.assertEqual(run("check_page.py", str(root)).returncode, 0)
            r = run("check_page.py", "--offline", str(root))
            self.assertEqual(r.returncode, 1)
            self.assertIn("依赖联网资源", r.stdout)

    def test_default_look_hints(self) -> None:
        loud = GOOD_PAGE.replace(
            "</style>",
            "h1 { background: linear-gradient(90deg, var(--text), var(--bg)); background-clip: text; }"
            " button { outline: none; transition: transform .2s; font-size: 11px; color: #6b7280; }</style>",
        ).replace("<body>", "<body><h1>🚀 发布</h1><button>✨ 开始</button>")
        with tempfile.TemporaryDirectory() as d:
            r = run("check_page.py", str(self.site(d, index=loud)))
            self.assertEqual(r.returncode, 0, r.stdout)
            for tag in ("[X2]", "[X5]", "[F7]", "[M4]", "[T4]", "[C1]"):
                self.assertIn(tag, r.stdout)


if __name__ == "__main__":
    unittest.main()
