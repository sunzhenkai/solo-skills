# Result：「在 goal 里」的判据改为指向真源

已 `git apply`（与 task-goal / task-delivery 的同 slug patch 同批）。

## 应用后的正文变化

「Goal 里的确认」节第一段的触发条件由自写三条件（`/goal` / 有进行中的 goal / 本任务由 Goal 方案交接且方案里带完成判据）改为「处在 goal 里时（判据以 task-goal 的「触发」节为单一真源，本 skill 不另写一份）」。其余内容不变。

## 测试

全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**。既有 `test_goal_confirmations_go_to_review` 断言的是审阅行为而非触发条件措辞，故全过。

## 遗留

- 无。

## 未验证 / 待观察

去掉第三条（「本任务由 Goal 方案交接且方案里带完成判据」）后，一种场景需要复核：task-goal 把复杂档交接到 task-explore 后，在 handoff 之前的那几轮里，task-explore 是否仍能正确认定自己在 goal 里。按 task-goal 的触发节第三条「被上游 skill 以 goal 模式委派」应能命中，但该条描述的是「被委派进来」而非「交接出去的后续」，措辞上略偏。实际运行中若出现 task-explore 不认 goal 的情况，需要在 task-goal 触发节补一条「由 Goal 方案交接进入的下游阶段」。
