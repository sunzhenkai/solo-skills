# plan：当前最小计划与验证策略

## 目的
把 criterion 变成当前可执行的一小组动作，不预设后续所有细节。

## 进入条件
目标与 criterion 已明确，但 PLAN.md 缺失、已失效或下一动作不可执行；或即将 execute 而当前实施内容尚未完成所需确认。

## 跳过条件
PLAN 与当前事实一致，下一步和验证方式明确；若下一步是 execute，当前模式所需的实施确认已完成且覆盖当前实施内容。

## 所需输入
TASK 目标 / criterion、用户限制、context/current 和已有相关产物。

## 执行方法
1. 写当前最少的动作与对应验证；没有把握的后续只写触发条件，不提前细化。
2. direct 任务用 PLAN checkbox 跟踪实施；OpenSpec 的具体 change checklist 由 taskflow 生成。
3. 只读 explore / diagnose 可沿当前最小计划继续。首次 execute 前或实施方案实质变化后，human 按 [confirm-protocol.md](confirm-protocol.md) 展示改动范围、步骤、验证与必要回滚并等明确确认；goal 简要复述方案后继续。
4. 把确认状态、依据和覆盖范围写进 PLAN「实施确认」：human 以用户明确确认记 confirmed，goal 以简要复述已给出记 not-required。实施范围、步骤或验证策略实质变化后回 pending；只更新 checkbox 或证据不改变状态。
5. 每个实际执行的子任务首次 execute 前确认自己的当前 PLAN；继承父意图或范围内 approve 不代替这一步。
6. 涉及写删迁、共享配置或难逆动作，写备份 / 回滚并按确认协议停。
7. 出现交付边界时转 decompose，不在 PLAN 再抄一份父子状态。

## 产出
`PLAN.md`：当前步骤、验证策略、必要约束、产物指针和实施确认记录。

## 完成门
每个当前步骤可执行、可验证，最后能走到 criterion；没有隐含扩大范围。进入 execute 前，human 的当前实施内容必须为 confirmed，goal 已简要复述；确认前不得进入 execute 或写代码。

## 退出与重入
按 router 选下一 reference。新事实使步骤失效时只改未执行部分，已勾项保留证据；实施内容实质变化时重入本环节并重新确认。
