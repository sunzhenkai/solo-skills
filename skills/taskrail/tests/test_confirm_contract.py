"""确认协议薄契约：两种模式 + 真阻塞不停审阅放行。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfirmContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (ROOT / "references" / "confirm-protocol.md").read_text(encoding="utf-8")
        cls.ur = (ROOT / "references" / "user-report.md").read_text(encoding="utf-8")

    def test_dual_mode(self) -> None:
        self.assertIn("human", self.text)
        self.assertIn("goal", self.text)
        self.assertIn("另一个模型", self.text)

    def test_true_blocker_not_auto(self) -> None:
        self.assertIn("真阻塞", self.text)
        self.assertIn("不放行真阻塞", self.text.replace("**", ""))

    def test_points_to_user_report(self) -> None:
        self.assertIn("user-report.md", self.text)
        self.assertIn("说决定，不提问", self.ur)

    def test_human_intent_and_plan_are_separate_gates(self) -> None:
        self.assertIn("意图确认与实施方案确认是两个独立停点", self.text)
        self.assertIn("首次 execute 前或实施方案实质变更", self.text)
        self.assertIn("停等明确确认", self.text)

    def test_plan_confirmation_record_and_invalidation(self) -> None:
        plan = (ROOT / "references" / "plan.md").read_text(encoding="utf-8")
        templates = (ROOT / "references" / "templates.md").read_text(encoding="utf-8")
        self.assertIn("确认前不得进入 execute 或写代码", plan)
        self.assertIn("实施内容实质变化时重入本环节并重新确认", plan)
        self.assertIn("只更新 checkbox 或证据不改变状态", plan)
        self.assertIn("## 实施确认", templates)
        self.assertIn("pending | confirmed | not-required", templates)

    def test_confirmation_boundaries_cover_scope_delivery_and_risk(self) -> None:
        self.assertIn("意图、实施方案、交付边界和风险", self.text)
        self.assertIn("任一变化", self.text)
        self.assertIn("独立分支 / 发布 / 子任务", self.text)
        self.assertIn("接受未修复的 Blocker / Major", self.text)
        self.assertIn("验证不足 / 缩小交付", self.text)

    def test_new_stops_are_wired_into_references(self) -> None:
        plan = (ROOT / "references" / "plan.md").read_text(encoding="utf-8")
        decompose = (ROOT / "references" / "decompose.md").read_text(encoding="utf-8")
        verify = (ROOT / "references" / "verify.md").read_text(encoding="utf-8")
        done = (ROOT / "references" / "done.md").read_text(encoding="utf-8")
        grill = (ROOT / "references" / "grill.md").read_text(encoding="utf-8")
        self.assertIn("新增仓库 / 依赖", plan)
        self.assertIn("所需确认未完成前不创建或激活子任务", decompose)
        self.assertIn("同任务内部切片不新增停点", decompose)
        self.assertIn("执行者不能自行接受", verify)
        self.assertIn("用户明确接受", done)
        self.assertIn("否则保持未完成", done)
        self.assertIn("不把假设当成用户决定", grill)

    def test_non_stop_updates_follow_user_cognition(self) -> None:
        self.assertIn("用户需要知道的新增信息", self.text)
        self.assertIn("纯内部迁移不单独汇报", self.text)
        self.assertIn("继续且不等回复", self.text)
        self.assertIn("非停点同步不需要回复", self.text)

    def test_major_change_requires_plain_language_alignment_by_default(self) -> None:
        # SSOT 在 confirm-protocol.md 与 approve.md，其余文件只守卫入口指针而非逐字复读
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        design = (ROOT / "references" / "design.md").read_text(encoding="utf-8")
        approve = (ROOT / "references" / "approve.md").read_text(encoding="utf-8")
        router = (ROOT / "references" / "router.md").read_text(encoding="utf-8")
        self.assertIn("大型项目、重大改动或架构调整", skill)
        self.assertIn("无论 `human` 还是 `goal`", skill)
        self.assertIn("不因分支内可逆或内部切片跳过", self.text)
        self.assertIn("重大方案首次落定 / 实质变更先停等用户人话确认", self.text)
        self.assertIn("不因改动在 git 分支内可逆或属于同任务内部切片而跳过", approve)
        self.assertIn("[approve.md](approve.md)", design)
        self.assertIn("[confirm-protocol.md](confirm-protocol.md)", design)
        self.assertIn("[approve.md](approve.md)", router)
        self.assertIn("[confirm-protocol.md](confirm-protocol.md)", router)

    def test_small_clear_change_allows_combined_first_turn_confirmation(self) -> None:
        intent = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        plan = (ROOT / "references" / "plan.md").read_text(encoding="utf-8")
        close = (ROOT / "references" / "close.md").read_text(encoding="utf-8")
        self.assertIn("单一明确小改", self.text)
        self.assertIn("一次确认", self.text)
        self.assertIn("单一明确小改", intent)
        self.assertIn("合并确认", plan)
        self.assertIn("紧凑版", close)

    def test_no_suspension_five_tuple(self) -> None:
        self.assertFalse((ROOT / "references" / "suspension.md").exists())
        self.assertNotIn("挂起五元组", self.text)
        self.assertNotIn("五元组", self.ur)


if __name__ == "__main__":
    unittest.main()
