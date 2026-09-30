# Decision: promote

- patch: evolutions/20260930-hypothesis-sync
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 4 计划（含族内同步）当轮以「继续」确认执行；
  risk: low 纯同步。

## 原因

- task-goal 侧定义已晋升，两处副本必须同口径；同步锁测试模式
  沿用仓内既有先例。
- eval 全项 pass；diff 两行；全仓 405 passed。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 405 passed, 1 skipped。

## 未做

- commit 由本轮统一提交；未 push、未 dotf 同步。
