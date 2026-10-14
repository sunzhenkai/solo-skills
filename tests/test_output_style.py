import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_output_style as chk  # noqa: E402


class OutputStyleTest(unittest.TestCase):
    def test_repo_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_output_style.py")],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_detects_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            s = Path(tmp) / "skills"
            (s / "taskrail").mkdir(parents=True)
            (s / "taskrail" / "SKILL.md").write_text("x" * 9000, encoding="utf-8")
            (s / "other").mkdir()
            (s / "other" / "SKILL.md").write_text("x" * 9000, encoding="utf-8")
            ref = s / "task-intent" / "references"
            ref.mkdir(parents=True)
            (ref / "statement-template.md").write_text(
                "```markdown\n" + "\n".join(f"- 行{i}" for i in range(9)) + "\n- 当前 phase\n```\n",
                encoding="utf-8",
            )
            (ref / "probe.md").write_text(
                "## Digest（≤10 行）\n\n```text\n" + "\n".join("a" for _ in range(11)) + "\n```\n",
                encoding="utf-8",
            )
            errs, warns = chk.run(s)
        joined = "\n".join(errs)
        self.assertIn("taskrail/SKILL.md", joined)
        self.assertIn("超过 8 行", joined)
        self.assertIn("phase", joined)
        self.assertIn("Digest 模板超过 10 行", joined)
        self.assertEqual(len(warns), 1)


if __name__ == "__main__":
    unittest.main()
