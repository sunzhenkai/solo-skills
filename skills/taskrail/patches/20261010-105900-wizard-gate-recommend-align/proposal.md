# wizard 闸口与含推荐对齐

- target: skills/taskrail
- mode: update
- patch: 20261010-105900-wizard-gate-recommend-align
- risk: medium
- status: proposed

## Intent

薄对齐 task-confirm 的 human「含推荐」契约：contract human 行补「含推荐」；wizard 禁止空问清单；定稿委托前未决口子须已带推荐；坑写成「推荐=…」。不改阶段机、档位或完成门。

## Conflict check

none。与已应用的 `task-confirm` patch `20261010-105830-human-gate-recommend` 一致。

## Rationale

编排侧若仍可空问再交 confirm，体验缺口会回潮。对齐委托边界即可。

## Files

- `skills/taskrail/references/contract.md`
- `skills/taskrail/references/phase-wizard.md`
- `skills/taskrail/tests/test_taskrail_contract.py`

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/taskrail/tests skills/task-confirm/tests -q`
