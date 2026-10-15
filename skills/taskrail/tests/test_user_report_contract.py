"""对用户汇报唯一出处（taskrail/references/user-report.md）契约：链接、顺序、记账不问人、resume 模板不裸露台账字段。"""
import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
UR = "taskrail/references/user-report.md"


def r(rel: str) -> str:
    return (SKILLS / rel).read_text(encoding="utf-8")


class UserReportTest(unittest.TestCase):
    def test_linked_from_three_skills(self) -> None:
        for rel in ("taskrail/SKILL.md", "task-explore/SKILL.md", "taskflow/SKILL.md"):
            self.assertIn("user-report.md", r(rel), rel)

    def test_contract_points_here(self) -> None:
        sec = r("taskrail/references/contract.md").split("## 对用户说话", 1)[1].split("\n## ", 1)[0]
        self.assertIn("[user-report.md](user-report.md)", sec)
        self.assertIn("属记账：编排者直接更新，不向用户请示", r("taskrail/references/contract.md"))

    def test_report_order(self) -> None:
        t = r(UR)
        idx = [t.index(k) for k in ("**影响面**", "**要改哪些地方**", "**怎么改**", "**我做的决定**")]
        self.assertEqual(idx, sorted(idx))

    def test_rules_present(self) -> None:
        t = r(UR)
        for k in ("## 3. 内部词留在台账", "## 4. file:line 只作附注", "## 5. 说决定，不提问",
                  "## 6. resume 模板", "勾 evolution 提案里的记账项", "晋升 Skill 改动前确认 diff"):
            self.assertIn(k, t)

    def test_resume_template_has_no_ledger_fields(self) -> None:
        tpl = r(UR).split("## 6. resume 模板", 1)[1].split("\n## ", 1)[0]
        for bad in ("phase", "status", "tier", "driver", "checkbox", "未勾"):
            self.assertNotIn(bad, tpl, bad)

    def test_resume_lines_do_not_list_ledger_fields(self) -> None:
        lines = [
            next(l for l in r("taskrail/SKILL.md").splitlines() if "`resume`：" in l),
            next(l for l in r("task-explore/references/commands.md").splitlines() if "resume 模板" in l),
        ]
        for l in lines:
            self.assertIsNone(re.search(r"/ *(当前 )?phase *[/（]|建议下一步", l), l)
        sus = r("taskrail/references/suspension.md")
        self.assertNotIn("等待项 → 已解除/仍未解除", sus)
        self.assertNotIn("建议下一步**（`explore`", r("task-explore/references/commands.md"))

    def test_unchecked_list_goes_to_ledger(self) -> None:
        self.assertIn("结束时在验证记录逐条列出未勾项", r("taskflow/references/driver-template.md"))

    def test_skill_sizes(self) -> None:
        for rel in ("taskrail/SKILL.md", "task-explore/SKILL.md", "taskflow/SKILL.md"):
            self.assertLessEqual(len(r(rel).encode("utf-8")), 8192, rel)




class TestStatementsNotQuestions(unittest.TestCase):
    def test_default_no_questions_and_blockers_listed(self) -> None:
        t = r(UR)
        sec = t.split("## 5. 说决定，不提问", 1)[1].split("\n## ", 1)[0]
        for k in ("默认不向用户提问", "只有真阻塞才停", "停的时候也用陈述句"):
            self.assertIn(k, sec)

    def test_pointers_follow_single_source(self) -> None:
        self.assertIn("说决定，不提问", r("taskrail/references/confirm-protocol.md"))
        self.assertIn("说决定，不提问", r("task-intent/SKILL.md"))
        self.assertIn("自问自答", r("task-explore/references/explore-design.md"))
        self.assertNotIn("最多一个问题", r("task-intent/references/intent.md"))

    def test_contract_examples_have_no_questions(self) -> None:
        sec = r("taskrail/references/contract.md").split("## 对用户说话", 1)[1].split("\n## ", 1)[0]
        for line in sec.splitlines():
            if "后：「" in line:
                self.assertNotRegex(line.split("后：「", 1)[1], r"[？?]")


if __name__ == "__main__":
    unittest.main()
