# Decision: promote

- patch: evolutions/20260930-goal-transition-script
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 与候选 diff 均于当轮确认。

## 原因

- 上一轮 goal-state-machine 把状态机落成数据；本轮把「读数据」落成脚本，配套 unittest。证据是 2026-09-30 失败原话「重申没有上限」「自行推导」——计数与状态重建从推理变查表执行。
- eval 全项 pass：候选 83 passed（54 既有 + 24 脚本 + 6 契约 - 1 命名冲突调整）。
- 改动与 Proposal 一致：新增 scripts/goal_transition.py + tests/test_goal_transition.py；SKILL.md 触发节改一句指向脚本；TestGoalTransitionScript 6 个契约断言；无夹带编辑。

## 晋升后验证

- 覆盖生产稿后重跑 `python3 -m pytest skills/task-goal skills/task-wizard -q` → **83 passed**。
- 处理过一次晋升落地问题：evolutions/ 归档目录里的测试副本与生产 tests/ 同名导致 pytest module clash，且归档副本 sys.path 指向不存在的归档 scripts/。处置：归档测试改名为 `goal_transition_test_snapshot.py.txt` 退出 pytest 收集（留作历史快照）；生产稿测试不受影响。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
