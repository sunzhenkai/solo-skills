"""anti-lazy 文本契约测试：锁定意图对齐、现场证据、差距选择与交付收口。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class AntiLazyContractTest(unittest.TestCase):
    def test_model_invocation_triggers_cover_task_lifecycle(self) -> None:
        self.assertIn("description: 意图对齐与差距检查", SKILL)
        for trigger in ("任务开始", "方向漂移", "用户纠正", "交付前"):
            self.assertIn(trigger, SKILL)
        self.assertNotIn("disable-model-invocation: true", SKILL)

    def test_intent_preserves_user_result_and_boundaries(self) -> None:
        self.assertIn("## 意图｜用户想推进什么？", SKILL)
        self.assertIn("重读用户最新请求，也回看最初目标", SKILL)
        self.assertIn("他要的是方案、实现、诊断，还是决策依据？", SKILL)
        self.assertIn("哪些边界是用户亲口划下的？", SKILL)

    def test_current_state_is_grounded_in_evidence(self) -> None:
        self.assertIn("## 现场｜现在真实走到哪里？", SKILL)
        self.assertIn("让证据描述现状", SKILL)
        self.assertIn("把事实、推测和未知分开", SKILL)
        self.assertIn("现场能回答的，先让现场回答", SKILL)

    def test_gap_drives_one_valuable_next_action(self) -> None:
        self.assertIn("## 差距｜距离「对了」还差什么？", SKILL)
        self.assertIn("把意图与现状并排放置", SKILL)
        self.assertIn("现在消除哪个差距，最能推进用户意图？", SKILL)
        self.assertIn("把下一步收敛到最有信息或推进价值的一个动作", SKILL)

    def test_delivery_maps_original_request_to_evidence(self) -> None:
        self.assertIn("## 收口｜凭什么可以交付？", SKILL)
        self.assertIn("让每项明确要求指向产物、回答或证据", SKILL)
        self.assertIn("用用户的原始场景检查交付", SKILL)
        self.assertIn("哪些检查实际运行过，结果是什么？", SKILL)
        self.assertIn("外在表达保持简洁", SKILL)


if __name__ == "__main__":
    unittest.main()
