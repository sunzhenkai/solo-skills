# Decision: promote

- patch: evolutions/20260930-hypothesis-streak
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 4 规则列于五项 Phase 计划（验证连败按假设计数），
  当轮以「继续」确认执行；risk: low。

## 原因

- 与已被两个真实 case 证实并修复的审阅连败缺陷同构（按外部条件
  计数 vs 按问题身份计数），是族内最后一处该模式。
- eval 全项 pass：4 条新断言红绿验证；diff 仅一条定义；全仓
  402 passed。
- 改动与 Proposal 一致：仅退出点定义一条 + 契约测试。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 402 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- commit 由本轮统一提交（计划已批准）；未 push、未 dotf 同步。
- task-delivery 的两处副本（SKILL.md 硬边界、loop-protocol Stop
  conditions）同步属 task-delivery 下一轮（4b）。
