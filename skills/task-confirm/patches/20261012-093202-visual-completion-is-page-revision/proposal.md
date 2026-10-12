# Web UI 视觉完成认代表页修订

- target: skills/task-confirm
- mode: update
- patch: 20261012-093202-visual-completion-is-page-revision
- risk: medium
- status: proposed

## Intent

视觉层次、密度、排版节奏的完成证据是代表页源码及其修订。Gallery 与 digest 只证明系统未漂。

## Conflict check

Active Instance 仍是系统约束。无 freeze 时 medium/complex 仍移交 design。

## Rationale

通用 Web UI 完成门认实现产物，不认检查指针。

## Files

- skills/task-confirm/references/gate-packs.md
- skills/task-confirm/evals/cases.yaml

## Validation

- git apply --check
- YAML 可解析
