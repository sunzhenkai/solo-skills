# taskflow：driver 模板与 propose 产出约定

由 [../SKILL.md](../SKILL.md)「脚手架」引用。本文件的 **Driver 协议** 块是建 worktree、一轮结束等规则的**唯一真源**，其余文件只引用不复述。

## 脚手架细则

`skip_specs: true` 必须显式写入：driver 无 spec 增量，不写这行会让 `openspec validate --strict` 失败；写了之后 `openspec status --change {task}-driver --json` 中 specs 为 `skipped`。

**脚手架把 `tasks.md` 留给 propose 阶段**：stock `openspec-propose` 只处理未完成的 artifact，脚手架把 tasks 写满会让它空转，留出空缺才会读 proposal 并按协议产出登记了子 change 的 `tasks.md`。这也是协议必须写在 proposal 而不是别处的原因——`openspec instructions apply --json` 的 `contextFiles` 保证 proposal 必然被读到。

### driver `proposal.md` 模板

`Driver 协议` 小节是固定文本，逐字写入，不要改写或精简；其余小节按任务填写。

填写「验收标准」时：任务描述含完成判据，第一条 checkbox 用判据原文；没有判据时按任务填写，不另造。`Why` 写目标、判据原文与方案 / 批准路径（指针，不复制原文）。这条验收标准不代替 driver `tasks.md` 的编排进度。

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
- 子 change 按依赖分批展开：依赖的实施项都已勾的切片才建子 change，起草时以 `worktrees/{task}` 里的代码为准
- 实现进度只认子 change 自己的 `tasks.md`；本文件的实施项只在对应子 change 全勾、`validate --strict` 通过、这一片已提交到任务分支后才勾
- 每勾掉一条实施项过一次片间检查点，不停人：按新认识补拆、合并或改顺序（只增删、改写未勾的实施项，记进 `TASK.md`「已做决定」），再展开依赖已满足的下一批；动到判据或范围的，按 taskrail 契约「意图变更」处理
- 两个根：planning root（`tasks/`、`openspec/changes/`）留在主工作树，只增量写本任务的目录，`openspec-*` 命令在这里跑；代码根是修改仓根目录下的 `worktrees/{task}`，读改代码、测试、回归、提交都在这里做，派给实现者的工作目录写它的绝对路径
- 涉及面里角色为 `必须` 的 git 修改仓一律建 worktree；修改仓不是 git 仓、或用户原话要求就地改时才在主工作树做，并记入 `TASK.md`「已做决定」。建法：先 fetch；基线默认 `origin/<默认分支>`，主工作树当前分支不是默认分支且领先于它时用 `HEAD`；执行 `git worktree add worktrees/{task} -b {task} <基线>`，分支已存在则 `git worktree add worktrees/{task} {task}`，worktree 已存在就复用；把 `worktrees/` 写进 `.git/info/exclude`；其他规则另有指定位置时以其为准。worktree 路径与基线记入「已做决定」。git 拒绝（如分支已在别处检出）时停下说明原因
- 主工作树里用户已有的改动和当前分支保持原样，不 stash / reset / 切分支。同一任务的 worker 共用这个 worktree，靠改动文件不重叠隔离
- 提交由编排者做，每片一次、收尾一次，只落在任务分支 `{task}`，不 push、不合进默认分支。收尾提交后保留 worktree，清理留给用户
- 只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮；单项做不了就保持未勾，在验证记录写一行原因后继续下一项；「需要用户决策」只停依赖该项的条目，其余条目继续
- 结束时在验证记录逐条列出未勾项与原因，不按 change 汇总；对用户按 user-report 四行说，不报编号

## 验证记录
````

### 脚手架输出

报告 change name、`proposal.md` 路径与仍空缺的项，桥接 stock `openspec-propose`：它会问继续已有 change 还是新建，**选继续**。

## propose 阶段的产出约定

`openspec-propose` 对 driver 产出的 `tasks.md` 按下列骨架组织：准备段建 worktree，实施段按 `wizard/plan.md`「路线图」一片一条（没有路线图时按方案定，通常就是一片），收尾段含回归、回填验收、提交与逐个子 change 的归档条目。

````markdown
## 1. 准备
- [ ] 1.1 给涉及面里角色为必须的修改仓建 worktree `worktrees/{task}`（基线与命令见 Driver 协议），之后改代码、测试、提交都在 worktree 里做

## 2. 实施（一片一条，依赖写在括号里）
- [ ] 2.1 完成子 change `{task}-api`：apply 至全部 checkbox 勾选、validate --strict 通过、提交到任务分支
- [ ] 2.2 完成子 change `{task}-ui`（依赖 2.1）：同 2.1（Web UI 做法见 taskrail `ui-delivery.md`）

## 3. 收尾
- [ ] 3.1 全仓回归与静态检查，命令与结果写入 proposal 验证记录
- [ ] 3.2 回填 proposal 验收标准
- [ ] 3.3 在 worktree 里把收尾改动提交到任务分支 `{task}`（不 push）
- [ ] 3.4 归档前置校核：子 change 全勾且 validate 通过、findings 全有处置（见 execution-discipline「收尾校核」）
- [ ] 3.5 归档全部子 change：逐个 `openspec archive {task}-<slice> --yes`（3.4 过了才跑）
````

收尾段按 [done.md](../../taskrail/references/done.md) 核对；缺证据不勾收尾条目。子 change 的归档是收尾段的普通 checkbox，在 apply 阶段完成。因此 driver 全勾时子 change 已全部 `openspec archive`，对 driver 执行 stock 归档不需要任何递归处理。

### 滚动展开

实施段一次列全，子 change 按依赖分批展开：

- propose 只给依赖已满足的那批切片备齐子 change（在 planning root 对 `{task}-<slice>` 委托 stock `openspec-propose`），其余切片只在实施段占一条。
- 每片做完：编排者在 worktree 只提交这一片的改动，勾掉实施项，过片间检查点（Driver 协议），再展开下一批。已勾的条目和已归档的子 change 不改写。
- 后面切片的细节在展开时按当时的代码起草；没超出路线图那一行，就属于 approve 已批的范围。
- 检查点不停人；动到判据或范围的，按 taskrail 契约「意图变更」处理。
