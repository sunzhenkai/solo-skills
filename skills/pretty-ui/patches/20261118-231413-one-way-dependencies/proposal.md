# Proposal：pretty-ui 保持独立通用能力

## Intent
移除 pretty-ui 对 ui-kit 的反向感知。pretty-ui 只描述自身通用 UI 设计、实现与评审能力和直接点名入口；ui-kit 与它的调用关系只由 ui-kit 侧持有。

## Files
- `skills/pretty-ui/SKILL.md`
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`

## Tests
验证直接点名入口和运行文档不包含 ui-kit；既有方向、证据、规则、评审和停止标准测试不变。
