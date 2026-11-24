"""way-to-fix 文本契约：锁定证据诊断、最小修复、验证与同类检查。"""
from __future__ import annotations

import unittest
from pathlib import Path

SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class WayToFixContractTest(unittest.TestCase):
    def test_model_invocation_covers_problem_reports(self) -> None:
        head = SKILL.split("---", 2)[1]
        self.assertIn("description: 问题修复闭环", head)
        for trigger in ("bug", "报错", "异常行为", "测试失败", "性能退化", "排查定位", "way-to-fix"):
            self.assertIn(trigger, head)
        self.assertNotIn("disable-model-invocation: true", head)

    def test_boundaries_isolate_readonly_and_side_effect_authorization(self) -> None:
        self.assertIn("## 边界与协作", SKILL)
        for partner in ("taskrail", "trouble-grill", "anti-lazy", "commit-push", "session-wrap"):
            self.assertIn(partner, SKILL)
        self.assertIn("排查与复现默认只读", SKILL)
        self.assertIn("涉及修改公共接口、配置或错误语义、新增依赖、扩大到同类问题", SKILL)
        self.assertIn("允许修复仅覆盖本地改动与验证，git 提交、推送、合入主分支与部署均需另行确认", SKILL)

    def test_analysis_builds_symptom_signal_from_evidence(self) -> None:
        self.assertIn("期望行为、实际症状、发生条件与影响范围", SKILL)
        self.assertIn("`wiki-data` 时按现象词走其 `query` 预检", SKILL)
        self.assertIn("区分事实、推测和未知", SKILL)
        self.assertIn("环境错配、过期构建或瞬时工具与网络故障，将其与代码缺陷分开处理", SKILL)
        self.assertIn("捕捉用户的原始症状", SKILL)
        self.assertIn("记录实际运行的命令或检查及关键结果", SKILL)
        self.assertIn("无法复现时，写清已试范围、现有证据", SKILL)

    def test_root_cause_requires_falsifiable_causal_evidence(self) -> None:
        self.assertIn("触发条件和失效机制", SKILL)
        self.assertIn("可观察预测", SKILL)
        self.assertIn("每次只改变一个变量", SKILL)
        self.assertIn("`trouble-grill` 的锚点、假设板与四道门", SKILL)
        self.assertIn("先将最小复现固化为回归测试，在未修复代码上观察失败作为因果锚点", SKILL)
        self.assertIn("反事实确认", SKILL)
        self.assertIn("连续两轮没有新证据", SKILL)
        self.assertIn("候选方向、置信度、证据缺口和下一验证动作", SKILL)

    def test_fix_is_minimal_anti_bandaid_and_reenters_on_failure(self) -> None:
        self.assertIn("离根因最近的位置实施最小修复", SKILL)
        self.assertIn("直击失效机制而非用吞错或宽容兜底掩盖症状", SKILL)
        self.assertIn("默认给出一个推荐方案", SKILL)
        self.assertIn("用户只要方案时，写清修改位置、关键改动、验证命令和预期结果", SKILL)
        self.assertIn("修改后观察此前失败的复现或回归检查转为通过，保持原有测试断言强度", SKILL)
        self.assertIn("复测原始未简化场景与相关现有检查，并清理临时调试内容", SKILL)
        self.assertIn("先核对或回退本次改动，把新失败作为反证回到第 2 步重查根因", SKILL)
        self.assertIn("失败、中断和未运行项连同原因随结果说明", SKILL)

    def test_generalization_checks_mechanism_within_bounded_scope(self) -> None:
        self.assertIn("以失败机制而非相似文本界定同类风险", SKILL)
        self.assertIn("受影响组件、兄弟实现和直接调用点", SKILL)
        self.assertIn("搜索命中只作为待核实线索", SKILL)
        self.assertIn("扩大修改范围前取得用户确认", SKILL)
        self.assertIn("已证实缺陷、待核实线索和已排除项", SKILL)
        self.assertIn("`wiki-data` 时交给其 `ingest`", SKILL)

    def test_delivery_uses_plain_language_and_omits_empty_sections(self) -> None:
        self.assertIn("用白话短句结论先行", SKILL)
        self.assertIn("只输出有内容的区块并省略空段", SKILL)
        self.assertIn("让每项明确要求对应产物、回答或运行证据", SKILL)
        self.assertIn("只呈现关键证据、验证盲区与必要的回滚说明", SKILL)
        self.assertIn("简单问题直接合并为结论与验证两句", SKILL)


if __name__ == "__main__":
    unittest.main()
