# taskflow：driver 模板与 propose 产出约定

由 [../SKILL.md](../SKILL.md)「脚手架」引用。本文件的 **Driver 协议** 块是切分支、一轮结束等规则的**唯一真源**，其余文件只引用不复述。

## 脚手架细则

`skip_specs: true` 必须显式写入：driver 无 spec 增量，不写这行会让 `openspec validate --strict` 失败；写了之后 `openspec status --change {task}-driver --json` 中 specs 为 `skipped`。

**不要写 `tasks.md`。** 它留给 propose 阶段：stock `openspec-propose` 只处理未完成的 artifact，脚手架把 tasks 写满会让它空转，留出空缺才会读 proposal 并按协议产出登记了子 change 的 `tasks.md`。这也是协议必须写在 proposal 而不是别处的原因——`openspec instructions apply --json` 的 `contextFiles` 保证 proposal 必然被读到。

### driver `proposal.md` 模板

`Driver 协议` 小节是固定文本，逐字写入，不要改写或精简；其余小节按任务填写。

上游传入的质量画像与显式降级原文是完成判据的约束，不是可摘要的背景。任务描述含质量画像原文或显式降级表时，`Why` 逐字保留该快照，不摘要、不改写、不用小节指针或路径替代；任务描述没有这些内容时不编造画像与降级条目。

填写「验收标准」时：任务描述含完成判据，第一条 checkbox 使用该判据原文。任务描述没有完成判据时按任务填写，不另造一条判据。这条验收标准不代替 driver `tasks.md` 的编排进度；进度仍只认 checkbox。脚手架仍不要写 `tasks.md`。

任务描述含质量画像时，验收标准除上面的完成判据原文外至少再写三条：画像原文快照已逐字进入本 proposal；每条角色底线写明验证方式（运行时行为、截图或测试证据）；`pending` 降级数为 0。`confirmed` 降级在验证记录里逐项写明维度、实际选择与用户确认来源，保持可追踪。

````markdown
## Why
<任务描述>

## What Changes
- 本 change 是 taskflow driver，不直接改代码，只编排子 change

## Non-goals
- <...>

## 涉及面
| 仓库 | 角色 | 说明 |
|------|------|------|
| . | 必须 | 会修改 |

## 验收标准
- [ ] <...>

## Driver 协议
- 本 change 无 spec 增量（`.openspec.yaml` 已设 `skip_specs: true`）
- 子 change 一律命名 `{task}-<slice>`，与本 change 同一 planning root；跨 root 时在涉及面表显式记录 root 或 store id
- 实现进度只认子 change 自己的 `tasks.md`；本文件的 checkbox 只在对应子 change 全勾且 `validate --strict` 通过后才勾
- 切任务分支只针对涉及面里角色为 `必须` 的修改仓，且本身可选；task 所在仓不是修改仓时不切。修改仓干净：先 fetch 默认分支，再从其最新提交 `git switch -c`（分支已存在则 `git switch`）。修改仓 dirty：列出未提交路径，由用户三选一——不切直接在当前分支修改 / 携带改动 `git switch` / `git worktree add` 从默认分支最新提交建独立工作树。不得 stash / reset / 强制切换。用户未选择、git 拒绝或切错仓时停下
- 只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮；单项做不了就保持未勾，在验证记录写一行原因后继续下一项；「需要用户决策」只停依赖该项的条目，其余条目继续
- 结束时逐条列出未勾项与原因，不按 change 汇总

## 验证记录
````

### 脚手架输出

报告 change name、`proposal.md` 路径、涉及面与验收标准里仍需用户确认的空缺，并桥接到 stock `openspec-propose`（方案未定时先 `openspec-explore`）。

仍需用户确认的空缺里，每个 `pending` 降级单独列一条，写明维度、默认期望、实际选择与原因；不合并成「降级待确认」这类汇总条目，也不由 agent 代用户确认。

同时提示：driver 已存在 proposal，`openspec-propose` 会问「继续已有 change 还是新建」，**应选继续**。

## propose 阶段的产出约定

`openspec-propose` 对 driver 产出的 `tasks.md` 按下列骨架组织：准备段切分支，实施段每个子 change 至少一条，收尾段含回归、回填验收、提交与逐个子 change 的归档条目。

收尾段的回归按 [references/delivery-quality-loop.md](delivery-quality-loop.md) 执行（静态门 / 窄切片 / 全链路三层，失败先归因再修）；验收按 [references/acceptance-rubric.md](acceptance-rubric.md) 出分，缺分或缺证据不勾收尾条目。

子 change 的 artifacts 在 propose 阶段一次性备齐（拆分粒度本身是提案决策），apply 阶段只做实施，不在实施循环里改 change 语义。

````markdown
## 1. 准备
- [ ] 1.1 （可选）把涉及面里角色为必须的修改仓切到任务分支：干净则从默认分支最新代码切；dirty 则列出路径，由用户在不切直接改 / 带脏切换 / git worktree 独立工作树中三选一

## 2. 实施
- [ ] 2.1 完成子 change `{task}-api`：apply 至全部 checkbox 勾选且 validate --strict 通过
- [ ] 2.2 完成子 change `{task}-ui`：Web UI 切片消费 frozen Active Instance（代表页 two-pass 先行）；无 Active Instance 且无已确认 adopt-only 降级时禁止直接铺业务页；其余同 2.1

## 3. 收尾
- [ ] 3.1 全仓回归与静态检查，命令与结果写入 proposal 验证记录
- [ ] 3.2 回填 proposal 验收标准
- [ ] 3.3 提交交付仓改动
- [ ] 3.4 归档前置校核：子 change 全勾且 validate 通过、降级无 `pending`、findings 全有 disposition（见「收尾机械校核」）
- [ ] 3.5 归档全部子 change
````

子 change 的归档是收尾段的普通 checkbox，在 apply 阶段完成。因此 driver 全勾时子 change 已全部 `openspec archive`，对 driver 执行 stock 归档不需要任何递归处理。
