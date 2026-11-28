---
id: taskrail
name: taskrail
description: "持久任务轨道：用户要求用 taskrail 创建、确认意图、恢复、解释或列出任务，使用 /goal，或需要跨会话任务台账、父子任务拆分、多阶段或跨项目开发编排时，在 workspace 维护 TASK / PLAN / ROADMAP，按证据路由 references，并统一验证与知识收口。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值保持原文。

把目标变成可恢复、可验证的开发任务。本 skill 负责事实、路由、父子任务和收口；代码实施交给 `taskflow`。契约真源：[references/contract.md](references/contract.md)；用户表达：[references/user-report.md](references/user-report.md)。

## 入口分诊

先判定交付物，再决定是否进入任务轨道：

- 评审、解释或修改 taskrail 自身：只读评审用 `agent-docs`，修改用 `skill-upgrader`；本 skill 只作为讨论对象。
- 显式 taskrail 命令、`/goal`，或需要跨会话任务台账、父子任务拆分、大型项目 / 架构调整 / 重大跨模块重构，以及多阶段或跨项目开发编排：按下文输入进入任务轨道。
- 普通问答、只读分析或一次性改动，且没有上两项信号：直接回答、实施或使用对应领域 skill。

只有第二项绑定或恢复 TASK。入口误加载时完成分诊即退出，不写 TASK / INDEX，不建 worktree。

## 输入

```text
taskrail <一句话目标>
taskrail goal: <一句话目标>
taskrail intent <一句话目标>
taskrail resume [task-id]
taskrail explain [task-id]
taskrail list
```

`/goal`、`goal:` 或沿用的 `confirm_mode: goal` 只改变确认方式，不改变路由。停点统一见 [references/confirm-protocol.md](references/confirm-protocol.md)（其中**大型项目、重大改动或架构调整**无论 `human` 还是 `goal`，动工前均先人话对齐方案并等明确放行）。`intent` 只做意图确认，按 [references/intent.md](references/intent.md) 执行；没有任务目录就只在对话里给复述，不建执行分支。`explain` 只读说明当前环节、跳过理由、子任务和下一动作。

## 绑定与恢复

按 [references/ledger.md](references/ledger.md) 确定 workspace、新建或恢复任务。热状态与 INDEX 更新使用 `python3 <taskrail>/scripts/task_state.py <command> <workspace> ...`。

resume 先跑 `reconcile`，只读 `TASK.md`、当前 `PLAN.md` / `ROADMAP.md` 就绪行、`context/current.md` 和当前 reference；不默认加载 history、兄弟子任务或全部 OpenSpec changes。driver 归档、目录位置或 checkbox 全勾都不能单独推出 done。

## 动态主循环

每轮六步：1. 读热状态核对目标与 `criterion`；2. 按 [references/router.md](references/router.md) 判定当前 reference；3. 只加载命中的 reference；4. 完成一个可检查动作并留证据；5. 用 `task_state.py` 更新 TASK / INDEX，路由原因记 `history.md`、决定记 `decisions.md`；6. 重新路由，命中 [confirm-protocol.md](references/confirm-protocol.md) 停点时等待明确回复，其余按认知增量同步并继续。

路由型 references（命中才读）：

| reference | 用途 |
|---|---|
| [plan.md](references/plan.md) | 当前最小计划与验证策略 |
| [explore.md](references/explore.md) | 代码入口、依赖、外部参照与影响面 |
| [diagnose.md](references/diagnose.md) | 红灯复现、基线与根因证据 |
| [grill.md](references/grill.md) | 关键取舍、前沿拉齐与未知 |
| [design.md](references/design.md) | 接缝、契约、架构、细则与回滚 |
| [approve.md](references/approve.md) | 按需人话对齐与批准 |
| [decompose.md](references/decompose.md) | 垂直切片、`subtasks/` 与集成项 |
| [review.md](references/review.md) | 按需独立评审分流与 findings 处置 |
| [verify.md](references/verify.md) | 判据、回归、集成与证据 |
| [close.md](references/close.md) | SUMMARY、知识提升、归档与重开 |

`execute` 委托 `taskflow`；OpenSpec 先按 [handoff.md](references/handoff.md) 跑 `check_handoff.py`，direct 不走该门。Web UI 与质量包分别按 [ui-delivery.md](references/ui-delivery.md)、[quality-appendix.md](references/quality-appendix.md) 在环节内加载，不另占 `current_ref`。

## 固定不变量

- 代码修改默认由 `taskflow` 在 `<workspace>/worktrees/` 的真 git worktree 实施，只提交到任务分支，不 push、不合默认分支、不部署、不改线上数据。
- `decompose` 自动建 pending 子任务并按依赖推进；多 worker 子任务派发前原子 `claim`，父任务必做集成与总判据验证。
- `context/current.md` 区分可准确提问的 `U-n` 与模糊区 `F-n`，每轮最多解一个就绪 `U-n`（见 [references/contract.md](references/contract.md)）。
- `status: done` 仅在 [references/done.md](references/done.md) 全过、`SUMMARY.md` 实质非空且所有直接子任务 done 后写入；危险动作按确认协议停，同仓同任务写操作串行。
