---
id: task-explore
name: task-explore
description: "任务探索命令：explore（grill 自问自答）/ design / approve / handoff，把已确认的意图推进到冻结、可交接的方案。taskrail 委派或用户点名 task-explore 时使用。"
---

# 任务探索

把已确认的意图推进到可交接的方案：grill 补细节 → 设计 → 冻结 → 交接。不写实现代码。对用户的话按 [user-report.md](../taskrail/references/user-report.md)；阶段、目录、`phase` 枚举与术语只在 [taskrail 契约](../taskrail/references/contract.md)。

## 命令

| 命令 | 做什么 | 进入时读 |
|------|--------|----------|
| `explore` | grill 自问自答：补细节、边界、约束 | [references/explore-design.md](references/explore-design.md) |
| `design` | 在 `{taskRoot}/design/` 写方案 | [references/explore-design.md](references/explore-design.md)；落盘时读 [references/templates.md](references/templates.md)；要写设计依据 / 对比表时读 [references/design-detail.md](references/design-detail.md)，其中质量底线按 [quality-appendix.md](../taskrail/references/quality-appendix.md) |
| `approve` | 自查 + 闸口 + 冻结 | [references/approve.md](references/approve.md) |
| `handoff` | 交接给 taskflow，转 `handed-off` | [references/handoff.md](references/handoff.md) |

端到端推进、resume、list、/goal 与其余动作（新建、保存进展、归档、reopen）经 taskrail 走，细则：台账 [references/ledger.md](references/ledger.md)，归档 [references/archive-reopen.md](references/archive-reopen.md)。用户点名 `{{slash:task-explore}}` 且首词不是上表命令时，按对话回答任务问题，不自动 grill、不写方案稿。

命令名不是 `phase` 取值；`handoff` 成功后 status 置为 handed-off、phase 置为 propose、写 driver。

## 台账要点

- 单任务真相只在 `{taskRoot}/TASK.md`；`INDEX.md` 是派生索引。所有决定追加到「已做决定」表。
- 产物只写绑定的 `{taskRoot}`。
- 有进展就直接写回 `TASK.md` 与 INDEX，一句话告知（记账不问人）。
- 多会话并发写同一台账时读 [references/ledger-concurrency.md](references/ledger-concurrency.md)。

## goal 里

处在 goal 里（判定见 [confirm-protocol.md](../taskrail/references/confirm-protocol.md)）时，每处要确认的决定改走该协议的「另一个模型审」；收敛就采纳推荐并同轮继续（approve 完立刻 handoff）。真阻塞照样停。

## 可选附录

一个目标里有 ≥2 个可独立推进的方向时读 [references/large-scope.md](references/large-scope.md)；默认单任务。
