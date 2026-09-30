---
id: taskflow
name: taskflow
description: "把一个任务拆成多个 OpenSpec change 并推进到底：`taskflow-new` 建 `{task}-driver`，四个阶段委托 stock `openspec-*`，进度只认 OpenSpec checkbox。在用户点名 taskflow、执行 `taskflow-new`、跟进 `{task}-driver`、要把一个任务拆成多个 OpenSpec change 时使用。"
---

# taskflow

面向用户默认使用简体中文；命令、路径、代码、状态值与既成术语保持原文。

一个任务 = 一个 driver change `{task}-driver`。实现拆成若干子 change `{task}-<slice>`，与 driver 同一 planning root；跨 root 时在 driver 涉及面表里显式记录 root 或 store id。共享 `{task}` 前缀让 `openspec list` 直接看出归属，不需要额外元数据。

**进度只有 checkbox 一种真相。** 不建 `tasks/` 台账、不写索引文件、不引入编号体系、不带脚本。

## 阶段路由

| 阶段 | 入口 | 参数 |
|------|------|------|
| 立项 | 本文件「脚手架」小节（command `taskflow-new`） | 任务描述 |
| 澄清 | stock skill `openspec-explore` | `{task}-driver` |
| 提案 | stock skill `openspec-propose` | `{task}-driver` |
| 实施 | stock skill `openspec-apply-change` | `{task}-driver` |
| 归档 | stock skill `openspec-archive-change` | `{task}-driver`（只归档 driver 自身） |

taskflow 只提供 `taskflow-new` 一个 command，四个阶段一律复用 stock skill，不另造等价命令。

## 委托契约

