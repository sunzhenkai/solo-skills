# 下沉过程复盘输出细则

- target: skills/session-wrap
- mode: update
- patch: 20261123-181738-compact-wrap-entry
- risk: low
- status: proposed

## Intent

将过程复盘的输出衔接细则保留在 process-review.md，SKILL.md 只留按需入口，避免本次变更新增 SKILL 体量告警。行为与输出契约不变。

## Conflict check

none

## Rationale

首次 patch 应用后 SKILL.md 为 8436 B，超过 8192 B 风格阈值；输出细则已在 reference 中完整定义，无需在正文重复。

## Files

- skills/session-wrap/SKILL.md：移除重复的输出衔接句。
- skills/session-wrap/tests/test_session_wrap_contract.py：将输出衔接断言指向实际真源 process-review.md。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、相关测试及 `make check-style`，确认不再新增体量告警。
