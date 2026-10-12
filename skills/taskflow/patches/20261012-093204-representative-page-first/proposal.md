# Web UI 实现先修订代表页

- target: skills/taskflow
- mode: update
- patch: 20261012-093204-representative-page-first
- risk: medium
- status: proposed

## Intent

页面实现仍委托 ui-template-apply。先修订一条主流程代表页，功能切片不代替这次修订。已共享的 token 变更仍走 design iterate。

## Conflict check

与 gate-packs、taskrail 的代表页要求一致。并行切片仍不在 apply 内改 core。

## Rationale

实现委托与完成门使用同一条通用规则。

## Files

- skills/taskflow/SKILL.md

## Validation

- git apply --check
