"""E2E 跨仓回归脚本的契约测试。

- 结构契约：脚本存在、只依赖 Python 标准库、提供 direct / openspec 两种模式。
- 活体契约（git 可用时）：真实跑 direct 模式；openspec CLI 可用时再跑 openspec 模式。
"""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "e2e_cross_repo.py"

STDLIB_OK = {
    "__future__", "argparse", "json", "os", "platform", "re", "shutil",
    "subprocess", "sys", "tempfile", "time", "datetime", "pathlib",
    "string", "typing",
}


class E2eScriptContractTest(unittest.TestCase):
    def test_script_exists(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"缺少 {SCRIPT}")

    def test_stdlib_only_imports(self) -> None:
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        extra = imported - STDLIB_OK
        self.assertEqual(extra, set(), f"scripts/ 只允许标准库依赖，实际：{sorted(extra)}")

    def test_help_lists_modes(self) -> None:
        proc = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--mode", proc.stdout)
        self.assertIn("openspec", proc.stdout)


@unittest.skipUnless(shutil.which("git"), "需要 git")
class E2eLiveDirectTest(unittest.TestCase):
    def test_direct_mode_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--mode", "direct", "--report", str(report)],
                capture_output=True, text=True, timeout=600)
            self.assertEqual(proc.returncode, 0,
                             f"stdout:\n{proc.stdout[-2000:]}\nstderr:\n{proc.stderr[-2000:]}")
            text = report.read_text(encoding="utf-8")
            self.assertIn("direct 模式完成", text)
            self.assertIn("全部通过", text)


@unittest.skipUnless(shutil.which("openspec"), "需要 openspec CLI")
class E2eLiveOpenspecTest(unittest.TestCase):
    def test_openspec_mode_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--mode", "openspec", "--report", str(report)],
                capture_output=True, text=True, timeout=900)
            self.assertEqual(proc.returncode, 0,
                             f"stdout:\n{proc.stdout[-2000:]}\nstderr:\n{proc.stderr[-2000:]}")
            text = report.read_text(encoding="utf-8")
            self.assertIn("openspec 模式完成", text)
            self.assertIn("全部通过", text)


if __name__ == "__main__":
    unittest.main()
