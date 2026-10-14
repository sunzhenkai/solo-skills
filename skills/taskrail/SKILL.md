---
id: taskrail
name: taskrail
description: "任务轨道：唯一对外编排入口。绑定 tasks/ 台账，按 wizard → explore(+grill) → design → approve → handoff → propose → apply → archive 推进；内含 human/goal 确认协议、门包与完成门。在用户点名 taskrail、要求端到端推进任务、消息含 /goal、resume 或继续已有任务时使用。"
---

# taskrail：任务轨道

面向用户默认简体中文；命令名、路径、状态值与既成术语保持原文。

把一句目标变成可恢复、可交接的任务推进。本 skill 是**脊柱**：持 `phase` / 完成门 / 档位跳过；确认按本 skill 的 [references/confirm-protocol.md](references/confirm-protocol.md)（原 task-confirm，已并入）；探索与审批材料委托 `task-explore`；交付委托 `taskflow`。

契约真源：[references/contract.md](references/contract.md)；术语表：[references/glossary.md](references/glossary.md)。

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

- `task-explore`（simple/medium 的 explore 仅为 grill；复杂档完整 explore；medium 可轻 design）
- `taskflow`（凡经 taskrail 的交付均必需，含 simple；入口门 `taskflow/scripts/check_handoff.py`）
- `grilling`（有任务目录时的拷问）
- stock `openspec-*`（propose/apply/archive；经 taskflow）
- Web UI 交付另需：playwright + axe-core（`ui_evidence_check`）；Active Instance 由 design 阶段在交付仓内建立，不依赖仓外 UI skill

## 绑定与目录

1. 先读 `tasks/INDEX.md`（无或漂移则按 `ongoing/`/`archive/` 重建，纪律见 task-explore）。
2. 无绑定：请用户 **创建**（`new`）或 **恢复**（`resume`）；确认前不进阶段。例外：本轮已点名对象；或 ongoing 仅一项且用户说「继续」。
3. `new`：无 `tasks/` 须先确认创建。推断 kebab-case `{slug}`，建 `tasks/ongoing/{slug}/TASK.md`（字段见契约），落 `wizard/` 等目录按需。INDEX 追加一行。
4. 同名已存在：禁止覆盖；提议 resume 或换名。
5. `resume`：读 `TASK.md` 元信息与阶段产物；输出 **目标 / phase / 未决 / 建议下一步**；从当前 `phase` 继续，不重出 wizard（除非用户点名重开）。

## 主循环

每轮：读绑定任务的 `phase` → 只加载该阶段细则 → 推荐派出的单位可交宿主 subagent（否则主会话自做；见契约「执行座位」）→ 做完当前闸口 → 更新 `TASK.md`（`updated`、`phase`、指针）→ 按档位决定下一阶段或停。

| phase | 动作 |
|-------|------|
| `wizard` | 读 [references/phase-wizard.md](references/phase-wizard.md)；落 `wizard/plan.md`（含交付类别与适用门包；Web UI 另含 Active Instance 状态）；闸口定稿 |
| `explore` | 委托 task-explore `explore`：simple/medium 仅为 grill；复杂为完整 explore(+grill) |
| `design` | 委托 task-explore `design`；复杂必经；中等可轻量（方案仍落任务目录）；simple 跳过 |
| `approve` | 委托 task-explore `approve`（必经；简单档轻量：只核判据可检查） |
| `propose` | **先** handoff（若 `status` 尚未 `handed-off`；交接节必写「交付类别」「适用门包」，Web UI 另写 Active Instance 根路径与三条 digest），跑 taskflow 入口门 `check_handoff.py` 通过后再委托 taskflow / `openspec-propose`；simple 为单切片 |
| `apply` | 委托 `openspec-apply-change`；进度只认 checkbox。Web UI：页面实现消费 frozen Active Instance，先按代表页 two-pass 方法实现并修订一条主流程代表页，再铺其余表面 |
| `archive` | 交付侧归档 driver；探索侧关闭走 task-explore `archive` |
| `done` | 完成门已过；停止新增工作 |

