---
id: task-explore
name: task-explore
description: "探索台账命令集（explore / design / approve / expand / handoff / archive），由 taskrail 委派；出口固定为 handoff。仅在用户点名 task-explore 或被 taskrail 委派时使用；泛指的推进、resume、/goal 一律走 taskrail。"
---

# 任务探索

命令名、路径、代码、状态值与既成术语保持原文。

在任务不明确、周期可能会非常长、或进行复杂问题排查时，不断进行探索、询问、排查等操作。不写实现代码。端到端编排优先走 `taskrail`；本 skill 提供台账与命令细则。

**探索任务** = `tasks/ongoing|archive/.../{task-name}/`。**taskflow 任务** = `{task-name}-driver`。两套账；唯一桥是 `handoff`。交付进度只认 taskflow checkbox。目录与 `phase` 字段约定见 [../taskrail/references/contract.md](../taskrail/references/contract.md)；术语见 [../taskrail/references/glossary.md](../taskrail/references/glossary.md)。

### 命令与 `TASK.md.phase`（强制）

本 skill 的 `new` / `chat` / `save` / `resume` / `reopen` / `expand` / `handoff` 等是**命令**，不是 `TASK.md.phase` 取值。`phase` 只允许契约封闭枚举：`wizard | explore | design | approve | propose | apply | archive | done`。禁止把命令名写入 `phase`。`handoff` 成功后：`status:=handed-off`，`phase:=propose`，并写入 `driver`（见 [references/handoff.md](references/handoff.md)）。

**子任务** = 探索期从父任务拆出的完整探索任务，承接一个可独立推进的方向：目录嵌套为 `ongoing/{parent}/{sub}/`，`TASK.md` 带 `parent:`，生命周期（explore / approve / handoff 等）与顶层任务相同。**父任务** = 拥有 ≥1 个子任务的探索任务；纯伞，只聚合与登记，`status` 恒 `ongoing`，**禁止 `handoff`、不建 driver**，`approve` 仅限范围/非目标/拆分原则。**handed-off** = 已交接 taskflow 的状态：任务留在 `ongoing/`，INDEX 可见、可 `resume`，不是归档。子任务与交付期的 taskflow 子 change 互不隶属。

## Goal 里的确认

处在 goal 里时（判据以 taskrail 确认协议（[../taskrail/references/confirm-protocol.md](../taskrail/references/confirm-protocol.md)）的「触发」节为单一真源，本 skill 不另写一份）,下文和 `references/` 里每一处要向用户确认、选择或询问的决定，都改为走 taskrail 确认协议 的「审阅」：派审规则、核对循环、收敛与停止条件以 taskrail 确认协议 为准，本 skill 不复制第二份。不列选项，不用向用户提问的选择界面。

推荐默认是该处已经写出的默认建议。没有写出默认时，取能让完成判据成立、且不覆盖已有目录、不泄密、不做未点名危险操作的那一条，只审这一条。

审阅收敛则采纳推荐默认并同一轮继续。冻结未决并交接时，审阅收敛即「按推荐冻结并交接」：本轮 `approve` 完立刻 `handoff`。审阅不通过、派不出或没有结论：停，不列选项。taskrail 确认协议 读不到：停并给出安装选项，不改回问用户。

不在 goal 里时，下面的确认规则不变。目标已存在则仍禁止覆盖，不交给审阅放行。

## 命令

