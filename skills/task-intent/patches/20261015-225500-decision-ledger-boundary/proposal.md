# 难回头的决定单独说 + 真阻塞边界 + 一本决定账

- target: skills/task-intent
- mode: update
- patch: 20261015-225500-decision-ledger-boundary
- risk: low
- status: applied

## Intent

复述中难回头的决定单独一句并指向 user-report 定义；「我的决定」同步追加到 TASK.md「已做决定」；示例补一条难回头说明；新增 eval。

## Conflict check

接续 20261015-224500-statements-not-questions；定义只在 taskrail user-report「说决定，不提问」，其余为指针。

## Files

见 change.patch。
