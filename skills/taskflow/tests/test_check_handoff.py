"""taskflow 入口门 check_handoff.py：fixture 通过 / 拒绝，及 SKILL.md 接线文本锁。"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def skill_corpus(root: Path) -> str:
    """SKILL.md 正文 + references/*.md：细则下沉到 references 后，文本契约按整个 skill 校核。"""
    parts = [(root / "SKILL.md").read_text(encoding="utf-8")]
    parts += [p.read_text(encoding="utf-8") for p in sorted((root / "references").glob("*.md"))]
    return "\n".join(parts)

SCRIPT = ROOT / "scripts" / "check_handoff.py"

GOOD_META = """---
slug: demo
status: handed-off
phase: propose
tier: full
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

    def write(self, text: str, slug: str = "demo") -> None:
        d = self.root / "tasks" / "ongoing" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "TASK.md").write_text(text, encoding="utf-8")

    def run_gate(self, slug: str = "demo") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), slug],
                              capture_output=True, text=True)

    def test_help(self) -> None:
        r = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)

    def test_pass_service(self) -> None:
        self.write(GOOD_META + HANDOFF_SVC)
        r = self.run_gate()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("PASS", r.stdout)

    def test_pass_web_ui(self) -> None:
        self.write(GOOD_META + HANDOFF_UI)
        self.assertEqual(self.run_gate().returncode, 0)

    def test_yaml_block_meta(self) -> None:
        self.write("# demo\n\n```yaml\nstatus: handed-off\nphase: apply\n```\n" + HANDOFF_SVC)
        self.assertEqual(self.run_gate().returncode, 0)

    def test_missing_task(self) -> None:
        r = self.run_gate("nope")
        self.assertEqual(r.returncode, 1)
        self.assertIn("taskrail", r.stdout)

    def test_not_handed_off(self) -> None:
        self.write(GOOD_META.replace("handed-off", "ongoing").replace("propose", "approve") + HANDOFF_SVC)
        r = self.run_gate()
        self.assertEqual(r.returncode, 1)
        self.assertIn("status", r.stdout)
        self.assertIn("phase", r.stdout)

    def test_missing_gate_packs(self) -> None:
        self.write(GOOD_META + "\n## 交接\n- 交付类别：Web UI\n")
        r = self.run_gate()
        self.assertEqual(r.returncode, 1)
        self.assertIn("适用门包", r.stdout)

    def test_missing_handoff_section(self) -> None:
        self.write(GOOD_META + "\n## 方案\n- 交付类别：服务\n")
        self.assertEqual(self.run_gate().returncode, 1)

    def test_web_ui_requires_digests(self) -> None:
        self.write(GOOD_META + HANDOFF_UI.replace("- binding digest：sha256:bbb\n", ""))
        r = self.run_gate()
        self.assertEqual(r.returncode, 1)
        self.assertIn("binding digest", r.stdout)

    def test_bypass_requires_user_confirmed(self) -> None:
        self.write(GOOD_META.replace("tier: full", 'gate_bypass: "agent decided"').replace("handed-off", "ongoing").replace("propose", "explore"))
        self.assertEqual(self.run_gate().returncode, 1)

    def test_bypass_user_confirmed(self) -> None:
        self.write('---\nstatus: ongoing\nphase: explore\ngate_bypass: "2026-10-12 user-confirmed: one-off spike"\n---\n')
        r = self.run_gate()
        self.assertEqual(r.returncode, 0)
        self.assertIn("BYPASS", r.stdout)

    def test_usage_error(self) -> None:
        r = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "missing"), "x"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


class TestEntryGateWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = skill_corpus(ROOT)
        cls.rail = (ROOT.parent / "taskrail" / "SKILL.md").read_text(encoding="utf-8")
        cls.handoff = (ROOT.parent / "task-explore" / "references" / "handoff.md").read_text(encoding="utf-8")

    def test_skill_wires_gate(self) -> None:
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
    """task-explore templates.md 的 TASK.md 原样模板必须能过入口门：模板与脚本解析同步。"""

    def run_on(self, text: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "tasks" / "ongoing" / "demo"
            d.mkdir(parents=True)
            (d / "TASK.md").write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), tmp, "demo"], capture_output=True, text=True)

    def test_template_task_md_passes(self) -> None:
        import re
        tpl = (ROOT.parent / "task-explore" / "references" / "templates.md").read_text(encoding="utf-8")
        block = re.search(r"## TASK\.md\n\n```markdown\n(.*?)\n```\n", tpl, re.S).group(1)
        text = block.replace("status: ongoing", "status: handed-off").replace("phase: wizard", "phase: propose")
        text = re.sub(r"## 交接\n.*", "## 交接\n- 交付类别：服务\n- 适用门包：无\n", text, flags=re.S)
        r = self.run_on(text)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_bullet_meta_compat(self) -> None:
        r = self.run_on("# demo\n\n- status: handed-off\n- phase: propose\n\n## 交接\n- 交付类别：服务\n- 适用门包：无\n")
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
