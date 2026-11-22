"""app-api-ops 的文本契约测试：接入流程、凭证约定与调用纪律的关键句必须存在。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def test_frontmatter_fields(self) -> None:
        self.assertIn("id: agent-api-ops", SKILL)
        self.assertIn("name: agent-api-ops", SKILL)
        self.assertTrue(SKILL.lstrip().startswith("---"), "SKILL.md 须以 YAML frontmatter 开头")

    def test_versioned(self) -> None:
        """frontmatter 带 semver version；正文含会话首用的版本检查协议。"""
        self.assertRegex(SKILL, r"(?m)^version: \d+\.\d+\.\d+$")
        self.assertIn("## 版本与更新", SKILL)
        self.assertIn("期望版本高于本地", SKILL)
        self.assertIn("subagent", SKILL)

    def test_internal_reference_positioning(self) -> None:
        """内部 reference skill：手动点名使用，description 是给人读的一行摘要。"""
        self.assertIn("disable-model-invocation: true", SKILL)
        desc_line = next(l for l in SKILL.splitlines() if l.startswith("description:"))
        self.assertIn("接入话术", desc_line)
        self.assertIn("project-design-patterns", desc_line)


class FlowContract(unittest.TestCase):
    def test_handoff_parsing_step(self) -> None:
        self.assertIn("API Base", SKILL)
        self.assertIn("API Key", SKILL)

    def test_credential_storage_convention(self) -> None:
        self.assertIn("~/.agent-state/app-keys/<app>.env", SKILL)
        self.assertIn("APP_API_BASE=", SKILL)
        self.assertIn("APP_API_KEY=", SKILL)
        self.assertIn("600", SKILL)

    def test_bearer_auth(self) -> None:
        self.assertIn("Authorization: Bearer", SKILL)

    def test_status_semantics(self) -> None:
        for code, marker in [("401", "Key 无效或已被删除"), ("403", "应用侧保留给会话/管理端"), ("429", "退避重试")]:
            self.assertIn(code, SKILL, f"缺少 {code} 语义")
            self.assertIn(marker, SKILL)

    def test_doc_discovery_priority(self) -> None:
        self.assertIn("端点概览", SKILL)
        self.assertIn("skill 接口", SKILL)

    def test_discipline_lines(self) -> None:
        self.assertIn("先读后写", SKILL)
        self.assertIn("删除、覆盖、批量修改类操作先向用户复述目标并等确认", SKILL)


class SizeContract(unittest.TestCase):
    def test_skill_md_under_8kb(self) -> None:
        self.assertLess(len(SKILL.encode("utf-8")), 8 * 1024, "SKILL.md 超过 check-style 的 8KB 上限")


if __name__ == "__main__":
    unittest.main()
