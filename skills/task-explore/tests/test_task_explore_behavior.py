"""替代原逐字门禁锁（gate_lines.txt）：只校验少数关键行为仍有规定，不锁措辞。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def corpus() -> str:
    files = [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md"))]
    return "\n".join(f.read_text(encoding="utf-8") for f in files)


class KeyBehaviors(unittest.TestCase):
    def setUp(self) -> None:
        self.t = corpus()

    def test_no_overwrite(self) -> None:
        self.assertIn("禁止覆盖", self.t)

    def test_create_tasks_needs_confirm(self) -> None:
        self.assertIn("没有 `tasks/` 时**必须先获得确认再创建**", self.t)

    def test_archive_and_reopen_need_explicit_confirm(self) -> None:
        self.assertIn("确认关闭", self.t)
        self.assertIn("确认 reopen", self.t)

    def test_phase_enum_closed(self) -> None:
        self.assertIn("wizard | explore | design | approve | propose | apply | archive | done", self.t)

    def test_no_repo_root_docs_from_task_dir(self) -> None:
        self.assertIn("禁止调用 `grill-with-docs` / `domain-modeling`", self.t)

    def test_approve_exit_is_handoff(self) -> None:
        self.assertIn("approve 后的唯一出口是 `handoff`", self.t)


class ArchiveReopenBehavior(unittest.TestCase):
    def setUp(self) -> None:
        self.t = (ROOT / "references" / "archive-reopen.md").read_text(encoding="utf-8")

    def test_conflict_has_no_side_effects(self) -> None:
        self.assertIn("不得改 `TASK.md`、不得移动目录、不得改 INDEX", self.t)

    def test_frozen_plan_goes_handoff_not_archive(self) -> None:
        self.assertIn("改走 handoff", self.t)

    def test_unknown_progress_not_done(self) -> None:
        self.assertIn("不当作已完成", self.t)
        self.assertIn("**不回写**", self.t)

    def test_summary_and_history_kept(self) -> None:
        self.assertIn("SUMMARY.md", self.t)
        self.assertIn("不删不改写", self.t)
        self.assertIn("driver 及其 change 不删", self.t)


if __name__ == "__main__":
    unittest.main()