### 档位跳过

wizard 定稿后写 `tier`，按契约表跳过未列出的阶段（simple 跳过 design，explore 仅为 grill；仍建任务目录、经轻量 approve，且必须 handoff + taskflow）。`grill` / `handoff` / `expand` 是非 phase 动作，见契约。

### expand

design 发现 ≥2 独立方向，或 approve 驳回「范围过大」时，**必须评估一次** expand（task-explore）。父纯伞、子一层；父禁止 handoff。

### approve 出口

`status` 为 `ongoing` 且尚未 `handed-off` 时，approve 完成后的唯一推荐下一步是 `handoff`：叶子任务交接自己；父伞只批量交接已批准子任务。此出口不列 archive、另起任务、继续探索。

查证项与外部依赖写入「可带进实现的未决」，进入 driver 准备段或对应切片前置。未决不把推荐改成 archive，也不另开任务。

同一已冻结方案里的多条实施线，建成该任务 `{slug}-driver` 的 taskflow 子 change。不为实施再 `expand`，不另起无关 driver。

禁止用当轮叙事改写 `criterion`。方案落盘不是完成门。

仅当用户明确说放弃、不实施、或确认关闭且不做实施时，才进入探索侧 archive。已冻结方案含实施动作且尚未 `handed-off` 时，拒绝进入 archive，改走 handoff。与 task-explore archive「不交接而结束」冲突时，以本节为准。

### 复杂档自动推进

`confirm_mode: goal` 且 `tier: complex` 时：闸口一律走确认协议审阅，收敛后同轮续下一阶段；不列选项。证据根落仓外并写入 `evidence_root`。apply 后可选质量环（角色化评审 / 增量复验）沿用 taskflow references 中的交付质量约定，不另开编排入口。

## 完成门

同时满足才把 `status`/`phase` 标 `done`：

1. 完成判据成立（`criterion` 原文）。
2. 交付标准全过（方案写「无」则只看判据）。
3. 相关 checkbox 全勾（含 simple 单切片）。
4. 复杂：质量画像字段齐全；显式降级无 `pending`、无未追认的 `provisional`。
5. 命中交付类别门包时（[references/gate-packs.md](references/gate-packs.md)）：可自动化门全过、运行态证据齐、主观项按参照集或项目标准逐条指认；未覆盖条目均已按「[references/confirm-protocol.md](references/confirm-protocol.md) 未覆盖即降级」登记。
6. 各轮评审的 Blocker / Major 全有 disposition（`fixed` 或 `accepted-recorded` 含理由），从 driver `proposal.md` 验证记录逐条核对。
7. Web UI（按档，见 [gate-packs.md](references/gate-packs.md)「档位调度」）：**medium / complex** 须 digest 与仓库 freeze 一致，且 `ui_evidence_check.py` report exit 0 + design 评审 `--validate-review` exit 0（reviewer ≠ implementer）。**simple**：digest/freeze 仅在有 Active Instance 时核对；`ui_evidence_check` 与 design 评审为 SHOULD——未跑须登记 B 类显式降级，quality floor 自检写入验证记录即可标 `done`。代表页修订记录不单独构成证据；digest 与 Gallery 只证明系统未漂。

完成门**逐条机械核对**：不靠记忆、不用「整体看没问题」替代；任一条缺证据即不标 `done`。

`handed-off`、propose 完、checkbox 全勾但判据不成立 → **不**标 done。

## 硬边界

- 不自动 commit / push / 部署 / 改线上数据。
- 危险与线上退出点以确认协议为准。
- 不在正文复制确认协议的审阅规则；不复制 taskflow 的 Driver 协议。
- 进度：approve 前认 `TASK.md.phase`；其后认 OpenSpec checkbox。
- Worker 派出为推荐选项，非强制；无宿主 subagent 时主会话自做，不因此退出轨道。
