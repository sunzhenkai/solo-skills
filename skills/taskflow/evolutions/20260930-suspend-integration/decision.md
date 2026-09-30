# Decision: promote

- patch: evolutions/20260930-suspend-integration
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 2 Proposal（2b 规则全文）于当轮以「确认」批准
  （与 2a 同一句确认，覆盖 2a → 2b 顺序执行）。

## 原因

- 审计 F1/F2/F4/F5 四个卡点同根（无挂起语义），证据稳定；task-goal
  与 task-delivery 侧机制已晋升，本轮补齐族内接入。
- eval 全项 pass：9 条新断言红绿验证；跨 skill 同步锁与模板逐字
  断言全过；全仓 393 passed。
- 改动与 Proposal 一致：SKILL.md 四处（模板一句、降级两条、一轮
  结束一段）、delivery-quality-loop.md 收尾门、acceptance-rubric.md
  评分门，无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 393 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- commit 由本轮统一提交（计划已批准）；未 push、未 dotf 同步。
- task-explore 的降级锁四处加门与 decide↔driver 快照同步（审计 F1/
  F2）属 task-explore 自己的进化轮，未在本轮修改。
