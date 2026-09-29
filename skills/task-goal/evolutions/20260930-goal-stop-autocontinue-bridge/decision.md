# Decision: promote

- patch: evolutions/20260930-goal-stop-autocontinue-bridge
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 于当轮确认；候选 diff 于下一轮以「晋升」确认。

## 原因

- 同类失败两次（2026-09-29 等待被登记成任务；2026-09-30 自动续跑下重申空转四轮），模式稳定。
- eval 全项 pass：基线/候选契约测试同绿（45 passed），空转窗口封顶为 3 次续跑，权限只收紧不放宽。
- 改动与 Proposal 一致：仅「授权」节追加一段，无夹带编辑（diff 为 +2 行）。

## 晋升后验证

- 覆盖生产稿后重跑 `python3 -m pytest skills/task-goal skills/task-wizard -q` → 45 passed。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
