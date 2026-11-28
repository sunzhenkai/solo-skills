# 精简过程复盘入口

- target: skills/session-wrap
- mode: update
- patch: 20261123-181920-trim-process-entry
- risk: low
- status: proposed

## Intent

压缩 SKILL.md 中重复的过程复盘取证说明，只保留触发条件、reference 入口和普通收尾边界。取证规则仍以 process-review.md 为真源，行为不变。

## Conflict check

none

## Rationale

上一 patch 后 SKILL.md 仍为 8289 B；继续下沉重复说明即可低于 8192 B，无需改动既有正文或新增机制。

## Files

- skills/session-wrap/SKILL.md：精简过程复盘入口句。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、相关测试及 `make check-style`，确认体量低于 8192 B。
