"""agent-roster 文本契约：不变量、权限两档、引用可达、脱敏占位。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (SKILL_ROOT / rel).read_text(encoding="utf-8")


class FrontmatterContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_frontmatter_trio(self) -> None:
        self.assertRegex(
            self.text,
            r"^---\nid: agent-roster\nname: agent-roster\ndescription: .+\n---",
        )


class InvariantContract(unittest.TestCase):
    """正文声明「最容易被绕过的五条」——文本契约逐条钉住。"""

    def setUp(self) -> None:
        self.text = read("SKILL.md")

    def test_five_invariants_present(self) -> None:
        for needle in (
            "选择理由先写后执行，顺序不可颠倒。",
            "受派方只能是名册里的 Endpoint，编排者不得自任",
            "未安装 `acpx` 时先停下并提议安装：未获确认不得安装，未获**明确拒绝**不得降级",
            "固化条件攒够时必须提案，不许继续沉默；提案与写入之间必须有使用者确认。",
            "点了 Role 就用它的默认 Endpoint；没有能用的默认就问这次用谁，不改走路由；没得到明确同意不改对照表。",
        ):
            self.assertIn(needle, self.text, needle)

    def test_order_invariant_stated(self) -> None:
        self.assertIn(
            "第 2 步与第 6 步的位置是本 skill 的不变量，不可重排。", self.text
        )

    def test_decision_md_four_items(self) -> None:
        self.assertIn("**候选有谁**、**选了谁**、**为什么选它**、**依据是什么**", self.text)

    def test_permission_two_levels(self) -> None:
        self.assertIn("**只读**（默认）：定计划、评审、调研、排查。", self.text)
        self.assertIn("**可写**：仅实施类委派。", self.text)

    def test_smoke_and_controlled_execution(self) -> None:
        self.assertIn("Endpoint+模型组合无 L3 成功记录时先冒烟", self.text)
        self.assertIn("`timeout` 必填", self.text)

    def test_probe_three_levels(self) -> None:
        for level in ("**L1 存在性**", "**L2 握手**", "**L3 冒烟**"):
            self.assertIn(level, self.text, level)


class RolesReferenceContract(unittest.TestCase):
    def setUp(self) -> None:
        self.roles = read("references/roles.md")
        self.skill = read("SKILL.md")

    def test_five_roles_inlined_with_semantics(self) -> None:
        for line in (
            "- `developer`：完成已经确定的任务",
            "- `planner`：把已经说清的需求写成方案",
            "- `reviewer`：审方案",
            "- `code-reviewer`：审代码",
            "- `designer`：出界面方案并审界面",
        ):
            self.assertIn(line, self.roles, line)

    def test_roles_md_no_repo_root_context_link(self) -> None:
        self.assertNotIn("CONTEXT.md", self.roles)

    def test_skill_md_no_out_of_skill_relative_links(self) -> None:
        self.assertNotIn("../../docs", self.skill)
        self.assertNotIn("../../../docs", self.skill)
        self.assertIn("只在源仓存在，安装副本不随分发", self.skill)


class ReferencedFilesExist(unittest.TestCase):
    def test_references_and_scripts_mentioned_in_skill_exist(self) -> None:
        skill = read("SKILL.md")
        mentioned = set(re.findall(r"(?:references|scripts)/[A-Za-z0-9_.-]+", skill))
        self.assertTrue(mentioned, "SKILL.md 应至少引用一个 references/scripts 文件")
        for rel in sorted(mentioned):
            self.assertTrue(
                (SKILL_ROOT / rel).is_file(), f"SKILL.md 引用的 {rel} 不存在"
            )

    def test_scripts_are_stdlib_only(self) -> None:
        for script in (SKILL_ROOT / "scripts").glob("*.py"):
            body = script.read_text(encoding="utf-8")
            for banned in ("import yaml", "import requests", "import dotenv"):
                self.assertNotIn(banned, body, f"{script.name} 引入第三方包 {banned}")


class RedactionPlaceholderContract(unittest.TestCase):
    def test_no_real_host_alias_in_scripts(self) -> None:
        for name in ("delegate.py", "smoke_gate.py"):
            body = read(f"scripts/{name}")
            self.assertNotIn("example-host", body, f"{name} 残留真实主机别名 example-host")
            self.assertIn("example-host/codex", body, f"{name} 缺 example-host 占位")
