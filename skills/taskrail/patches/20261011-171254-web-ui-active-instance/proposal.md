# Web UI Active Instance 编排门禁

- target: skills/taskrail
- mode: update
- patch: 20261011-171254-web-ui-active-instance
- risk: medium
- status: proposed

## Intent

wizard 记录 Active Instance 状态；契约阶段载荷与完成门核对三条 digest；依赖表声明 ui-template-*。

## Conflict check

不新增 phase；DS 本体仍落交付项目根，不进 tasks/。

## Rationale

编排入口须在定稿前暴露 freeze 缺口，并在 done 时防 digest 漂移。

## Files

- skills/taskrail/SKILL.md
- skills/taskrail/references/contract.md
- skills/taskrail/references/phase-wizard.md
- skills/taskrail/tests/test_deliverable_class_contract.py
- skills/taskrail/evals/cases.yaml

## Validation

- `python3 -m pytest skills/taskrail -q`
