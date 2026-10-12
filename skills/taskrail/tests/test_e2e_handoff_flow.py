"""端到端：approve 态被拒 → handoff 写交接载荷 → check_handoff 放行 → ui_evidence_check 证据门 → 完成门 digest 核对。

回放 examples/minimal-webui 的真实脚本 CLI（subprocess），不锁文档措辞。
装了 playwright + axe-core（UI_EVIDENCE_AXE_JS）时另起本地静态页真跑证据门。
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "minimal-webui" / "workspace"
CHECK_HANDOFF = ROOT.parent / "taskflow" / "scripts" / "check_handoff.py"
UI_EVIDENCE = ROOT / "scripts" / "ui_evidence_check.py"
SLUG = "demo-list"
DIGESTS = ("contract", "binding", "projection")


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True)


def digests(text: str) -> dict[str, str]:
    return {k: m.group(1) for k in DIGESTS
            if (m := re.search(rf"^- {k} digest[:：]\s*(\S+)", text, re.M))}


class TestHandoffToEvidenceFlow(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name) / "ws"
        shutil.copytree(EXAMPLE, self.ws)
        self.task = self.ws / "tasks" / "ongoing" / SLUG / "TASK.md"
        self.handed_off = self.task.read_text(encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def gate(self) -> subprocess.CompletedProcess:
        return run(str(CHECK_HANDOFF), str(self.ws), SLUG, cwd=self.ws)

    def test_full_flow(self) -> None:
        # 1. approve 刚完成、尚未 handoff：入口门必须拒绝建 driver
        before = (self.handed_off.replace("status: handed-off", "status: ongoing")
                  .replace("phase: propose", "phase: approve"))
        before = before.split("## 交接")[0]
        self.task.write_text(before, encoding="utf-8")
        r = self.gate()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("taskrail", r.stdout)

        # 2. handoff：写回交接载荷与 handed-off 状态（phase-handoff 步骤 2、6）→ 入口门放行
        self.task.write_text(self.handed_off, encoding="utf-8")
        r = self.gate()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("PASS", r.stdout)

        # 3. 证据门：manifest 合法、report 通过、design 评审异源且指向通过的 report
        r = run(str(UI_EVIDENCE), "ui-manifest.json", "--validate-only", cwd=self.ws)
        self.assertEqual(r.returncode, 0, r.stdout)
        r = run(str(UI_EVIDENCE), "--validate-report", "evidence/ui/sample/report.json", cwd=self.ws)
        self.assertEqual(r.returncode, 0, r.stdout)
        review = self.task.parent / "design" / "review-ui.md"
        r = run(str(UI_EVIDENCE), "--validate-review", str(review), cwd=self.ws)
        self.assertEqual(r.returncode, 0, r.stdout)

        # 4. 完成门第 7 条：交接载荷与 design/contract.md 的三条 digest 一致
        contract = (self.task.parent / "design" / "contract.md").read_text(encoding="utf-8")
        self.assertEqual(digests(self.handed_off), digests(contract))
        self.assertEqual(set(digests(contract)), set(DIGESTS))

    def test_handoff_missing_digest_blocks(self) -> None:
        self.task.write_text(re.sub(r"^- binding digest.*\n", "", self.handed_off, flags=re.M), encoding="utf-8")
        r = self.gate()
        self.assertEqual(r.returncode, 1)
        self.assertIn("binding digest", r.stdout)

    def test_self_review_blocks_completion(self) -> None:
        review = self.task.parent / "design" / "review-ui.md"
        review.write_text(review.read_text(encoding="utf-8").replace("reviewer: reviewer-b", "reviewer: implementer-a"),
                          encoding="utf-8")
        r = run(str(UI_EVIDENCE), "--validate-review", str(review), cwd=self.ws)
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_failing_report_blocks_completion(self) -> None:
        rp = self.ws / "evidence" / "ui" / "sample" / "report.json"
        rep = json.loads(rp.read_text(encoding="utf-8"))
        cell = rep["routes"][0]["states"]["error"]["mobile"]
        cell["axe"]["violations"] = [{"id": "color-contrast", "impact": "serious", "nodes": 1}]
        spec = importlib.util.spec_from_file_location("uec", UI_EVIDENCE)
        uec = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(uec)  # type: ignore[union-attr]
        rep["summary"] = uec.summarize(rep)
        rp.write_text(json.dumps(rep), encoding="utf-8")
        r = run(str(UI_EVIDENCE), "--validate-report", str(rp), cwd=self.ws)
        self.assertEqual(r.returncode, 1, r.stdout)
        review = self.task.parent / "design" / "review-ui.md"
        self.assertEqual(run(str(UI_EVIDENCE), "--validate-review", str(review), cwd=self.ws).returncode, 1)

    def test_drifted_contract_detected(self) -> None:
        contract = self.task.parent / "design" / "contract.md"
        contract.write_text(contract.read_text(encoding="utf-8").replace("sha256:2b7d41", "sha256:ffffff"),
                            encoding="utf-8")
        self.assertNotEqual(digests(self.handed_off), digests(contract.read_text(encoding="utf-8")))


def _browser_ready() -> bool:
    axe = os.environ.get("UI_EVIDENCE_AXE_JS")
    return bool(axe and Path(axe).is_file() and importlib.util.find_spec("playwright"))


@unittest.skipUnless(_browser_ready(), "需要 playwright + UI_EVIDENCE_AXE_JS 才真跑浏览器")
class TestLiveEvidenceRun(unittest.TestCase):

    def test_live_run_then_review(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            ws = Path(d) / "ws"
            shutil.copytree(EXAMPLE, ws)
            r = run(str(UI_EVIDENCE), "ui-manifest.json", "--start-cmd",
                    f"{sys.executable} -m http.server 8765 --bind 127.0.0.1 --directory site",
                    "--out", "evidence/ui", "--run-id", "live", cwd=ws)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            review = ws / "tasks" / "ongoing" / SLUG / "design" / "review-ui.md"
            review.write_text(review.read_text(encoding="utf-8").replace("ui/sample/", "ui/live/"), encoding="utf-8")
            self.assertEqual(run(str(UI_EVIDENCE), "--validate-review", str(review), cwd=ws).returncode, 0)


if __name__ == "__main__":
    unittest.main()
