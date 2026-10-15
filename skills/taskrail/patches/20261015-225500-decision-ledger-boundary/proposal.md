# 难回头的决定单独说 + 真阻塞边界 + 一本决定账

- target: skills/taskrail
- mode: update
- patch: 20261015-225500-decision-ledger-boundary
- risk: low
- status: applied

## Intent

user-report 第 5 节：真阻塞补「删除或迁移数据、改共享配置」；新增「不停」的普通取舍例与「难回头的决定」定义（单独一行「我定了 X，因为 Y」）；决定追加到 TASK.md「已做决定」，完成通知指向它。contract 一本账写明唯一决定表；confirm-protocol 闸口决定追加到该表；示例 TASK.md 改用新表；新增边界双向测试与 3 条 eval。

## Conflict check

接续 20261015-224500-statements-not-questions；定义只在 taskrail user-report「说决定，不提问」，其余为指针。

## Files

见 change.patch。
