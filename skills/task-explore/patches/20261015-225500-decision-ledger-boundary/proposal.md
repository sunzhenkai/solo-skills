# 难回头的决定单独说 + 真阻塞边界 + 一本决定账

- target: skills/task-explore
- mode: update
- patch: 20261015-225500-decision-ledger-boundary
- risk: low
- status: applied

## Intent

TASK.md 模板「## 决策」改为「## 已做决定」表（决定 / 理由 / 可逆 / 来源阶段）；commands / approve / ledger 改指新表；grill 结论追加到该表。

## Conflict check

接续 20261015-224500-statements-not-questions；定义只在 taskrail user-report「说决定，不提问」，其余为指针。

## Files

见 change.patch。
