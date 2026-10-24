# taskflow：direct / OpenSpec 执行纪律

worktree 唯一真源是 [worktree.md](worktree.md)；OpenSpec 固定 Driver 协议在 [driver-template.md](driver-template.md)。

## 进度归属

- direct：PLAN checkbox 记实施，evidence 记验证；不创建第二份完成度。
- OpenSpec：子 change tasks.md 记实施，driver tasks.md 记编排；对应子 change 全勾、validate 通过、该片已提交后才勾 driver 项。
- 父子结构只看 ROADMAP 与子 TASK，不在父 driver 再复制一套子任务进度。
- 涉及仓库角色只有必须（会改）/ 建议（只读）/ 排除。

## 实施中

- 一次完成一个连贯增量，先 focused tests，再提交；同任务同仓写操作串行。
- 单项做不了保持未勾并写原因，继续其他就绪项；工具故障与代码根因分开，真阻塞只停依赖项。
- 测试失败且原因明确继续 execute，原因不明回 diagnose；契约 / 方案不足回 design / grill；独立交付边界回 decompose。
- 不缩小 criterion；确需缩小时回 intent / approve。
- worker 输入只含本人范围、criterion、相关契约与证据、worktree 绝对路径；返回摘要、路径、未决，不回灌原始日志。

## 收尾校核

- 当前代码的验证证据有效；换代码后旧证据作废。
- OpenSpec 子 changes 勾齐再归档，未勾齐就不归档；归档前 validate 通过，`--yes` 只用于已校核的非交互命令，不得掩盖未勾项。
- 片间检查点只核对证据、提交和下一就绪片，不额外停人；提交由编排者做。
- reviewer Blocker / Major 有 fixed 或 accepted-recorded 理由。
- driver 归档只表示 OpenSpec 执行收尾，随后必须回 taskrail verify / close，并按 [done.md](../../taskrail/references/done.md) 验收；不直接标任务 done。
