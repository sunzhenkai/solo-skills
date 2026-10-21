---
id: taskrail
name: taskrail
description: "任务轨道：唯一对外编排入口。绑定 tasks/ 台账，按 wizard（意图确认、拆分）→ design(grill) → approve → handoff → propose → apply → archive 推进，大任务拆成切片或子任务滚动推进，按完成清单收口；human/goal 两种确认模式。在用户点名 taskrail、要求端到端推进任务、消息含 /goal、resume 或继续已有任务、要先确认理解对不对、要把大任务拆开分批做时使用。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值保持原文。

把一句目标变成按步骤推进、可恢复、做完符合预期的任务。意图确认、探索、设计、审批与交接都按本 skill 的阶段细则做，交付交给 `taskflow`，对用户的话按 [references/user-report.md](references/user-report.md)。

契约真源（阶段、档位、目录、术语）：[references/contract.md](references/contract.md)。给人看的地图：`docs/task-flow/README.md`。

## 输入

```text
taskrail <一句话目标>
taskrail goal: <一句话目标>
taskrail intent <一句话目标>
taskrail resume [slug]
taskrail list
```

消息含 `/goal`、`goal:` 前缀，或有进行中的 goal 且本条挂了本 skill → `confirm_mode: goal`；resume 沿用 `TASK.md.confirm_mode`，本条带 `/goal` 时改成 goal 并记入「已做决定」；其余 `human`。停在哪、两种模式在闸口上的差别见 [references/confirm-protocol.md](references/confirm-protocol.md)「停点」表。

`taskrail intent`（或用户说「先确认你理解对了没」）只做意图确认：按 [references/intent.md](references/intent.md) 走到纠偏收敛就停。已绑定任务时落 `wizard/intent.md`；没有任务目录就只在对话里给复述，不建任务。

## 依赖

`taskflow`（full 档）、stock `openspec-*`（full 档，经 taskflow）。full 档的执行条件在定档时就查（phase-wizard 第 4 步）；缺哪个就说缺哪个和怎么装，不发明等价命令。stock skill 里停下问人的地方由编排者代答（taskflow「经 taskrail 委托时」）。

## 绑定

细则见 [references/ledger.md](references/ledger.md)；建 `TASK.md` / INDEX 按 [references/templates.md](references/templates.md)；多会话同时写同一台账时读 [references/ledger-concurrency.md](references/ledger-concurrency.md)。

1. 先读 `tasks/INDEX.md`（无或漂移则按 `ongoing/` / `archive/` 重建）。
2. 无绑定：自行判定新建或恢复，一句话说出决定和理由（同一件事就恢复，否则新建）。
3. 新建：无 `tasks/` 就在仓库根建；推断 kebab-case `{slug}`，建 `tasks/ongoing/{slug}/TASK.md`，INDEX 追加一行。同名已存在不覆盖：同一件事就恢复，否则换名。
4. `resume`：读 `TASK.md` 与阶段产物，按 user-report 的 resume 四行汇报，从当前 `phase` 继续；已 `handed-off` 的先按契约「交接后的位置」从 driver 状态推导并回写 `phase`；拆过的任务报做完了几项，从下一个就绪项继续（large-scope.md「续跑」）。`list` 打印 INDEX。

## 主循环

每轮：读 `phase` → 只加载该阶段细则 → 做完当前步 → 更新 `TASK.md`（`updated`、`phase`、指针、「已做决定」）→ 按档位进下一阶段；只在 confirm-protocol「停点」表列出的时机停。

| phase | 动作 |
|-------|------|
| `wizard` | 读 [references/phase-wizard.md](references/phase-wizard.md)：先按 intent.md 落 `wizard/intent.md`，再写 `wizard/plan.md` 与 `criterion` / `tier`，要拆就出路线图，定稿 |
| `design` | 读 [references/design.md](references/design.md)：先 grill 自问自答，再写 `design/`；要对比表 / 设计依据时读 [references/design-detail.md](references/design-detail.md) |
| `approve` | 读 [references/approve.md](references/approve.md)：自查 → 闸口 → 冻结 |
| `propose` | 未 `handed-off` 先按 [references/handoff.md](references/handoff.md) 交接；`check_handoff.py` 通过后委托 taskflow |
| `apply` | full：委托 taskflow / `openspec-apply-change`，进度只认 checkbox，切片按依赖滚动展开；skip：直接实现 + 验证；父任务：按路线图逐项推进子任务 |
| `archive` | 归档 driver（收尾校核已过） |
| `done` | 完成清单已过：发完成通知（[user-report.md](references/user-report.md) 第 8 节），同轮任务归档（[references/archive-reopen.md](references/archive-reopen.md)）；子任务随父任务收尾 |

`handoff` 是动作，不是 `phase` 取值：成功后 status 置为 handed-off、phase 置为 propose、写 driver。用户说关闭任务，或要把归档的任务拉回来，按 archive-reopen.md 做。

**档位**：`skip` = wizard 定稿后直接实现 + 验证；`full` = 全路径。规则见契约「流程」。

**approve 出口**：唯一下一步是 handoff，细则只在契约「approve 出口与交接」。

**命中才读**（均从这里直接打开）：Web UI → [references/ui-delivery.md](references/ui-delivery.md)；多 worker 并行 → [multi-worker.md](../taskflow/references/multi-worker.md)；要拆分，或推进 / 恢复拆过的任务 → [references/large-scope.md](references/large-scope.md)；full 档选型 / 外部集成 → [references/external-precedent.md](references/external-precedent.md)；质量画像 / 降级分级 / 验收打分或门包类别名 → [references/quality-appendix.md](references/quality-appendix.md)。

## 完成

按 [references/done.md](references/done.md) 逐条核对，全过才标 `done`。`handed-off` 或 checkbox 全勾但判据不成立都不算完成。标 `done` 后发完成通知，说清改动在哪、怎么合入，再把任务目录归档。

## 边界

- 提交只落在任务 worktree 的任务分支；不 push、不合进默认分支、不部署、不改线上数据；危险动作按确认协议停。
- 进度：approve 前认 `TASK.md.phase`，之后认 OpenSpec checkbox。
- 没有 worker 能力时主会话自做，不因此退出轨道。
