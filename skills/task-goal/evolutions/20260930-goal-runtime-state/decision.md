# Decision: promote

- patch: evolutions/20260930-goal-runtime-state
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 与候选 diff 均于当轮确认。

## 原因

- 状态机三层架构（规则 + 查表 + 计数器）的最后一块。证据链：2026-09-30 失败「重申没有上限」「自行推导」 + 2026-09-29 同族失败 + 前两轮已落地的网格与脚本——state-file 是脚本入参的明证。
- eval 全项 pass：基线 83，候选 91（新增 35 个脚本用例 + 3 个契约断言 - 命名调整）。
- 端到端模拟：4 轮 auto-continue 走 state-file，第 3 轮标 blocked=true，第 4 轮保持 blocked 不再空转。
- 改动与 Proposal 一致：脚本改扩建 + references/state-file.md + SKILL.md 触发节一句改写 + 测试扩展；无夹带编辑。

## 晋升后验证

- 覆盖生产稿后重跑 `python3 -m pytest skills/task-goal skills/task-wizard -q` → **91 passed**。
- 沿用上一轮处置：evolutions/ 归档测试副本改名为 `goal_transition_test_snapshot.py.txt` 退出 pytest 收集，避免与生产 tests/test_goal_transition.py module clash。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
