---
id: taskrail
name: taskrail
description: "任务轨道：唯一编排入口。绑定 tasks/ 台账，按 wizard → explore(+grill) → design → approve → propose → apply → archive 推进；支持 human 确认与 goal 自动确认。在用户点名 taskrail、要求端到端任务推进、/goal 任务编排、或 resume 已有任务时使用。只要探索台账可点名 task-explore；只要 OpenSpec driver 可点名 taskflow。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值与既成术语保持原文。

把一句目标变成可恢复、可交接的任务推进。本 skill 是**脊柱**：持 `phase` / 完成门 / 档位跳过；确认委托 `task-confirm`；探索与审批材料委托 `task-explore`；交付委托 `taskflow`。

契约真源：[references/contract.md](references/contract.md)。

## 输入

```text
taskrail <一句话目标>
taskrail goal: <一句话目标>
taskrail resume [slug]
taskrail list
```

- 消息含 `/goal`，或当前有进行中的 goal 且本条挂了本 skill → `confirm_mode: goal`。
- 显式 `goal:` 前缀同上。
- 未命中 → `confirm_mode: human`。

## 依赖

执行前确认可读；缺任一项停下报告安装选项：

- `task-confirm`
- `task-explore`（simple/medium 的 explore 仅为 grill；复杂档完整 explore；medium 可轻 design）
- `taskflow`（凡经 taskrail 的交付均必需，含 simple）
- `grilling`（有任务目录时的拷问）
- stock `openspec-*`（propose/apply/archive；经 taskflow）

## 绑定与目录

1. 先读 `tasks/INDEX.md`（无或漂移则按 `ongoing/`/`archive/` 重建，纪律见 task-explore）。
2. 无绑定：请用户 **创建**（`new`）或 **恢复**（`resume`）；确认前不进阶段。例外：本轮已点名对象；或 ongoing 仅一项且用户说「继续」。
3. `new`：无 `tasks/` 须先确认创建。推断 kebab-case `{slug}`，建 `tasks/ongoing/{slug}/TASK.md`（字段见契约），落 `wizard/` 等目录按需。INDEX 追加一行。
4. 同名已存在：禁止覆盖；提议 resume 或换名。
5. `resume`：读 `TASK.md` 元信息与阶段产物；输出 **目标 / phase / 未决 / 建议下一步**；从当前 `phase` 继续，不重出 wizard（除非用户点名重开）。

## 主循环

每轮：读绑定任务的 `phase` → 只加载该阶段细则 → 做完当前闸口 → 更新 `TASK.md`（`updated`、`phase`、指针）→ 按档位决定下一阶段或停。

| phase | 动作 |
|-------|------|
| `wizard` | 读 [references/phase-wizard.md](references/phase-wizard.md)；落 `wizard/plan.md`；闸口定稿 |
| `explore` | 委托 task-explore `explore`：simple/medium 仅为 grill；复杂为完整 explore(+grill) |
| `design` | 委托 task-explore `design`；复杂必经；中等可轻量（方案仍落任务目录）；simple 跳过 |
| `approve` | 委托 task-explore `approve`（必经；简单档轻量：只核判据可检查） |
| `propose` | **先** handoff（若 `status` 尚未 `handed-off`），再委托 taskflow / `openspec-propose`；simple 为单切片 |
| `apply` | 委托 `openspec-apply-change`；进度只认 checkbox |
| `archive` | 交付侧归档 driver；探索侧关闭走 task-explore `archive` |
| `done` | 完成门已过；停止新增工作 |

### 档位跳过

wizard 定稿后写 `tier`，按契约表跳过未列出的阶段（simple 跳过 design，explore 仅为 grill；仍建任务目录、经轻量 approve，且必须 handoff + taskflow）。`grill` / `handoff` / `expand` 是非 phase 动作，见契约。

### expand

design 发现 ≥2 独立方向，或 approve 驳回「范围过大」时，**必须评估一次** expand（task-explore）。父纯伞、子一层；父禁止 handoff。

### 复杂档自动推进

`confirm_mode: goal` 且 `tier: complex` 时：闸口一律走 task-confirm 审阅，收敛后同轮续下一阶段；不列选项。证据根落仓外并写入 `evidence_root`。apply 后可选质量环（角色化评审 / 增量复验）沿用 taskflow references 中的交付质量约定，不另开编排入口。

## 完成门

同时满足才把 `status`/`phase` 标 `done`：

1. 完成判据成立（`criterion` 原文）。
2. 交付标准全过（方案写「无」则只看判据）。
3. 相关 checkbox 全勾（含 simple 单切片）。
4. 复杂：质量画像字段齐全；显式降级无 `pending`、无未追认的 `provisional`。

`handed-off`、propose 完、checkbox 全勾但判据不成立 → **不**标 done。

## 硬边界

- 不自动 commit / push / 部署 / 改线上数据。
- 危险与线上退出点以 `task-confirm` 为准。
- 不复制 task-confirm 的审阅规则；不复制 taskflow 的 Driver 协议。
- 进度：approve 前认 `TASK.md.phase`；其后认 OpenSpec checkbox。
