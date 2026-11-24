# 对齐通用实现防错护栏并衔接 overlays 机械门

- target: skills/ui-kit
- mode: update
- patch: 20261124-144900-ui-guardrails-and-check
- risk: low
- status: applied

## Intent

拉齐模板路线与通用路线的实现防错口径，并在交互态验收中衔接 taskrail 运行态机械门的 `overlays` 自动核对与 `Esc` 焦点归还检查。

## Files

- `skills/ui-kit/references/language.md`：§1 原则对齐 `pretty-ui/references/guardrails.md`。
- `skills/ui-kit/references/verify.md`：交互态清单补焦点进入与 `Esc` 归还，并注明可写进 manifest `overlays` 自动核对。
- `skills/ui-kit/tests/test_ui_kit_contract.py`：新增对应守卫断言。
