# Proposal：ui-kit 单方持有路由依赖

## Intent
修复把上游编排名写入独立下游的反向耦合。依赖方向只由 ui-kit 指向 pretty-ui、ui-template 等能力；下游无需知道 ui-kit。ui-template 三件套恢复原状，pretty-ui 的独立性由其自身测试保证。

## Files
- `skills/ui-kit/SKILL.md`
- `skills/ui-kit/tests/test_ui_kit_contract.py`

## Tests
验证单向依赖正文契约；既有 React/非 React 分派、专项衔接和模板验收测试保持通过。
