"""agent-api-ops 引用件的文本契约测试：定位、版本协议、接入流程与调用纪律的关键句必须存在。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
REF = (ROOT / "references" / "agent-api-ops.md").read_text(encoding="utf-8")


class PositioningContract(unittest.TestCase):
    def test_reference_is_linked_from_skill_md(self) -> None:
        """操作规范是 project-design-patterns 的引用件，SKILL.md 一层直链。"""
        self.assertIn("references/agent-api-ops.md", SKILL)
        self.assertTrue((ROOT / "references" / "agent-api-ops.md").is_file())

    def test_not_a_standalone_skill(self) -> None:
        """不再是独立 skill：无 skill frontmatter，也不再有独立安装命令。"""
        self.assertFalse(REF.lstrip().startswith("---"), "引用件不带 skill frontmatter")
        self.assertNotIn("disable-model-invocation", REF)
        self.assertNotIn("-s agent-api-ops", REF)

    def test_version_protocol_uses_skill_frontmatter(self) -> None:
        """版本协议：skill.md 声明 project-design-patterns 版本，升级安装整个 skill。"""
        self.assertIn("## 版本与更新", REF)
        self.assertIn("skill: project-design-patterns@", REF)
        self.assertIn("`SKILL.md` frontmatter `version`", REF)
        self.assertIn("npx skills add sunzhenkai/solo-skills -s project-design-patterns -g -y", REF)
        self.assertIn("期望版本高于本地", REF)
        self.assertIn("subagent", REF)


class FlowContract(unittest.TestCase):
    def test_handoff_parsing_step(self) -> None:
        self.assertIn("API Base", REF)
        self.assertIn("API Key", REF)

    def test_credential_storage_convention(self) -> None:
        self.assertIn("~/.agent-state/app-keys/<app>.env", REF)
        self.assertIn("APP_API_BASE=", REF)
        self.assertIn("APP_API_KEY=", REF)
        self.assertIn("600", REF)

    def test_bearer_auth(self) -> None:
        self.assertIn("Authorization: Bearer", REF)

    def test_status_semantics(self) -> None:
        for code, marker in [("401", "Key 无效或已被删除"), ("403", "应用侧保留给会话/管理端"), ("429", "退避重试")]:
            self.assertIn(code, REF, f"缺少 {code} 语义")
            self.assertIn(marker, REF)

    def test_doc_discovery_priority(self) -> None:
        self.assertIn("端点概览", REF)
        self.assertIn("skill 接口", REF)

    def test_discipline_lines(self) -> None:
        self.assertIn("先读后写", REF)
        self.assertIn("删除、覆盖、批量修改类操作先向用户复述目标并等确认", REF)


if __name__ == "__main__":
    unittest.main()
