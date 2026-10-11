# Web UI 基准物绑定 Active Instance

- target: skills/task-confirm
- mode: update
- patch: 20261011-171254-web-ui-active-instance
- risk: medium
- status: proposed

## Intent

将 Web UI 门包基准物从「tokens/组件契约散文」升级为交付项目根 frozen `design-system/v1` Active Instance（三条 digest）；补档位硬门、DS runtime 自动化门挂钩、实现委托 `ui-template-apply`。

## Conflict check

与既有「禁止外部产品当基准」「必载 roles=design」无冲突；明确 DS 本体由仓外 ui-template-* 维护，本 skill 只认指针。

## Rationale

task 系列此前有 UI 评审与门包，但无强制 freeze 的设计系统；与计划「双轨+硬门」对齐。

## Files

- skills/task-confirm/references/gate-packs.md
- skills/task-confirm/tests/test_reviewer_binding_contract.py
- skills/task-confirm/evals/cases.yaml

## Validation

- `python3 -m pytest skills/task-confirm -q`
