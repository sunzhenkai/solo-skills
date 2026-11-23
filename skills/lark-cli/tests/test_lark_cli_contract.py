"""lark-cli：手动门禁、三道防膨胀约束与禁止安装上游 skill 的文本契约。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


class LarkCliContractTest(unittest.TestCase):
    def test_frontmatter_and_manual_trigger(self) -> None:
        fm = _frontmatter(SKILL)
        self.assertEqual(ROOT.name, "lark-cli")
        self.assertIn("id: lark-cli", fm)
        self.assertIn("name: lark-cli", fm)
        self.assertIn("disable-model-invocation: true", fm)

    def test_three_gates_and_on_demand_read(self) -> None:
        for needle in (
            "## 三道门禁",
            "门 1 · 手动进入",
            "门 2 · 先路由再读",
            "门 3 · 按需加载",
            "lark-cli skills read lark-shared",
            "一次读多个业务 skill",
        ):
            self.assertIn(needle, SKILL)

    def test_forbids_global_upstream_skill_install(self) -> None:
        self.assertIn("npx @larksuite/cli@latest install", SKILL)
        self.assertIn("npx skills add larksuite/cli -g", SKILL)
        self.assertIn("~/.agents/skills/lark-*", SKILL)
        self.assertIn("不把 App Secret / token 写入对话或仓库", SKILL)

    def test_catalog_reference_exists(self) -> None:
        self.assertIn("references/catalog.md", SKILL)
        self.assertTrue((ROOT / "references" / "catalog.md").is_file())


if __name__ == "__main__":
    unittest.main()
