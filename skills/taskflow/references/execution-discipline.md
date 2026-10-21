# taskflow：执行纪律

Driver 协议逐字块在 [driver-template.md](driver-template.md)，建 worktree 与「一轮结束」规则只以它为准。

## 进度归属

- 子 change 的 `tasks.md` 记实现，driver 的 `tasks.md` 记编排。driver 某条实施项只在对应子 change 全勾、`openspec validate --strict --type change {task}-<slice>` 通过、这一片已提交到任务分支后勾。
- 不另存完成度、暂缓或分支状态；暂缓原因写 driver `proposal.md` 验证记录。
- 涉及面角色只有 `必须`（会改）/ `建议`（只读）/ `排除`。

## 实施中

- 默认串行，一次一个子 change；做完一个先提交、过片间检查点（Driver 协议），再展开、做下一个。
- 单项做不了就保持未勾，在验证记录写一行原因，继续下一项；只有真阻塞（[user-report.md](../../taskrail/references/user-report.md) 第 5 节）才停依赖它的条目，按 user-report 四行说。
- 发现会少交付的地方：不缩判据的记进「已做决定」继续；缩判据或交付面的是改判据，停下等用户。
- 实现者输入：判据原文、本人负责范围、相关验收要求与证据、运行约束（工作目录 = `worktrees/{task}` 的绝对路径；提交留给编排者，不 push、不外发）。

## 收尾校核

对 driver 做 stock 归档前逐条核对：

- 子 change 全勾且各自 `validate --strict` 通过；driver 实施项与之一致。
- 每轮评审的 Blocker / Major 都有处置（`fixed` / `accepted-recorded` 带理由）。
- 证据与当前代码一致（换代码后旧证据作废，重跑受影响部分）。
- [done.md](../../taskrail/references/done.md) 全过。

`openspec archive` 报未勾时先回填真实状态或保持未勾，勾齐再归档：归档后记录不可回改，未勾齐就不归档（`--yes` 不用来盖过未勾项）。
