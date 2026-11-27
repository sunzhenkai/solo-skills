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

    def test_anti_lazy_and_optional_grilling_wired_at_key_gates(self) -> None:
        for name in ("confirm-protocol.md", "design.md", "intent.md", "plan.md", "verify.md"):
            self.assertIn("`anti-lazy`", read(name), name)
        self.assertIn("走纠偏重启", read("intent.md"))
        self.assertIn("过交付闸门", read("verify.md"))
        grill = read("grill.md")
        self.assertIn("不自答闭环", grill)
        self.assertIn("可选外部 skill `grilling` 或 `grill-with-docs`", grill)

    def test_matt_engineering_core_disciplines_are_wired(self) -> None:
        decompose = read("decompose.md")
        explore = read("explore.md")
        grill = read("grill.md")
        design = read("design.md")
        diagnose = read("diagnose.md")
        self.assertIn("tracer bullet", decompose)
        self.assertIn("fresh context window", decompose)
        self.assertIn("GLOSSARY.md", explore)
        self.assertIn("`Q1` / `Q2`", grill)
        self.assertIn("不阻塞其余前沿", grill)
        self.assertIn("`codebase-design`", design)
        self.assertIn("`domain-modeling`", design)
        self.assertIn("seam", design)
        self.assertIn("三条件", design)
        self.assertIn("Design It Twice", design)
        self.assertIn("tight & red-capable", diagnose)
        self.assertIn("Minimise", diagnose)
        self.assertIn("[DEBUG-", diagnose)
        self.assertIn("`diagnosing-bugs`", diagnose)

    def test_examples_index_has_no_removed_wizard_path(self) -> None:
        index = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        self.assertIn("旧 handoff 兼容回归样例", index)
        self.assertNotIn("wizard/intent.md", index)


if __name__ == "__main__":
    unittest.main()
