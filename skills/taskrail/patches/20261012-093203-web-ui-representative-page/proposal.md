# Web UI apply 与完成门要求代表页

- target: skills/taskrail
- mode: update
- patch: 20261012-093203-web-ui-representative-page
- risk: medium
- status: proposed

## Intent

Web UI 的 apply 先走 ui-template-apply，按 frontend-design 实现并修订一条主流程代表页。完成门另须这份实现记录。

## Conflict check

非 Web UI 的 apply 仍只认 OpenSpec checkbox。digest 一致性保留。

## Rationale

编排完成门与实现顺序对齐，不增加新的检查清单。

## Files

- skills/taskrail/SKILL.md

## Validation

- git apply --check
