# 修正过程复盘取证断言真源

- target: skills/session-wrap
- mode: update
- patch: 20261123-182215-fix-process-test-source
- risk: low
- status: proposed

## Intent

将过程复盘取证规则的测试断言从 SKILL.md 改为 process-review.md，与规则下沉后的实际真源一致。契约要求和生产行为不变。

## Conflict check

none

## Rationale

最终契约测试因 SKILL.md 不再重复取证句而失败；reference 仍完整保留该规则，修正断言位置即可验证原契约。

## Files

- skills/session-wrap/tests/test_session_wrap_contract.py：将取证规则断言指向 PROCESS。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、session-wrap 测试、全仓测试与公开仓检查。
