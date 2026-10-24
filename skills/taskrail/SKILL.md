---
id: taskrail
name: taskrail
description: "任务轨道：在 workspace 中维护任务与父子任务，按证据动态进入、跳过或重入 explore / diagnose / grill / design / approve / decompose 等 references；direct 或 OpenSpec 均可执行，统一验证与知识收口。用于端到端代码开发、跨项目需求、/goal、resume、自动拆任务或只确认意图。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值保持原文。

把目标变成可恢复、可验证的开发任务。本 skill 负责事实、路由、父子任务和收口；代码实施交给 `taskflow`。契约真源：[references/contract.md](references/contract.md)；用户表达：[references/user-report.md](references/user-report.md)。

## 输入

```text
taskrail <一句话目标>
taskrail goal: <一句话目标>
taskrail intent <一句话目标>
taskrail resume [task-id]
taskrail explain [task-id]
taskrail list
```

`/goal`、`goal:` 或沿用的 `confirm_mode: goal` 只改变确认方式，不改变路由。停点见 [references/confirm-protocol.md](references/confirm-protocol.md)。`intent` 只做意图确认，按 [references/intent.md](references/intent.md) 执行；没有任务目录就只在对话里给复述，不建执行分支。`explain` 只读说明当前环节、跳过理由、子任务和下一动作。

## 绑定与恢复

按 [references/ledger.md](references/ledger.md) 确定 workspace、新建或恢复任务。台账热状态和 INDEX 更新使用：

```bash
python3 <taskrail>/scripts/task_state.py <command> <workspace> ...
```

resume 先跑 `reconcile`，再读 `TASK.md`、当前 `PLAN.md` / `ROADMAP.md` 就绪行、`context/current.md` 和当前 reference；不默认读 history、全部子任务或全部 OpenSpec changes。driver 归档、目录位置或 checkbox 全勾都不能单独推出 done。

## 动态主循环

每轮只做以下六步：

1. 读 TASK 热状态，核对目标和 `criterion`。
2. 按 [references/router.md](references/router.md) 检查当前 reference 是否仍适用。
3. 只加载命中的 reference；其统一结构见 [references/ref-contract.md](references/ref-contract.md)。
4. 完成一个可检查动作，产生产物或证据。
5. 用热状态脚本更新 TASK / INDEX，把路由原因追加到 `history.md`，决定写入 `decisions.md`。
6. 重新路由；只在确认协议规定的停点或真阻塞时停。

路由型 references（从这里直接打开，命中才读）：

| reference | 用途 |
|---|---|
| [plan.md](references/plan.md) | 当前最小计划与验证策略 |
| [explore.md](references/explore.md) | 代码入口、依赖、约束与影响面 |
| [diagnose.md](references/diagnose.md) | 复现、基线与根因证据 |
| [grill.md](references/grill.md) | 关键取舍、冲突与未知 |
| [design.md](references/design.md) | 契约、架构、兼容性与迁移 |
| [approve.md](references/approve.md) | 必要的人或模型批准 |
| [decompose.md](references/decompose.md) | 自动规划切片、`subtasks/` 与集成项 |
| [verify.md](references/verify.md) | 判据、回归、集成与证据 |
| [close.md](references/close.md) | SUMMARY、知识提升与归档；归档 / 重开见 [archive-reopen.md](references/archive-reopen.md) |

`execute` 委托 `taskflow`；OpenSpec 先按 [handoff.md](references/handoff.md) 运行 `check_handoff.py`，direct 不走该门。`review` 按需走角色化只读评审。Web UI、外部参照、质量包分别按 [ui-delivery.md](references/ui-delivery.md)、[external-precedent.md](references/external-precedent.md)、[quality-appendix.md](references/quality-appendix.md) 在环节内加载，不另占 `current_ref`。

## 固定不变量

- 代码任务默认由 taskflow 在 git worktree 实施；direct 与 OpenSpec 仅差执行编排，不差隔离。
- workspace 统一持 `tasks/`、`openspec/`、`worktrees/`；各修改仓可位于 workspace 内外。
- 提交只落在任务 worktree 的任务分支；不 push、不合默认分支、不部署、不改线上数据。
- `decompose` 自动建 pending 子任务并推进就绪项；父任务必须做集成与总判据验证。
- `status: done` 只能由 [references/done.md](references/done.md) 全过且 `SUMMARY.md` 存在后写入；父任务的子任务必须全部 done。
- 危险动作按确认协议停；同仓同任务写操作串行；无 worker 能力时主会话自做，不退出轨道。
