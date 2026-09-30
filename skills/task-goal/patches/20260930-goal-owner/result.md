# Result：goal 生命周期的 owner 条款

已 `git apply`（与 task-delivery / task-explore 的同 slug patch 同批）。

## 应用后的正文变化

| 位置 | 改动 |
|---|---|
| 触发节 | 声明**本节是「在 goal 里」的单一真源**，其他 skill 不另写判据 |
| 触发节 | state-file 路径由进入 side 给出：委派方在 `goal-state-file:` 指定；独立 `/goal` 进入默认 `<task 运行目录>/goal-state.yaml`，无任务运行目录则落 `<evidence_root>/goal-state.yaml` |
| 写完之后·复杂档 | **按来路分流**：由 task-delivery 的 goal 模式委派进来时，执行循环归 delivery 的 Stage 1–12，本协议只持状态与审阅，路由不换成 task-explore；其余情况仍走 task-explore |
| `references/state-file.md` | 落点节补三行：委派方指定 / 独立进入的默认 / `goal-state-file:` 戳可覆盖 |

## 测试

全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**。本批未新增断言——现有断言未覆盖这些措辞，属陈述性条款。

## 遗留

- 无。

## 未验证 / 待观察

**「每轮收口回报」的格式未定义**（只说带 `goal-event:` 戳优先，无戳按 task-goal 的事件推断顺序）。这依赖 goal 系统是否支持盖戳：

1. 支持盖戳 → 完全无歧义。
2. 不支持 → delivery 的收口报告内容要能被推断顺序第 6 条接住（「上次处于写完之后且 checkbox 有推进 → 步骤推进」）。若实际运行中推断频繁落空（落进「无进展轮」），需要在 `state-file.md` 的推断顺序里补一条 delivery 收口专用分支。

另需观察：复杂档按来路分流后，「goal 直接进入但用户其实想走 delivery 自动闭环」的场景会被路由到 task-explore，与预期不符。当前靠「用户点名 delivery」区分，无自动判据。
