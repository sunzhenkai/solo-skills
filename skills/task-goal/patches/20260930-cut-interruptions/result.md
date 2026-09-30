# Result：降低 goal 模式下的假打断

已 `git apply` 应用。本 skill 6 处正文改动 + 1 处测试同步，语义与 proposal 一致。

## 应用后的正文变化

| 位置 | 改动 |
|---|---|
| 起手节 | 缺完成判据改为「由审阅派出评审者给一条可检查的候选判据，收敛即采纳」，删去「从摸底开始」的全量重做；评审者补不上才回退 |
| 不套模板节 | 详细设计硬墙 `已停。本流程不做详细设计。` 改为交 task-explore 的 `design` 阶段 |
| 审阅节·排队 | 「授权节列名的只读工作」改为显式白名单（只读环境查证、外部原文取证、证据固化；不写交付代码、不改完成判据与步骤） |
| 审阅节·核对 | 新增「跨轮复用」段：P0/P1 语义指纹与结论落 `goal-review-log.md`，已消失条不重派审阅 |
| 授权节 | 复述生效时写清本轮按此执行的动作清单；重申仍停时按 suspension.md 的「最小解除集」排序给下一步 |
| 授权节·无进展轮 | 自动续跑造成的无进展按已停行第 1~2 次处理，不判协议异常；带用户输入或审阅结论的才判异常 |
| 退出点·未点名的危险操作 | 补「上游方案的执行前授权清单里列明的可逆、仓内、非线上动作不算未点名，清单外仍停」 |
| `references/suspension.md` | blocked 摘要同轮写入 state-file 的 `handoff_summary` 并落盘 `blocked: true` |

## 测试

`python3 -m pytest skills -q` → **415 passed, 1 skipped**。

同步改动：`tests/test_task_goal_contract.py` 的 `test_skill_references_suspension` 计数断言 4 → 6（本轮新增两处指向 `references/suspension.md`）。该断言是纯计数，改正文必同步。

## 遗留

- 无。`goal_transition.py` 未改动（A5「自动续跑轮禁写 state」经评估放弃：与网格「已停 × 自动续跑」语义耦合，改它要动状态机契约）。
- 配套改动在 task-wizard / task-explore / task-delivery / taskflow 各自的 `patches/20260930-cut-interruptions/`，与本 patch 同批应用。

## 未验证 / 待观察

以下三条是本次新增的机制，尚无真实运行证据，需在后续 goal 运行中观察：

1. 「缺判据由审阅补齐」的实际收敛率（评审者能否给出可检查的判据）。
2. `goal-review-log.md` 的复用是否真的减少重派（而非形式化落盘）。
3. 无进展轮收窄后，自动续跑期间的状态是否稳定（不再被误判为协议异常）。
