# 新增实现期防错护栏并同步量测口径

- target: skills/pretty-ui
- mode: update
- patch: 20261124-144900-ui-guardrails-and-check
- risk: low
- status: applied

## Intent

把高频结构性 UI bug（Flex/Grid 溢出、外扩环裁切、嵌套宽度阈值、浮层贴边/双线/焦点归还、切页卸载壳、四态缺失、无障碍底线）前移到实现阶段，减少写代码时的返工，并同步浏览器量测片段的裂图与极小热区检查。

## Files

- `skills/pretty-ui/references/guardrails.md`：新增 14 条实现期防错护栏（G-L1..G-A3）。
- `skills/pretty-ui/SKILL.md`：`小改`、`build` 第 5 步与「按需读取」接入 `guardrails.md`（保持 < 8KB）。
- `skills/pretty-ui/references/evidence.md`：第 3 节量测片段新增 `裂图`、`极小热区` 检查。
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`：新增 `GuardrailsTest` 及量测守卫断言。
