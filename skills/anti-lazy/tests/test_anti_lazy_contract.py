"""anti-lazy 文本契约测试：锁定保守触发、入口分流、纠偏重启、六类反模式自检与收口硬闸。"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")

DESC_NEG = re.compile(r"何时不用|不走|不适用|不触发|不要|不应|不用于")


def _extract_description(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("description:"):
            return line[len("description:"):].strip().strip("\"'")
    return ""


class AntiLazyContractTest(unittest.TestCase):
    def test_conservative_model_invocation_description(self) -> None:
        desc = _extract_description(SKILL)
        self.assertTrue(desc, "SKILL.md 缺少 description")
        self.assertLessEqual(len(desc), 300)
        for trigger in ("用户纠正", "偷懒", "复杂任务", "宣称完成前"):
            self.assertIn(trigger, desc)
        self.assertNotIn("disable-model-invocation: true", SKILL)
        self.assertIsNone(DESC_NEG.search(desc))

    def test_exemption_and_three_entry_modes(self) -> None:
        self.assertIn("保守触发与豁免", SKILL)
        self.assertIn("单步确定性问答", SKILL)
        for mode in ("起手对齐", "纠偏重启", "交付闸门"):
            self.assertIn(mode, SKILL)

    def test_correction_restart_protocol(self) -> None:
        self.assertIn("### 纠偏重启协议", SKILL)
        for step in ("先停手", "显式作废", "反查偷懒类型", "全量重扫同类遗漏"):
            self.assertIn(step, SKILL)

    def test_six_anti_lazy_checks_present(self) -> None:
        self.assertIn("## 4. 反偷懒自检", SKILL)
        signals = (
            "需求静默漏项",
            "替代验证 / 假验证",
            "半成品 / 局部修补",
            "遇阻过早甩锅",
            "拿“剩余缺口”掩盖未完成",
            "顺旧错打补丁",
        )
        for signal in signals:
            self.assertIn(signal, SKILL)

    def test_four_core_sections_have_completion_gates(self) -> None:
        for heading in (
            "## 1. 意图｜对齐结果、约束与边界",
            "## 2. 现场｜让一手证据描述现状",
            "## 3. 差距｜聚焦核心缺口，区分阻塞与延后",
        ):
            self.assertIn(heading, SKILL)
        self.assertEqual(SKILL.count("**完成门**"), 3)
        self.assertIn("## 5. 收口硬闸", SKILL)
        for gate in ("逐条对账", "证据保真", "阻塞清零", "简洁表达"):
            self.assertIn(gate, SKILL)

    def test_escalation_boundaries_are_explicit(self) -> None:
        self.assertIn("`trouble-grill`", SKILL)
        self.assertIn("`taskrail`", SKILL)
        self.assertIn("`session-wrap`", SKILL)


if __name__ == "__main__":
    unittest.main()
