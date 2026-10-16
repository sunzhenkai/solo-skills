---
id: taskflow
name: taskflow
description: "交接后的执行：check_handoff 入口门通过后用 `taskflow-new` 建 `{task}-driver`，拆成 OpenSpec change，委托 stock `openspec-*` propose/apply/archive，进度只认 checkbox。仅在用户点名 taskflow / taskflow-new / 某个 `{task}-driver`、或被 taskrail 委派时使用；泛指的推进、resume、/goal 一律走 taskrail。"
---

# taskflow

面向用户默认简体中文；对用户报进度按 [user-report.md](../taskrail/references/user-report.md)，不报 checkbox 计数与字段。

一个任务 = 一个 driver change `{task}-driver`，实现拆成子 change `{task}-<slice>`（同一 planning root；跨 root 时在 driver 涉及面表记录）。**进度只有 checkbox 一种真相**：不另建台账、索引或编号。术语见 [taskrail 契约「术语」](../taskrail/references/contract.md)。

## 阶段路由

| 阶段 | 入口 | 参数 |
|------|------|------|
| 立项 | 本文件「脚手架」（command `taskflow-new`） | 任务描述 |
| 提案 | stock `openspec-propose` | `{task}-driver` |
| 实施 | stock `openspec-apply-change` | `{task}-driver` |
| 归档 | stock `openspec-archive-change` | `{task}-driver`（只归档 driver 自身） |

方案未定时先 stock `openspec-explore`。只提供 `taskflow-new` 一个 command，其余复用 stock skill。

委托时必须在 driver 的 planning root 下执行，并显式给出 change name `{task}-driver`；缺任一项不委托。`openspec-*` 不可用时说明怎么装（`dotf agents -c` 或 `openspec init --tools agents`，或改用 openspec CLI 直调）。

## 入口门

创建 `{task}-driver` 或子 change 前，第一步在工作区根跑：

```bash
python3 <taskflow>/scripts/check_handoff.py <workspace-root> <slug>
```

exit 非 0 → 不建 driver，改走 taskrail（approve → handoff），不自己补写 `TASK.md` 绕过。核对项只在脚本里。

用户明确说「不走 taskrail 直接建 driver」时，由用户确认后在 `TASK.md` 元信息写 `gate_bypass: "<YYYY-MM-DD> user-confirmed: <理由>"` 再跑（脚本以 BYPASS 放行）；agent 不自己写这一行。

## 脚手架

`taskflow-new {任务描述}`，入口门通过后三步：

1. 由描述归纳 kebab-case `{task}`（描述为空才问）。
2. `openspec new change {task}-driver --goal "<任务描述原文>"`。
3. `.openspec.yaml` 补 `skip_specs: true`，按 [references/driver-template.md](references/driver-template.md) 写 `proposal.md`（**Driver 协议** 块逐字写入）；`tasks.md` 留给 propose。

## 执行

propose / apply / 收尾前读 [references/execution-discipline.md](references/execution-discipline.md)。默认**串行**：一次做一个子 change，做完勾 checkbox 再下一个。

- 派给实现者的输入由交接载荷生成：判据原文、交付类别、要产出的证据、指针；不手写省略验收的自由提示词。
- 完成按 [done.md](../taskrail/references/done.md)。
- Web UI → [ui-delivery.md](../taskrail/references/ui-delivery.md)；多 worker 并行 → [references/multi-worker.md](references/multi-worker.md)。

经验积累与 evals 不在运行路径上，见 [references/self-evolution.md](references/self-evolution.md)。
