"""OpenSpec 入口门：新状态、旧任务兼容、direct 拒绝、批准与载荷校验。"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_handoff.py"


def skill_corpus(root: Path) -> str:
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    parts += [path.read_text(encoding="utf-8") for path in sorted((root / "references").glob("*.md"))]
    return "\n".join(parts)


GOOD_META = """---
slug: demo
status: active
current_ref: execute
confirm_mode: human
execution: openspec
criterion: "demo 接口 p95 < 200ms"
driver: "demo-driver"
---
"""

LEGACY_META = """---
slug: demo
status: handed-off
phase: propose
tier: full
criterion: "demo 接口 p95 < 200ms"
driver: "demo-driver"
---
"""

HANDOFF_SVC = """
# demo

## 交接
- 交付类别：服务 / 后端
- 适用门包：quality-appendix.md「服务 / 后端」
- driver：demo-driver
"""

HANDOFF_UI = """
## 交接
- 交付类别：Web UI
- 适用门包：ui-delivery.md
- Active Instance 根路径：design-system/v1
- contract digest：sha256:aaa
- binding digest：sha256:bbb
- projection digest：sha256:ccc
"""


class TestCheckHandoff(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, text: str, slug: str = "demo", approved: bool = True, approval_dir: str = "reviews") -> None:
        directory = self.root / "tasks" / "ongoing" / slug
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "TASK.md").write_text(text, encoding="utf-8")
        if approved:
            (directory / approval_dir).mkdir(exist_ok=True)
            (directory / approval_dir / "APPROVED.md").write_text("已批准\n", encoding="utf-8")

    def run_gate(self, slug: str = "demo", json_output: bool = False) -> subprocess.CompletedProcess:
        command = [sys.executable, str(SCRIPT), str(self.root), slug]
        if json_output:
            command.append("--json")
        return subprocess.run(command, capture_output=True, text=True)

    def test_help(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)

    def test_new_openspec_metadata_passes(self) -> None:
        self.write(GOOD_META + HANDOFF_SVC)
        result = self.run_gate(json_output=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["status"], "active")
        self.assertEqual(payload["execution"], "openspec")

    def test_pass_web_ui(self) -> None:
        self.write(GOOD_META + HANDOFF_UI)
        self.assertEqual(self.run_gate().returncode, 0)

    def test_legacy_yaml_block_and_phase_remain_readable(self) -> None:
        self.write("# demo\n\n```yaml\nstatus: handed-off\nphase: apply\ncriterion: x\ndriver: demo-driver\n```\n" + HANDOFF_SVC, approval_dir="approve")
        self.assertEqual(self.run_gate().returncode, 0)

    def test_legacy_frontmatter_remains_readable(self) -> None:
        self.write(LEGACY_META + HANDOFF_SVC, approval_dir="approve")
        self.assertEqual(self.run_gate().returncode, 0)

    def test_requires_approval_or_not_required_reason(self) -> None:
        self.write(GOOD_META + HANDOFF_SVC, approved=False)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("APPROVED.md", result.stdout)
        self.assertIn("not-required", result.stdout)

    def test_not_required_with_reason_passes_without_approval_file(self) -> None:
        self.write(GOOD_META + HANDOFF_SVC + "- 批准：not-required: 普通可逆改动且用户未要求审批\n", approved=False)
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_not_required_without_reason_fails(self) -> None:
        self.write(GOOD_META + HANDOFF_SVC + "- 批准：not-required:   \n", approved=False)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("not-required", result.stdout)

    def test_direct_is_rejected_by_openspec_gate(self) -> None:
        self.write(GOOD_META.replace("execution: openspec", "execution: direct") + HANDOFF_SVC)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("direct 不走本入口门", result.stdout)

    def test_invalid_status_and_current_ref_are_rejected(self) -> None:
        text = GOOD_META.replace("status: active", "status: blocked").replace("current_ref: execute", "current_ref: plan")
        self.write(text + HANDOFF_SVC)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("status", result.stdout)
        self.assertIn("current_ref", result.stdout)

    def test_requires_criterion(self) -> None:
        self.write(GOOD_META.replace('criterion: "demo 接口 p95 < 200ms"', 'criterion: ""') + HANDOFF_SVC)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("criterion", result.stdout)

    def test_requires_driver_name(self) -> None:
        self.write(GOOD_META.replace('driver: "demo-driver"', "driver: null") + HANDOFF_SVC)
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("demo-driver", result.stdout)

    def test_child_task_driver_uses_leaf(self) -> None:
        self.write(GOOD_META.replace('driver: "demo-driver"', 'driver: "api-driver"') + HANDOFF_SVC, slug="demo/subtasks/api")
        self.assertEqual(self.run_gate("demo/subtasks/api").returncode, 0)

    def test_missing_task(self) -> None:
        result = self.run_gate("nope")
        self.assertEqual(result.returncode, 1)
        self.assertIn("taskrail", result.stdout)

    def test_path_traversal_is_rejected(self) -> None:
        result = self.run_gate("../demo")
        self.assertEqual(result.returncode, 1)
        self.assertIn("task path", result.stdout)

    def test_missing_gate_packs(self) -> None:
        self.write(GOOD_META + "\n## 交接\n- 交付类别：Web UI\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("适用门包", result.stdout)

    def test_missing_handoff_section(self) -> None:
        self.write(GOOD_META + "\n## 方案\n- 交付类别：服务\n")
        self.assertEqual(self.run_gate().returncode, 1)

    def test_web_ui_requires_digests(self) -> None:
        self.write(GOOD_META + HANDOFF_UI.replace("- binding digest：sha256:bbb\n", ""))
        result = self.run_gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("binding digest", result.stdout)

    def test_bypass_requires_user_confirmed(self) -> None:
        text = GOOD_META.replace('driver: "demo-driver"', 'gate_bypass: "agent decided"\ndriver: "demo-driver"')
        self.write(text + HANDOFF_SVC)
        self.assertEqual(self.run_gate().returncode, 1)

    def test_bypass_user_confirmed(self) -> None:
        self.write('---\nstatus: active\ngate_bypass: "2026-10-12 user-confirmed: one-off spike"\n---\n')
        result = self.run_gate()
        self.assertEqual(result.returncode, 0)
        self.assertIn("BYPASS", result.stdout)

    def test_usage_error(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "missing"), "x"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


class TestEntryGateWiring(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_corpus(ROOT)
        cls.rail = (ROOT.parent / "taskrail" / "SKILL.md").read_text(encoding="utf-8")
        cls.handoff = (ROOT.parent / "taskrail" / "references" / "handoff.md").read_text(encoding="utf-8")

    def test_skill_wires_gate_and_bypass(self) -> None:
        self.assertIn("入口门", self.skill)
        self.assertIn("scripts/check_handoff.py", self.skill)
        self.assertIn("不建 driver", self.skill)
        self.assertIn("gate_bypass", self.skill)
        self.assertIn("不手写省略验收的自由提示词", self.skill)

    def test_taskrail_and_handoff_reference_gate(self) -> None:
        self.assertIn("check_handoff.py", self.rail)
        self.assertIn("check_handoff.py", self.handoff)
        self.assertIn("交付类别", self.handoff)


class TestTemplateCompat(unittest.TestCase):
    def run_on(self, text: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "tasks" / "ongoing" / "demo"
            (directory / "reviews").mkdir(parents=True)
            (directory / "reviews" / "APPROVED.md").write_text("已批准\n", encoding="utf-8")
            (directory / "TASK.md").write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), tmp, "demo"], capture_output=True, text=True)

    def test_new_template_can_be_prepared_for_gate(self) -> None:
        templates = (ROOT.parent / "taskrail" / "references" / "templates.md").read_text(encoding="utf-8")
        match = re.search(r"## TASK\.md[^\n]*\n\n```markdown\n(.*?)\n```\n", templates, re.S)
        self.assertIsNotNone(match)
        text = match.group(1).replace("current_ref: plan", "current_ref: execute").replace("execution: null", "execution: openspec").replace("driver: null", 'driver: "demo-driver"')
        text += "\n## 交接\n- 交付类别：服务\n- 适用门包：无\n"
        result = self.run_on(text)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_bullet_meta_compat(self) -> None:
        result = self.run_on("# demo\n\n- status: handed-off\n- phase: propose\n- criterion: x\n- driver: demo-driver\n\n## 交接\n- 交付类别：服务\n- 适用门包：无\n")
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
