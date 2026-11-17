"""taskrail 环节与相邻 skill 的接入：排查方法、已有知识与收口落点。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / "references" / name).read_text(encoding="utf-8")


class NeighborSkillContract(unittest.TestCase):
    def test_diagnose_uses_trouble_grill_for_divergent_root_cause(self) -> None:
        diagnose = read("diagnose.md")
        self.assertIn("按 `trouble-grill` 的锚点、假设板与四道门执行", diagnose)
        self.assertIn("记录写本任务 `evidence/diagnose.md`", diagnose)
        self.assertIn("未安装时按本文件方法执行", diagnose)

    def test_explore_reads_existing_knowledge_first(self) -> None:
        explore = read("explore.md")
        self.assertIn("项目有 Atlas（默认 `docs/atlas/`）或知识 wiki（默认 `docs/wiki/`）时先读入口与相关页", explore)
        self.assertIn("过期或冲突以当前源码为准", explore)

    def test_close_routes_knowledge_to_owning_skills(self) -> None:
        close = read("close.md")
        self.assertIn("`stale_pages` 非空就把复核交给 `project-atlas`", close)
        self.assertIn("踩坑和操作台账交给 `wiki-data`", close)
        self.assertIn("跨任务的 skill 改进交给 `skill-upgrader`", close)

    def test_examples_index_has_no_removed_wizard_path(self) -> None:
        index = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        self.assertIn("旧 handoff 兼容回归样例", index)
        self.assertNotIn("wizard/intent.md", index)


if __name__ == "__main__":
    unittest.main()
