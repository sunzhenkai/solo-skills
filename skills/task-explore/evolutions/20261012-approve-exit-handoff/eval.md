# Eval：approve-exit-handoff（20261012，task-explore）

## 回归

- 生产稿未改。全仓基线 **495 passed, 2 skipped**。
- 候选暂存后 **497 passed, 2 skipped**。既有 archive 断言（不要求清零、随归档关闭、关闭原因取自用户）仍过。

## 模式

- phase-approve：下一步只写 handoff；不列 archive / 另起任务 / 继续探索；未决不改推 archive；禁止改写 criterion；实施线进同一 driver 的子 change。
- phase-archive：方案已冻结且含实施、尚未 handed-off 时拒绝进入，改走 handoff。「方案已写完」「还有未决」不是关闭原因。用户明确放弃或不实施时不拦截。
- SKILL.md archive 摘要与阶段细则同一句。

## 契约

- 第一级：候选暂存后新断言与既有 task-explore 契约通过。
- 第二级：与 taskrail 同轮，候选暂存全仓 497 passed。

## 副作用

- 未改 handoff 不归档、父任务纯伞、子任务一层、未决不要求清零。
- 过拟合：无项目名、路径、密钥。

## 结论

pass
