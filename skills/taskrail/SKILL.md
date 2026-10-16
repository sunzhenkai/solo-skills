---
id: taskrail
name: taskrail
description: "任务轨道：唯一对外编排入口。绑定 tasks/ 台账，按 wizard → explore(grill) → design → approve → handoff → propose → apply → archive 推进，按完成清单收口；human/goal 两种确认模式。在用户点名 taskrail、要求端到端推进任务、消息含 /goal、resume 或继续已有任务时使用。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值保持原文。

把一句目标变成按步骤推进、可恢复、做完符合预期的任务。本 skill 只管**步骤与完成**：意图交给 `task-intent`，探索与审批交给 `task-explore`，交付交给 `taskflow`，对用户的话按 [references/user-report.md](references/user-report.md)。

契约真源（阶段、档位、目录、术语）：[references/contract.md](references/contract.md)。给人看的地图：`docs/task-flow/README.md`。

## 输入

```text
taskrail <一句话目标>
taskrail goal: <一句话目标>
taskrail resume [slug]
taskrail list
```

消息含 `/goal`、`goal:` 前缀，或有进行中的 goal 且本条挂了本 skill → `confirm_mode: goal`；否则 `human`。两种模式的差别只在 [references/confirm-protocol.md](references/confirm-protocol.md)。

## 依赖

`task-intent`、`task-explore`、`taskflow`（full 档）、`grilling`、stock `openspec-*`（full 档，经 taskflow）。缺哪个就说缺哪个和怎么装，不发明等价命令。

## 绑定

1. 先读 `tasks/INDEX.md`（无或漂移则按 `ongoing/` / `archive/` 重建）。
2. 无绑定：自行判定新建或恢复，一句话说出决定和理由（同一件事就恢复，否则新建）。
3. 新建：无 `tasks/` 就在仓库根建；推断 kebab-case `{slug}`，建 `tasks/ongoing/{slug}/TASK.md`，INDEX 追加一行。同名已存在不覆盖：同一件事就恢复，否则换名。
4. `resume`：读 `TASK.md` 与阶段产物，按 user-report 的 resume 四行汇报，从当前 `phase` 继续；`list` 打印 INDEX。

## 主循环

每轮：读 `phase` → 只加载该阶段细则 → 做完当前步 → 更新 `TASK.md`（`updated`、`phase`、指针、「已做决定」）→ 按档位进下一阶段或停。

| phase | 动作 |
|-------|------|
| `wizard` | 读 [references/phase-wizard.md](references/phase-wizard.md)：先委托 `task-intent` 落 `wizard/intent.md`，再写 `wizard/plan.md` 与 `criterion` / `tier`，定稿 |
| `explore` | 委托 task-explore `explore`（grill 自问自答，只追细节） |
| `design` | 委托 task-explore `design` |
| `approve` | 委托 task-explore `approve` |
| `propose` | 未 `handed-off` 先走 task-explore `handoff`；`check_handoff.py` 通过后委托 taskflow |
| `apply` | full：委托 taskflow / `openspec-apply-change`，进度只认 checkbox；skip：直接实现 + 验证 |
| `archive` | 交付侧归档 driver；探索侧关闭走 task-explore `archive` |
| `done` | 完成清单已过，停止新增工作 |

**档位**：`skip` = wizard 定稿后直接实现 + 验证；`full` = 全路径。规则见契约「流程」。

**approve 出口**：唯一下一步是 handoff，细则只在契约「approve 出口与交接」。

**命中才读**（均从这里直接打开）：Web UI → [references/ui-delivery.md](references/ui-delivery.md)；多 worker 并行 → [multi-worker.md](../taskflow/references/multi-worker.md)；一个目标里有多个独立方向 → [large-scope.md](../task-explore/references/large-scope.md)；full 档选型 / 外部集成 → [references/external-precedent.md](references/external-precedent.md)；质量画像 / 降级分级 / 验收打分或门包类别名 → [references/quality-appendix.md](references/quality-appendix.md)；交接步骤 → [handoff.md](../task-explore/references/handoff.md)。

## 完成

按 [references/done.md](references/done.md) 逐条核对，全过才标 `done`。`handed-off` 或 checkbox 全勾但判据不成立都不算完成。

## 边界

- 不自动 commit / push / 部署 / 改线上数据；危险动作按确认协议停。
- 进度：approve 前认 `TASK.md.phase`，之后认 OpenSpec checkbox。
- 没有 worker 能力时主会话自做，不因此退出轨道。
