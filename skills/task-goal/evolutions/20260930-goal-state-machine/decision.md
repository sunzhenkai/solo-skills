# Decision: promote

- patch: evolutions/20260930-goal-state-machine
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 与候选 diff 均于当轮确认。

## 原因

- 同类失败一族（2026-09-29 等待被登记成任务；2026-09-30 自动续跑重申空转四轮）已各打一次补丁，模式稳定——散文补丁逐个补格子而不枚举格子。
- eval 全项 pass：基线 45 passed，候选 54 passed（新增 8 个 TestStateMachine 断言 + 1 个 references 存在断言更新）。
- 改动与 Proposal 一致：新增 references/state-machine.md（事件封闭枚举 + 迁移网格 + 无进展轮兜底）；SKILL.md 四处接入句 + 「无进展轮」兜底段 + autocontinue 段落末尾补「blocked 是已停的交接形态」；无夹带编辑。

## 晋升后验证

- 覆盖生产稿后重跑 `python3 -m pytest skills/task-goal skills/task-wizard -q` → **54 passed**。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
