"""真阻塞边界两头都要守住：该停的停，不该停的不停；难回头的决定单独说；决定只记一本账。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]


def r(rel: str) -> str:
    return (SKILLS / rel).read_text(encoding="utf-8")


def section5() -> str:
    t = r("taskrail/references/user-report.md")
    return t.split("## 5. 说决定，不提问", 1)[1].split("\n## ", 1)[0]


class TestMustStop(unittest.TestCase):
    def test_blocker_categories(self) -> None:
        line = next(l for l in section5().splitlines() if l.startswith("- 只有真阻塞才停"))
        for k in ("删除或迁移数据", "改共享配置", "线上", "不可逆", "对外发送", "要改完成标准", "安全底线", "账号、权限"):
            self.assertIn(k, line, k)


class TestMustNotStop(unittest.TestCase):
    def test_ordinary_choices(self) -> None:
        line = next(l for l in section5().splitlines() if l.startswith("- 不停、直接定下来说一句的"))
        for k in ("拓扑先不导入初始数据", "命名", "页面布局"):
            self.assertIn(k, line, k)
        self.assertNotIn("删除", line)

    def test_ordinary_examples_not_in_blocker_line(self) -> None:
        line = next(l for l in section5().splitlines() if l.startswith("- 只有真阻塞才停"))
        for k in ("命名", "布局", "初始数据"):
            self.assertNotIn(k, line, k)


class TestHardToReverse(unittest.TestCase):
    def test_defined_once_and_pointed(self) -> None:
        sec = section5()
        self.assertIn("**难回头的决定**", sec)
        for k in ("数据结构", "接口 / API 形状", "schema", "存储格式", "对外命名", "依赖", "单独一行"):
            self.assertIn(k, sec, k)
        self.assertIn("「说决定，不提问」", r("task-intent/SKILL.md"))
        self.assertIn("我定了 X，因为 Y", r("task-intent/SKILL.md"))


class TestSingleDecisionLedger(unittest.TestCase):
    def test_template_table(self) -> None:
        t = r("task-explore/references/templates.md")
        self.assertIn("## 已做决定", t)
        self.assertIn("| # | 决定 | 理由 | 可逆 | 来源阶段 |", t)
        self.assertNotIn("\n## 决策\n", t)

    def test_writers_append_there(self) -> None:
        for rel in ("taskrail/references/contract.md", "taskrail/references/confirm-protocol.md",
                    "task-intent/SKILL.md", "task-explore/references/explore-design.md",
                    "taskrail/references/user-report.md"):
            self.assertIn("「已做决定」", r(rel), rel)

    def test_no_old_section_name(self) -> None:
        for rel in ("taskrail/references/contract.md", "task-explore/references/commands.md",
                    "task-explore/references/approve.md", "task-explore/references/ledger.md"):
            self.assertNotIn("决策节", r(rel), rel)
            self.assertNotIn("决策小节", r(rel), rel)


if __name__ == "__main__":
    unittest.main()
