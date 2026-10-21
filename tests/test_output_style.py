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
            ref = s / "taskrail" / "references"
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
        self.assertFalse(any("对用户说话" in e for e in errs))  # 临时目录无 user-report，不报

    def test_lint_warns_desc_chain_ban(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            s = Path(tmp) / "skills"
            d = s / "demo"
            (d / "references").mkdir(parents=True)
            body = "\n".join(["不要做 A。禁止做 B。"] * 6)
            (d / "SKILL.md").write_text(
                "---\nname: demo\ndescription: " + "x" * 320 + "\n---\n\n"
                "细则见 [a](references/a.md)。\n" + body + "\n",
                encoding="utf-8",
            )
            (d / "references" / "a.md").write_text("再看 [b](b.md)。\n", encoding="utf-8")
            (d / "references" / "b.md").write_text("b\n", encoding="utf-8")
            _, warns = chk.run(s)
        self.assertTrue(any("description 320" in w for w in warns))
        self.assertTrue(any("引用链超一层" in w and "references/b.md" in w for w in warns))
        self.assertTrue(any("禁令词" in w for w in warns))

    def test_lint_quiet_on_clean_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            s = Path(tmp) / "skills"
            d = s / "demo"
            (d / "references").mkdir(parents=True)
            (d / "SKILL.md").write_text(
                "---\nname: demo\ndescription: >-\n  Does X. Use when Y.\n---\n\n"
                "见 [a](references/a.md) 与 [b](references/b.md)。\n",
                encoding="utf-8",
            )
            (d / "references" / "a.md").write_text("[b](b.md)\n", encoding="utf-8")
            (d / "references" / "b.md").write_text("b\n", encoding="utf-8")
            _, warns = chk.run(s)
        self.assertEqual(warns, [])


if __name__ == "__main__":
    unittest.main()
