# taskflow：driver 模板与 propose 产出约定

由 [../SKILL.md](../SKILL.md)「脚手架」引用。本文件的 **Driver 协议** 块是切分支、一轮结束等规则的**唯一真源**，其余文件只引用不复述。

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
- 实现进度只认子 change 自己的 `tasks.md`；本文件的 checkbox 只在对应子 change 全勾且 `validate --strict` 通过后才勾
- 切任务分支只针对涉及面里角色为 `必须` 的修改仓，且本身可选；task 所在仓不是修改仓时不切。修改仓干净：先 fetch 默认分支，再从其最新提交 `git switch -c`（分支已存在则 `git switch`）。修改仓 dirty：不动用户的改动，不得 stash / reset / 强制切换；用 `git switch -c` 带着这些改动切到新任务分支（git 只是带过去，文件不变），并一句话说明「你手上有未提交改动，我没动它们，带着切到了任务分支」，记入 `TASK.md`「已做决定」。未提交改动与本任务要改的文件重叠，或 git 拒绝、切错仓时才停下，说明是哪些文件
- 只有「checkbox 全勾」「需要用户决策」「本轮预算耗尽」三种情况允许结束一轮；单项做不了就保持未勾，在验证记录写一行原因后继续下一项；「需要用户决策」只停依赖该项的条目，其余条目继续
- 结束时在验证记录逐条列出未勾项与原因，不按 change 汇总；对用户按 user-report 四行说，不报编号

## 验证记录
````

### 脚手架输出

报告 change name、`proposal.md` 路径与仍空缺的项，桥接 stock `openspec-propose`：它会问继续已有 change 还是新建，**选继续**。

## propose 阶段的产出约定

`openspec-propose` 对 driver 产出的 `tasks.md` 按下列骨架组织：准备段切分支，实施段每个子 change 至少一条，收尾段含回归、回填验收、提交与逐个子 change 的归档条目。

收尾段按 [done.md](../../taskrail/references/done.md) 核对；缺证据不勾收尾条目。

子 change 的 artifacts 在 propose 阶段一次性备齐（拆分粒度本身是提案决策），apply 阶段只做实施，不在实施循环里改 change 语义。

````markdown
## 1. 准备
- [ ] 1.1 （可选）把涉及面里角色为必须的修改仓切到任务分支：干净则从默认分支最新代码切；dirty 则带着用户改动 `git switch -c`（不动改动；说决定见 user-report），与本任务文件重叠时才停

## 2. 实施
- [ ] 2.1 完成子 change `{task}-api`：apply 至全部 checkbox 勾选且 validate --strict 通过
- [ ] 2.2 完成子 change `{task}-ui`：同 2.1（Web UI 做法见 taskrail `ui-delivery.md`）

## 3. 收尾
- [ ] 3.1 全仓回归与静态检查，命令与结果写入 proposal 验证记录
- [ ] 3.2 回填 proposal 验收标准
- [ ] 3.3 提交交付仓改动
- [ ] 3.4 归档前置校核：子 change 全勾且 validate 通过、findings 全有处置（见 execution-discipline「收尾校核」）
- [ ] 3.5 归档全部子 change
````

子 change 的归档是收尾段的普通 checkbox，在 apply 阶段完成。因此 driver 全勾时子 change 已全部 `openspec archive`，对 driver 执行 stock 归档不需要任何递归处理。
