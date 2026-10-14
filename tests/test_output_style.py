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

    def test_size_warn_checklist_error_label_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            s = Path(tmp) / "skills"
            (s / "taskrail").mkdir(parents=True)
            (s / "taskrail" / "SKILL.md").write_text("x" * 9000, encoding="utf-8")
            ref = s / "task-intent" / "references"
            ref.mkdir(parents=True)
            (ref / "intent.md").write_text(
                "## 3. 给用户的复述（自然口语）\n\n"
                "- **要干嘛**：把导出改快一些，并且把前后耗时对比一并发给你看看结果\n\n"
                "## 6. x\n\n## 覆盖清单\n- 要干嘛：x\n- 怎么干：y\n\n",
                encoding="utf-8",
            )
            errs, warns = chk.run(s)
        self.assertTrue(any("taskrail/SKILL.md" in w for w in warns))
        self.assertTrue(any("自然口语" in w for w in warns))
        self.assertTrue(any("输出什么" in e for e in errs))
        self.assertFalse(any("要干嘛" in e for e in errs))
        self.assertFalse(any("对用户说话" in e for e in errs))  # 临时目录无 contract，不报


if __name__ == "__main__":
    unittest.main()
