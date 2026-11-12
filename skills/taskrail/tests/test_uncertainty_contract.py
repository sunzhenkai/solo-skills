"""未决问题与待明确区：准确提问、按需毕业、单一落点与完成门。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def read(name: str) -> str:
    return (REF / name).read_text(encoding="utf-8")


class UncertaintyContractTest(unittest.TestCase):
    def test_question_and_fog_are_classified_by_precision(self) -> None:
        contract = read("contract.md")
        self.assertIn("未决问题 `U-n`", contract)
        self.assertIn("待明确区 `F-n`", contract)
        self.assertIn("判断依据是能否准确提问，不是能否立即回答", contract)
        self.assertIn("旧任务没有这两节时视为空", contract)

    def test_hot_context_is_the_only_question_index(self) -> None:
        contract = read("contract.md")
        template = read("templates.md")
        self.assertIn("## 未决问题", template)
        self.assertIn("## 待明确区", template)
        self.assertIn("| ID | 问题 | 解决形式 | 依赖 |", template)
        self.assertIn("| ID | 模糊区域 | 重估触发 |", template)
        self.assertIn("ROADMAP 只写交付结构", contract)
        self.assertIn("详情只在 `context/current.md` 维护", contract)
        self.assertIn("只列 `U-n / F-n` 与指针", read("design.md"))

    def test_resolution_and_graduation_leave_no_duplicate_open_item(self) -> None:
        grill = read("grill.md")
        self.assertIn("把该项移出未决表", grill)
        self.assertIn("毕业为新的 `U-n` 并从待明确区移除", grill)
        self.assertIn("失效时把原因写 `history.md`", grill)
        self.assertIn("已做决定写 decisions.md", grill)

    def test_router_handles_one_ready_question_without_a_new_phase(self) -> None:
        contract = read("contract.md")
        router = read("router.md")
        self.assertIn("每个路由轮次最多解决一个依赖就绪的 `U-n`", contract)
        self.assertIn("不新增 `current_ref`", contract)
        self.assertIn("goal 可在后续轮次继续", contract)
        self.assertIn("选一个依赖就绪、最能解决当前最关键不确定性的 `U-n`", router)

    def test_plan_defers_fog_until_it_graduates(self) -> None:
        self.assertIn("`F-n` 仅保留重估触发", read("plan.md"))

    def test_done_requires_only_criterion_relevant_questions_to_close(self) -> None:
        done = read("done.md")
        close = read("close.md")
        self.assertIn("影响 criterion 的 `U-n` 均已解决", done)
        self.assertIn("其余 `F-n` 已写入 SUMMARY", done)
        self.assertIn("未阻塞交付的 `F-n` 写入剩余风险或后续项", close)


if __name__ == "__main__":
    unittest.main()
