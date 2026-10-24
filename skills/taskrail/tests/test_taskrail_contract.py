"""taskrail 核心契约：动态 references、正交维度、热状态和完成门。"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def read(*parts: str) -> str:
    return ROOT.joinpath(*parts).read_text(encoding="utf-8")


class ContractTest(unittest.TestCase):
    def test_skill_identity_and_size(self) -> None:
        raw = (ROOT / "SKILL.md").read_bytes()
        self.assertLessEqual(len(raw), 8192)
        text = raw.decode("utf-8")
        self.assertRegex(text, r"(?m)^id: taskrail$")
        self.assertRegex(text, r"(?m)^name: taskrail$")

    def test_references_exist_and_old_pipeline_is_removed(self) -> None:
        for name in (
            "contract.md", "router.md", "ref-contract.md", "plan.md", "explore.md",
            "diagnose.md", "grill.md", "design.md", "approve.md", "decompose.md",
            "verify.md", "close.md", "done.md", "intent.md", "handoff.md",
            "ledger.md", "templates.md", "archive-reopen.md", "user-report.md",
            "confirm-protocol.md", "ui-delivery.md", "quality-appendix.md",
        ):
            self.assertTrue((REF / name).is_file(), name)
        self.assertFalse((REF / "phase-wizard.md").exists())
        self.assertFalse((REF / "large-scope.md").exists())

    def test_dynamic_state_and_no_tier(self) -> None:
        contract = read("references", "contract.md")
        self.assertIn("current_ref: intake | plan | explore | diagnose", contract)
        self.assertIn("confirm_mode: human | goal", contract)
        self.assertIn("execution: direct | openspec | null", contract)
        self.assertIn("enter / continue / skip / reopen", contract)
        self.assertNotIn("tier:", contract)
        self.assertNotIn("status: ongoing", contract)

    def test_dimensions_are_orthogonal(self) -> None:
        contract = read("references", "contract.md")
        self.assertIn("分别判断", contract)
        self.assertIn("direct / OpenSpec", contract)
        self.assertIn("不拆 / 切片 / 子任务", contract)
        skill = read("SKILL.md")
        self.assertIn("只改变确认方式，不改变路由", skill)

    def test_handoff_is_openspec_only(self) -> None:
        contract = read("references", "contract.md")
        handoff = read("references", "handoff.md")
        skill = read("SKILL.md")
        self.assertIn("只有 OpenSpec 路径", contract)
        self.assertIn("direct 路径不建 driver", contract)
        self.assertIn("check_handoff.py", handoff)
        self.assertIn("check_handoff.py", skill)
        self.assertIn("not-required", contract)

    def test_user_report_and_intent_boundary(self) -> None:
        report = read("references", "user-report.md")
        intent = read("references", "intent.md")
        self.assertIn("唯一出处", report)
        self.assertIn("说决定，不提问", report)
        self.assertIn("真阻塞才停", report)
        self.assertIn("注意任务边界", intent)

    def test_done_is_single_source(self) -> None:
        done = read("references", "done.md")
        self.assertIn("唯一真源", done)
        self.assertIn("driver 归档、checkbox 全勾、目录已归档都不能代替", done)
        self.assertIn("## 观感验收", done)
        self.assertIn("pretty-ui/references/direction.md", done)
        self.assertIn("SUMMARY.md", done)

    def test_context_budget_and_lazy_loading(self) -> None:
        contract = read("references", "contract.md")
        router = read("references", "router.md")
        self.assertIn("6 KB", contract)
        self.assertIn("8 KB", contract)
        self.assertIn("不默认加载", contract)
        self.assertIn("每次只加载选中的 reference", router)
        self.assertIn("不把兄弟子任务、历史和原始日志带入", router)

    def test_no_deleted_compat_shells_in_skill(self) -> None:
        skill = read("SKILL.md")
        self.assertNotIn("decide", skill)
        self.assertNotIn("plan-review", skill)
        self.assertNotIn("gate-packs", skill)
        self.assertFalse((REF / "commands.md").exists())


    def test_local_markdown_links_exist(self) -> None:
        link = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
        files = [
            path
            for skill in (ROOT, ROOT.parent / "taskflow")
            for path in [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]
        ]
        missing = [
            f"{path}: {target}"
            for path in files
            for target in link.findall(path.read_text(encoding="utf-8"))
            if "://" not in target and not (path.parent / target).resolve().is_file()
        ]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
