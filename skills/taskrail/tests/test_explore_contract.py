"""references 可组合契约：统一结构、按需加载、无固定阶段命令。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"
ROUTED = ("plan", "explore", "diagnose", "grill", "design", "approve", "decompose", "verify", "close")


def read(*parts: str) -> str:
    return ROOT.joinpath(*parts).read_text(encoding="utf-8")


class ReferenceContractTest(unittest.TestCase):
    def test_public_commands_are_task_operations(self) -> None:
        skill = read("SKILL.md")
        for command in (
            "taskrail <一句话目标>", "taskrail goal: <一句话目标>",
            "taskrail intent <一句话目标>", "taskrail resume [task-id]",
            "taskrail explain [task-id]", "taskrail list",
        ):
            self.assertIn(command, skill)
        for removed in ("taskrail wizard", "taskrail design", "taskrail approve", "taskrail handoff"):
            self.assertNotIn(removed, skill)

    def test_every_routed_reference_has_complete_contract(self) -> None:
        required = ("## 目的", "## 进入条件", "## 跳过条件", "## 所需输入", "## 执行方法", "## 产出", "## 完成门", "## 退出与重入")
        for name in ROUTED:
            text = (REF / f"{name}.md").read_text(encoding="utf-8")
            for heading in required:
                self.assertIn(heading, text, f"{name}: {heading}")

    def test_router_uses_evidence_and_prevents_oscillation(self) -> None:
        router = read("references", "router.md")
        self.assertIn("当前最关键不确定性", router)
        self.assertIn("没有新证据", router)
        self.assertIn("enter / skip / exit / reopen", router)
        self.assertIn("代码任务不得跳过验证", router)

    def test_handoff_contains_pointers_not_full_design_copy(self) -> None:
        handoff = read("references", "handoff.md")
        self.assertIn("指针与判据", handoff)
        self.assertIn("check_handoff.py", handoff)
        self.assertIn("不复制完整方案", handoff)
        self.assertNotIn("逐字复制", handoff)

    def test_approve_returns_to_router_not_fixed_pipeline(self) -> None:
        approve = read("references", "approve.md")
        self.assertIn("返回 router", approve)
        self.assertNotIn("下一步只写 handoff", approve)
        self.assertIn("未选 OpenSpec 不强制 handoff", approve)

    def test_templates_track_hot_state_and_decisions(self) -> None:
        templates = read("references", "templates.md")
        self.assertIn("current_ref: plan", templates)
        self.assertIn("confirm_mode: human", templates)
        self.assertIn("decisions.md / history.md", templates)
        self.assertIn("superseded", templates)
        self.assertNotIn("tier:", templates)

    def test_ledger_and_concurrency_are_separate(self) -> None:
        self.assertTrue((REF / "ledger.md").is_file())
        self.assertTrue((REF / "ledger-concurrency.md").is_file())
        self.assertTrue((REF / "decompose.md").is_file())


if __name__ == "__main__":
    unittest.main()
