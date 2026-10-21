---
id: taskflow
name: taskflow
description: "交接后的执行：check_handoff 入口门通过后用 `taskflow-new` 建 `{task}-driver`，拆成 OpenSpec change，委托 stock `openspec-*` propose/apply/archive，进度只认 checkbox。taskrail 委派，或用户点名 taskflow / taskflow-new / 某个 `{task}-driver` 时使用。"
---

# taskflow

面向用户默认简体中文；端到端推进、resume、/goal 走 taskrail。对用户报进度按 [user-report.md](../taskrail/references/user-report.md)，不报 checkbox 计数与字段。

一个任务 = 一个 driver change `{task}-driver`，实现拆成子 change `{task}-<slice>`（同一 planning root；跨 root 时在 driver 涉及面表记录）。**进度只有 checkbox 一种真相**：不另建台账、索引或编号。术语见 [taskrail 契约「术语」](../taskrail/references/contract.md)。

## 阶段路由

| 阶段 | 入口 | 参数 |
|------|------|------|
| 立项 | 本文件「脚手架」（command `taskflow-new`） | 任务描述 |
| 提案 | stock `openspec-propose` | `{task}-driver`；展开切片时为 `{task}-<slice>` |
| 实施 | stock `openspec-apply-change` | `{task}-driver`，逐片 `{task}-<slice>` |
| 归档 | stock `openspec-archive-change` | `{task}-driver`（只归档 driver 自身） |

方案未定时先 stock `openspec-explore`。只提供 `taskflow-new` 一个 command，其余复用 stock skill。

委托 `openspec-*` 时在 driver 的 planning root（主工作树）下执行，并显式给出 change name（`{task}-driver` 或 `{task}-<slice>`）；缺任一项不委托。代码改在 `worktrees/{task}`，两个根的分工见 Driver 协议。`openspec-*` 不可用时说明怎么装（`dotf agents -c` 或 `openspec init --tools agents`，或改用 openspec CLI 直调）。

## 经 taskrail 委托时

stock `openspec-*` 里停下来问人的地方，由编排者按下表代答；停不停只看 taskrail [confirm-protocol.md](../taskrail/references/confirm-protocol.md)「停点」表。单独点名 taskflow 时按 stock 原样交互。

| stock 的行为 | 在轨道里 |
|---|---|
| propose 完停下，等新请求再 apply | approve 放行即授权 propose 与 apply，propose 完接着 apply |
| 同名 change 已存在，问继续还是新建 | 选继续，不问 |
| 实现中不清楚或卡住，暂停并列选项 | 按 Driver 协议：该项保持未勾、验证记录写原因、做下一项；真阻塞按 user-report 第 5 节停 |
| 归档前确认未勾项、问是否同步 spec | 收尾校核过了才归档；子 change 用 `openspec archive {task}-<slice> --yes`（同步 spec），未勾齐不归档 |

## 入口门

创建 `{task}-driver` 或子 change 前，第一步在工作区根跑：

```bash
python3 <taskflow>/scripts/check_handoff.py <workspace-root> <slug>
```

exit 非 0 → 不建 driver，改走 taskrail（approve → handoff），不自己补写 `TASK.md` 绕过。核对项只在脚本里。

用户原话明确要求「不走 taskrail 直接建 driver」时：没有 `TASK.md` 就按 taskrail [templates.md](../taskrail/references/templates.md) 建最小的一份，元信息写 `gate_bypass: "<YYYY-MM-DD> user-confirmed: <用户原话>"` 再跑（脚本以 BYPASS 放行）。理由只照录用户原话；用户没说跳过就走 taskrail。

## 脚手架

`taskflow-new {任务描述}`，入口门通过后三步：

1. 定 `{task}`：有 `TASK.md` 时等于其 slug；否则由描述归纳 kebab-case（描述为空时说明需要任务描述）。
2. `openspec new change {task}-driver --goal "<目标 + criterion 原文 + 方案 / 批准路径；无 TASK.md 时为任务描述原文>"`。
3. `.openspec.yaml` 补 `skip_specs: true`，按 [references/driver-template.md](references/driver-template.md) 写 `proposal.md`（**Driver 协议** 块逐字写入）；`tasks.md` 留给 propose。

## 执行

propose / apply / 收尾前读 [references/execution-discipline.md](references/execution-discipline.md)。默认**串行**：一次做一个子 change；子 change 按依赖滚动展开，每做完一片提交一次、勾掉实施项，过片间检查点再展开下一批（driver-template「滚动展开」）。

- 派给实现者的输入由交接载荷生成：判据原文、交付类别、要产出的证据、指针；不手写省略验收的自由提示词。
- 完成按 [done.md](../taskrail/references/done.md)。
- Web UI → [ui-delivery.md](../taskrail/references/ui-delivery.md)；多 worker 并行 → [references/multi-worker.md](references/multi-worker.md)。

经验积累与 evals 不在运行路径上，见 [references/self-evolution.md](references/self-evolution.md)。
