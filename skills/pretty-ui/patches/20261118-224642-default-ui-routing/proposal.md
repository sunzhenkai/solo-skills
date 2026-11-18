# Proposal：pretty-ui 作为通用路线下游

## Intent
保留 pretty-ui 全部设计、实现、截图打磨与评审能力，把自动定位收窄为 ui-kit 的既有/非 React 通用路线，同时保留用户直接点名调用，消除两个宽泛默认入口的竞争。

## Files
- `skills/pretty-ui/SKILL.md`
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`

## Tests
验证 frontmatter 的 ui-kit 分派关系、正文边界与直接点名兼容性；原有方向、证据、规则和停止标准测试不变。