| 命令 | 何时 | 写入 |
| --- | --- | --- |
| `new` | 立项；从输入推断任务名 | `tasks/ongoing/{task-name}/` + `INDEX.md` |
| `explore` | 不断探索预期目标 | 术语/ADR 可落任务目录；`TASK.md` 须经确认或 `save` |
| `chat` | **默认命令**：对任务问答 | 默认不写盘 |
| `resume` | 恢复进行中的探索任务 | 任务文档只读；INDEX 漂移可重建 |
| `design` | 针对任务方案设计 | `{taskRoot}/design/` |
| `approve` | **必经**：结构门 + 评审 + 冻结 | `approve/APPROVED.md`；`TASK.md` 决策；INDEX |
| `save` | 保存任务最新进展到任务文档 | 更新 `TASK.md` 与 `INDEX.md` |
| `handoff` | 交接给 taskflow，转入 `handed-off` | driver + 任务状态更新 |
| `archive` | 归档确认关闭的探索任务（含 `handed-off` 后收尾） | `tasks/archive/{yyyy-mm-dd}/{task-name}` |
| `reopen` | 把归档探索任务搬回 ongoing | `ongoing/` + `INDEX.md` |
| `expand` / `split` | 拆子任务（`split` 为 `expand` 别名） | `ongoing/{parent}/{sub}/` + 父 TASK.md + `INDEX.md` |

兼容别名：点名 `decide` / `plan-review` → 走 `approve`（细则见 phase-approve；旧文件为薄引用）。

用户点名 `{{slash:task-explore}}` 且首词命中上表命令名时走该命令；否则走 `chat`。用户要看任务列表或检索任务时，打印 `INDEX.md`（先 Ongoing，需要时再 Archived），不另造命令。

## 加载

进入命令时 **只读该命令详情**，不要预加载其它 phase 或文档骨架。

| 命令 | 进入时读取 |
| --- | --- |
| `explore` | [references/explore-design.md](references/explore-design.md) |
| `design` | [references/explore-design.md](references/explore-design.md)；落盘时再读 [references/templates.md](references/templates.md) |
| `approve` | [references/approve.md](references/approve.md) |
| `decide` / `plan-review` | 兼容别名：同 `approve`，读 [references/approve.md](references/approve.md) |
| `handoff` | [references/handoff.md](references/handoff.md)；委托时再读 `taskflow` |
| `archive` | [references/archive-reopen.md](references/archive-reopen.md) |
| `reopen` | [references/archive-reopen.md](references/archive-reopen.md) |
| `new` / `save` | [references/commands.md](references/commands.md)；写文件时再读 [references/templates.md](references/templates.md) |
| `expand` / `split` | 本文件步骤；写文件时再读 [references/templates.md](references/templates.md) |
| `chat` / `resume` | [references/commands.md](references/commands.md) |

写台账（`INDEX.md` / `TASK.md`）时，除该命令详情外再读 [references/ledger.md](references/ledger.md)；不写台账的命令不读。

## 台账与绑定

布局、`INDEX.md`、绑定与进展提示的细则在 [references/ledger.md](references/ledger.md)，写台账或绑定前先读。不可跳过的要点：

- 没有 `tasks/` 时**必须先获得确认再创建**；同名 `ongoing/{task-name}` 已存在时禁止覆盖，改提议 `resume` 或换名。
- **无 task 上下文时，应提示创建或者恢复（给出 ongoing 列表选择），在确认后进行 new/resume 命令。** 不得猜测任务、不得先聊后补目录。
- 单任务真相只在 `{taskRoot}/TASK.md`；`INDEX.md` 是派生索引，不是第二份真相。产物只写绑定的 `{taskRoot}`，不写 `docs/design/`。

## 命令门禁

各命令的步骤与不可跳过门禁在 [references/commands.md](references/commands.md)（含 `handoff` 交接目标推断、`archive` 五条门禁、`reopen` 四条门禁、`expand` 步骤）；进入命令时读对应小节，再读上表的 phase 详情。approve 后的唯一出口是 `handoff`：方案已冻结且含实施动作、尚未 `handed-off` 时，不进入 `archive`。

## 何时不用

| 情况 | 改用 |
| --- | --- |
| 从未建探索任务，范围清楚、马上实现 | 直接实现，或 `taskflow` / `openspec-propose` |
| 已有探索任务，路径已清、要交付 | 本 skill 的 `handoff`（不要另起无关 `{task}-driver` 名） |
| 只要读代码、不需要任务台账 | `code-explore` |
| 只要一次 grill、不需要 `tasks/` | `grill-with-docs` / `grilling` |
| 已在 OpenSpec change 里交付 | `taskflow` + `openspec-*` |
