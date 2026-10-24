# plan：当前最小计划与验证策略

## 目的
把 criterion 变成当前可执行的一小组动作，不预设后续所有细节。

## 进入条件
目标与 criterion 已明确，但 PLAN.md 缺失、已失效或下一动作不可执行。

## 跳过条件
PLAN 与当前事实一致，下一步和验证方式明确；直接沿用。

## 所需输入
TASK 目标 / criterion、用户限制、context/current 和已有相关产物。

## 执行方法
1. 写当前最少的动作与对应验证；没有把握的后续只写触发条件，不提前细化。
2. direct 任务用 PLAN checkbox 跟踪实施；OpenSpec 的具体 change checklist 由 taskflow 生成。
3. 涉及写删迁、共享配置或难逆动作，写备份 / 回滚并按确认协议停。
4. 出现交付边界时转 decompose，不在 PLAN 再抄一份父子状态。

## 产出
`PLAN.md`：当前步骤、验证策略、必要约束和产物指针。

## 完成门
每个当前步骤可执行、可验证，最后能走到 criterion；没有隐含扩大范围。

## 退出与重入
按 router 选下一 reference。新事实使步骤失效时只改未执行部分，已勾项保留证据。
