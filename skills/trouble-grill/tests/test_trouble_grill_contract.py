"""trouble-grill：wiki-data 可选归档与独立落盘契约。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class WikiDataHandoffContract(unittest.TestCase):
    def test_archive_is_explicit_and_preserves_evidence(self) -> None:
        self.assertIn("用户明确要求把排查结果沉淀到知识 wiki 时", SKILL)
        self.assertIn("`wiki-data` 的 `ingest`", SKILL)
        for field in ("锚点", "证据等级", "用户输入", "dead-end", "验证盲区", "回退条件"):
            self.assertIn(field, SKILL)
        self.assertIn("只有 `confirmed` 可作为根因归档", SKILL)

    def test_default_persistence_remains_independent(self) -> None:
        self.assertIn("tasks/ongoing/{task-name}/TASK.md", SKILL)
        self.assertIn("未提出归档或没有 `wiki-data` 时", SKILL)
        self.assertIn("仍按上述位置落盘，排查流程不变", SKILL)


if __name__ == "__main__":
    unittest.main()
