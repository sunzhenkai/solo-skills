"""自动拆分：subtasks、依赖推进、父子上下文隔离和父任务集成验收。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def read(name: str) -> str:
    return (REF / name).read_text(encoding="utf-8")


class DecomposeContractTest(unittest.TestCase):
    def test_all_children_are_created_pending_under_subtasks(self) -> None:
        text = read("decompose.md")
        self.assertIn("自动建立和恢复子任务", text)
        self.assertIn("立即创建轻量 pending TASK", text)
        self.assertIn("--parent <parent-id>", text)
        self.assertIn("subtasks/<child>/TASK.md", text)
        self.assertIn("只拆一层", text)
        self.assertIn("subtasks/<child>/", read("contract.md"))
        self.assertIn("<parent>/subtasks/<child>", read("handoff.md"))

    def test_slices_and_children_use_delivery_atomicity(self) -> None:
        contract = read("contract.md")
        self.assertIn("必须原子落地的是切片", contract)
        self.assertIn("能按契约独立交付", contract)
        self.assertIn("不是唯一判据", contract)
        self.assertIn("一个连贯改动能在同一分支实施并验证", read("decompose.md"))

    def test_roadmap_covers_criterion_dependencies_and_integration(self) -> None:
        text = read("decompose.md")
        for field in ("项 | 类型 | 目标 | 子判据", "涉及仓库", "依赖", "交付边界"):
            self.assertIn(field, text)
        self.assertIn("子判据合计覆盖总判据", text)
        self.assertIn("依赖无环", text)
        self.assertIn("集成项", text)

    def test_child_scope_and_plan_confirmation(self) -> None:
        self.assertIn("子任务继承父意图", read("intent.md"))
        self.assertIn("不重新确认", read("intent.md"))
        self.assertIn("子任务未超父 ROADMAP 范围和子判据", read("confirm-protocol.md"))
        self.assertIn("意图、approve 不重复停；PLAN", read("confirm-protocol.md"))
        self.assertIn("由父批准覆盖，不逐个停", read("approve.md"))
        self.assertIn("每个实际执行的子任务", read("plan.md"))

    def test_parent_is_coordinator_and_must_verify_integration(self) -> None:
        contract = read("contract.md")
        self.assertIn("父任务若有子任务则不直接写业务代码", contract)
        self.assertIn("不持实施 driver", contract)
        self.assertIn("全部子任务 done 后父任务进入 verify", contract)
        done = read("done.md")
        self.assertIn("所有直接子任务 done", done)
        self.assertIn("父 ROADMAP 集成项和总判据已验证", done)

    def test_ready_progress_and_blocked_dependency_chain(self) -> None:
        text = read("decompose.md")
        self.assertIn("自动推进依赖已 done 的就绪项", text)
        self.assertIn("正在做的优先", text)
        self.assertIn("子任务 blocked 只停其依赖链", text)
        self.assertIn("N 个里完成 M 个", read("user-report.md"))
        self.assertIn("取下一就绪项", read("ledger.md"))

    def test_parent_does_not_load_every_child_context(self) -> None:
        router = read("router.md")
        self.assertIn("父任务只读 ROADMAP、共享契约和就绪子 TASK", router)
        self.assertIn("不把兄弟子任务、历史和原始日志带入", router)

    def test_old_large_scope_pipeline_is_gone(self) -> None:
        self.assertFalse((REF / "large-scope.md").exists())
        self.assertFalse((REF / "phase-wizard.md").exists())


if __name__ == "__main__":
    unittest.main()
