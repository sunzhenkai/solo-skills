# verify：判据、回归与集成验证

## 目的
用当前代码和可复验证据证明交付成立，而不是用计划、checkbox 或归档状态代替。

## 进入条件
当前实施项已完成，或父任务的直接子任务全部 done。代码任务不得跳过。

## 跳过条件
仅纯问答且无交付物；其他情况无跳过。

## 所需输入
criterion、PLAN / driver 验证记录、交付标准、当前 worktree、子任务 SUMMARY（若为父任务）。

## 执行方法
1. 在对应 worktree 跑 focused tests，再跑受影响的静态检查与回归；命令和结果写证据文件，摘要有路径。
2. 对照 criterion、用户“不做”和交付标准逐项核对；代码变化后旧证据失效。
3. 父任务必须执行 ROADMAP 集成项和跨仓主流程，再验总判据；不能只汇总子任务结论。
4. reviewer Blocker / Major 必须 fixed 或 accepted-recorded 带理由；缺证据不能标通过。
5. Web UI、性能、安全等按命中的质量包补证据。

## 产出
当前任务的验证记录与证据指针；direct 写 PLAN / evidence，OpenSpec 写 driver proposal 验证记录。

## 完成门
[done.md](done.md) 除 SUMMARY / 归档动作外全部满足；任何未验证项按实际缩小交付处理，不能静默通过。

## 退出与重入
全过进 close；实现问题回 execute，原因不明回 diagnose，方案问题回 design / grill。
