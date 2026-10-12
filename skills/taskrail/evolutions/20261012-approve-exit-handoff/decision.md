# Decision: promote

- patch: evolutions/20261012-approve-exit-handoff
- decision: promote
- date: 2026-10-12
- 用户确认 Proposal 与候选 diff。

## 原因

- eval pass：覆盖前基线 495 passed；覆盖后 `python3 -m pytest skills -q` → 497 passed, 2 skipped。
- 同模式的阶段细则在 task-explore 同 slug 一并晋升，避免只改脊柱时「只加载阶段细则」仍走旧出口。
- diff 与 Proposal 一致：approve 出口、契约、两侧阶段细则与各 1 条断言。未改档位、父任务纯伞、子任务一层。

## 晋升后

- 未 commit、未 push、未做安装同步。
