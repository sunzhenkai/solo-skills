# Web UI 实现委托 ui-template-apply

- target: skills/taskflow
- mode: update
- patch: 20261011-171254-web-ui-active-instance
- risk: medium
- status: proposed

## Intent

UI 切片委托 ui-template-apply；契约/证据绑 digest、Gallery、Phase 8；rubric 与质量环对齐 DS runtime。

## Conflict check

不在本 skill 复制 design 0–9；改 core 移交 ui-template-design iterate。

## Rationale

执行段是唯一写业务页的入口，必须强制消费 Active Instance。

## Files

- skills/taskflow/SKILL.md
- skills/taskflow/references/delivery-quality-loop.md
- skills/taskflow/references/acceptance-rubric.md
- skills/taskflow/tests/test_execution_spine_contract.py
- skills/taskflow/evals/cases.yaml

## Validation

- `python3 -m pytest skills/taskflow -q`