`openspec-*` skill 默认由 `dotf agents -c` 装到全局 `~/.agents/skills`（`openspec init --tools agents`），**不是每个仓都自带**。委托前确认当前 agent 环境能读到它们；不可用就停下报告并给出可选项（跑 `dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调），**不要自行发明等价命令**。

可用时，委托必须同时具备两项绑定：**在 driver 的 planning root 下执行**，并**显式给出 change name `{task}-driver`**。缺任一项不得委托——openspec CLI 只认 cwd 最近的 `openspec/`，无绑定会写错位置或反问用户选 change。无法确定时停下报告。

## 脚手架

`taskflow-new {任务描述}` 固定三步，不多做：

1. 由任务描述归纳 kebab-case 的 `{task}`（Agent 自己归纳，不追问用户；描述确实为空时才问「要做什么？」）。
2. `openspec new change {task}-driver --goal "<任务描述原文>"`。
3. 在该 change 的 `.openspec.yaml` 补 `skip_specs: true`，再按下方模板写 `proposal.md`。

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

收尾段的回归按 [references/delivery-quality-loop.md](references/delivery-quality-loop.md) 执行（静态门 / 窄切片 / 全链路三层，失败先归因再修）；验收按 [references/acceptance-rubric.md](references/acceptance-rubric.md) 出分，缺分或缺证据不勾收尾条目。

子 change 的 artifacts 在 propose 阶段一次性备齐（拆分粒度本身是提案决策），apply 阶段只做实施，不在实施循环里改 change 语义。

````markdown
## 1. 准备
- [ ] 1.1 （可选）把涉及面里角色为必须的修改仓切到任务分支：干净则从默认分支最新代码切；dirty 则列出路径，由用户在不切直接改 / 带脏切换 / git worktree 独立工作树中三选一

## 2. 实施
- [ ] 2.1 完成子 change `{task}-api`：apply 至全部 checkbox 勾选且 validate --strict 通过
- [ ] 2.2 完成子 change `{task}-ui`：同上

## 3. 收尾
- [ ] 3.1 全仓回归与静态检查，命令与结果写入 proposal 验证记录
- [ ] 3.2 回填 proposal 验收标准
- [ ] 3.3 提交交付仓改动
- [ ] 3.4 归档全部子 change
````

子 change 的归档是收尾段的普通 checkbox，在 apply 阶段完成。因此 driver 全勾时子 change 已全部 `openspec archive`，对 driver 执行 stock 归档不需要任何递归处理。

## 纪律

### 进度归属

- 子 change 的 `tasks.md` 记**实现**进度，driver 的 `tasks.md` 记**编排**进度，后者必然滞后于前者。
- driver 的某条实施 checkbox 只在对应子 change 全部 checkbox 已勾、且在其 planning root 下 `openspec validate --strict --type change {task}-<slice>` 通过之后才允许勾选。
- 不持久化第二份完成度、暂缓或分支状态记录。暂缓原因写进 driver `proposal.md` 的验证记录小节。
- 已知代价：`openspec archive` 对未勾 checkbox 不设防。完成度靠上述纪律与 stock skill 的确认环节，taskflow 不补脚本。

### 涉及面与交付分支

- 角色只有三个取值：`必须`（会修改）、`建议`（只读参考）、`排除`。`建议` 与 `排除` 仓保持只读。
- 切分支规则的唯一真相是上方 Driver 协议模板（逐字写入每个 driver proposal）：只针对 `必须` 修改仓且本身可选，task 所在仓不是修改仓时不切；干净从默认分支最新提交切；dirty 由用户三选一；禁止 stash / reset / 强制切换，用户未选择或 git 拒绝时停下。
- 模板之外的增量：部分仓已准备成功、其它仓停下时，已准备成功的仓保留现状以便重试。

### 质量画像与降级确认

- 质量画像与显式降级原文快照由上游任务描述带入 driver proposal，实施阶段不改写、不删减，只按下面规则补新发现的降级。
- 子 change 实施中发现新的生产性降级——凡比默认期望少交付的都算，改名成「技术选型」「本期简化」也一样——先按 [../../task-goal/references/quality-profile.md](../../task-goal/references/quality-profile.md) 定级。**A 类**（缩完成判据或交付面；拿不准归 A）：标 `pending`，写入 driver `proposal.md` 的验证记录，作为需要用户决策的项停下等用户，不静默接受、不自行确认。**B 类**（判据与交付面都不缩）：经审阅收敛临时确认记 `provisional`，不停机不等用户，到用户在场点（真人门、收口）集中追认。这命中 Driver 协议「一轮结束」三条件里的「需要用户决策」；不依赖该决策的其余条目仍按「一轮结束」继续。
- 执行者、子代理与审阅收敛都不算用户确认；B 类 `provisional` 是唯一例外——经审阅收敛写入，但只算临时确认，追认前不算 `confirmed`。用户点名接受该项、明确全部确认、按意图命中已列授权项（复述生效，见 [../../task-goal/SKILL.md](../../task-goal/SKILL.md)「授权」节）、或在用户在场点追认后，才允许勾相关验收标准 checkbox，并在验证记录把该项记为 `confirmed`，保留维度与实际选择以便追踪；追认否决按该项回滚说明处理后回降级确认门重定级。
- driver 的最终验收必须按 [references/acceptance-rubric.md](references/acceptance-rubric.md) 给出五维分数与证据，并满足五维均 ≥2、UI/UX 均值 ≥2.5；缺分不得勾验收标准 checkbox。

### 一轮结束

规则的唯一真相是上方 Driver 协议模板：只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮；单项做不了保持未勾、在验证记录写一行原因后继续其余条目；结束时逐条列出未勾项与原因。

模板之外的增量：不因一项卡住就整轮停下；不把未完成项勾成完成；不用「某 change 还剩 3 项」这类按 change 汇总的数量代替逐条说明。

「需要用户决策」结束一轮时，按 [../../task-goal/references/suspension.md](../../task-goal/references/suspension.md) 的挂起五元组呈现（等待项、授权形状、阻塞面、非依赖面、恢复触发）：依赖该决策的 checkbox 停，不依赖的继续按「一轮结束」推进，不整轮停摆。用户输入到达先比对授权形状——逐字点名或意图命中（复述生效）都算，命中即恢复对应条目，未命中重申仍停，不写成选项列表。

### 并行执行

有多 agent / 子代理能力时，对**无未完成依赖、范围不重叠**的单位优先并行；没有该能力则主会话串行，其余纪律不变。并行只改变执行方式，完成度仍只认 checkbox，不另建账本。

两层都可以并行：

| 层 | 单位 | 可以并行 | 必须串行 |
|----|------|----------|----------|
| change | 子 change `{task}-<slice>` | 落在不同必须仓，或主会话已确认实现范围不重叠 | 同一工作树且可能改同一批文件或互相依赖契约；准备段切分支；收尾段回归 / 回填 / 提交 / 归档 |
| task | 同一 change 的 checkbox | 互不依赖且文件范围不重叠 | 有先后依赖、共享同一文件、或需要用户决策 |

每个子代理只领一个单位（一个子 change，或同一 change 内一组已声明不重叠的 checkbox），并同时满足：

- 在该单位的 planning root 下执行，且显式给出 change name
- 只改自己范围内的代码与自己的 `tasks.md` checkbox
- 不勾 driver 编排项（仍由主会话在子 change 全勾且 `validate --strict` 通过后勾）
- 不发明等价命令，不扩大到 `建议` / `排除` 仓的写入

主会话负责派发、汇总、处理冲突与未勾原因。子代理失败或超时不是整轮结束理由，按「一轮结束」继续其余独立项。

### 实现者输入

默认正常交付：按 [references/implementer-isolation.md](references/implementer-isolation.md)，实现者必须拿到质量画像或保留语义的子范围裁剪、相关验收要求与运行约束；完整 rubric 和跨范围审阅意见仍由审阅者持有。普通任务不得盲派。

只有任务显式标记 benchmark / regression 时才盲测复跑：实现者只拿同一份样例/需求原文与运行约束，不拿画像、rubric、期望清单或审阅意见；复跑不追加事后提示。

---

## Self-evolution

本 Skill 从真实执行中积累经验，并按 Eval 验证改进。目录（均相对本 Skill 根目录）：

```text
skills/taskflow/
├── SKILL.md
├── examples/      # 经过验证的优秀执行案例
├── evals/         # 可验证成功标准（cases.yaml）
└── experience/    # 真实失败 / 成功 / 规律
```

自进化不改变上文已规定的目标、流程、工具用法、输出与约束。

- 执行复杂任务前先查 `examples/`，有相关成功案例就复用；没有就按正文执行，不编造案例。
- 任务完成前对照 `evals/cases.yaml` 验证关键输出；Eval 失败先修输出，不带着失败交卷。
- 完成后遇失败、用户纠正、明显成功或新的有效方法才写入 `experience/`：单次失败进 `failures/`，重复规律进 `patterns/`（至少两次同类证据）。不记 trivial 信息，不伪造条目，不写密钥 / 内部 URL / 凭据。
- 改生产正文：先出提案并经用户确认，再走 `skill-evolver`（`evolutions/`）或 `skill-upgrader` 的 `update` 模式（`patches/`）；禁止由单次失败直接改 `SKILL.md`。
