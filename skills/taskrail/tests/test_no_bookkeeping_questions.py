"""可回头的记账（建任务 / 恢复 / 起名 / 建 tasks/ / 更新台账 / dirty 切分支）不提问，直接做并一句话说明。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]


def r(rel: str) -> str:
    return (SKILLS / rel).read_text(encoding="utf-8")


ASK = re.compile(r"请用户(选|确认)|(?<!不)先问|询问是否|提示是否|提示创建或者恢复|先确认创建|先获确认再建|由用户三选一|停下来问|列出请用户选")
FILES = (
    "taskrail/SKILL.md", "taskrail/references/contract.md", "taskrail/references/user-report.md",
    "task-explore/SKILL.md", "task-explore/references/ledger.md", "task-explore/references/commands.md",
    "task-explore/references/approve.md", "task-explore/references/explore-design.md",
    "task-intent/SKILL.md", "taskflow/references/driver-template.md",
    "role-based-reviewer/SKILL.md", "role-based-reviewer/references/inference-and-speed.md",
)


class TestNoBookkeepingQuestions(unittest.TestCase):
    def test_no_ask_patterns(self) -> None:
        for rel in FILES:
            m = ASK.search(r(rel))
            self.assertIsNone(m, f"{rel}: {m.group(0) if m else ''}")

    def test_binding_decides_and_states(self) -> None:
        t = r("task-explore/references/ledger.md")
        self.assertIn("新建任务 mcp-admin-tools，因为和进行中的 i18n 无关", t)
        self.assertIn("不列选项", t)
        self.assertIn("自行判定新建或恢复", r("taskrail/SKILL.md"))

    def test_no_trailing_invitation(self) -> None:
        self.assertIn("如果理解偏了请纠正", r("taskrail/references/user-report.md"))  # 列为禁止项
        sec = r("taskrail/references/contract.md").split("## 对用户说话", 1)[1].split("\n## ", 1)[0]
        self.assertNotIn("有不同意见直接说", sec)

    def test_agent_roster_dirty_tree_is_stated_blocker(self) -> None:
        self.assertIn("说明哪些文件有未提交改动（受派方会改到用户的改动，属真阻塞）", r("agent-roster/SKILL.md"))

    def test_no_noise_dump(self) -> None:
        self.assertIn("不转贴术语表、工具调用过程", r("taskrail/references/user-report.md"))


if __name__ == "__main__":
    unittest.main()
