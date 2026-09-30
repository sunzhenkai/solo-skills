# Decision: promote

- patch: evolutions/20260930-review-queue
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 3 规则概要列于五项 Phase 计划（审阅基建降级阶梯），
  当轮以「继续」确认执行；proposal.yaml 载明 risk: medium。

## 原因

- 真实 case 实证异源端点耗尽形态；资源等待与授权等待的类别错误
  是稳定模式（审计模式 3 的 goal 层实例）。
- eval 全项 pass：5 条新断言红绿验证；既有审阅纪律与三 Strike
  语义未动；全仓 398 passed。
- 改动与 Proposal 一致：SKILL.md 三处、state-machine.md 一格、
  suspension.md 白名单一句，无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 398 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- commit 由本轮统一提交（计划已批准）；未 push、未 dotf 同步。
- task-delivery 异源门 (a)(b)(c) 的实现评审阶梯（排队语义对称接入）
  属 task-delivery 后续进化轮；本轮只改 task-goal 的方案审阅路径。
