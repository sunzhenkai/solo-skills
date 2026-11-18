# 修正 agent-roster 的委派文案

- target: skills/agent-roster
- mode: update
- patch: 20261118-235654-fix-delegation-wording
- risk: low
- status: proposed

## Intent

把 description 中的「把定计划」改为「把计划制定」，消除语病；不改变委派、名册或 flow 模式的触发与执行行为。

## Conflict check

none

## Rationale

这是单个描述短语的文案修正，不改变现有契约，可由既有 agent-roster 测试和风格检查回归。

## Files

- `skills/agent-roster/SKILL.md`：修正 description 语病。

## Validation

- `git apply --check --recount` 校验 patch。
- 运行 agent-roster 契约测试。
- 运行 `make check-style`、仓级检查与全量测试。
