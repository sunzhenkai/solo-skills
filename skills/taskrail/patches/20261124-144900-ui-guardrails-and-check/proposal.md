# 升级 ui_evidence_check.py 为分级机械门（L1 快检 + L2 完整门）

- target: skills/taskrail
- mode: update
- patch: 20261124-144900-ui-guardrails-and-check
- risk: medium
- status: applied

## Intent

补齐运行态 UI 证据门的检测盲区并降低普通 UI 改动的使用门槛：
- 新增 L1 快检（`--quick --base-url <url> --routes ...`），免手写 manifest，普通 UI 改动默认可跑；缺 `axe-core` 时标 `skipped` 不阻断其余检查。
- 补齐 `pageerror` / `console.error` / 资源 4xx-5xx / `requestfailed`、裂图、横向溢出（含元凶定位）、外扩环裁切、极小热区（`<24px` 阻断 / 移动端 `<40px` 告警）、sticky/fixed 焦点遮挡检测。
- L2 完整门新增 `overlays` 交互浮层核对（打开可见、内边距防贴边、内部无溢出、焦点进入、`Esc` 关闭与焦点归还），默认 `dpr=2.0`。

## Files

- `skills/taskrail/scripts/ui_evidence_check.py`：实现 L1/L2 机械门升级。
- `skills/taskrail/references/ui-delivery.md`：普通 UI 改动升级为默认 L1 快检，机械门拆清 L1/L2/L3。
- `skills/taskrail/tests/test_ui_evidence_check.py`：新增单测覆盖 quick 模式、runtime/dom/focus_obscured/overlays 汇总与坏页 HTML fixture 测试。
