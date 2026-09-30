# Decision: promote

- patch: evolutions/20260930-partial-suspend
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 2 Proposal（2a 规则全文）于当轮以「确认」批准。

## 原因

- 三个真实卡点形态（全局停摆、两轮封顶、真人门/预算无形态）证据
  稳定；task-goal 侧配套机制（suspension、A/B、连败计数）已晋升，
  本轮是接入侧对齐。
- eval 全项 pass：13 条新契约断言红绿验证；全仓 384 passed；安全
  边界未放宽。
- 改动与 Proposal 一致：SKILL.md 两处（真人门+硬边界）、
  loop-protocol.md 六处（预算语义、冻结门、追认点、Stage 9、完成门、
  Stop conditions），新增 tests/，无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 384 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- commit 由本轮统一提交（计划已批准）；未 push、未 dotf 同步。
- 2b（taskflow 挂起接入 + pending 期合法勾法）属下一轮。
