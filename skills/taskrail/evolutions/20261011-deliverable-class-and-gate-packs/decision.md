# Decision: promote

- patch: evolutions/20261011-deliverable-class-and-gate-packs
- decision: promote
- date: 2026-10-11
- 用户确认: 优化方案 v4 之 R3 经用户「继续」放行；subagent 复核 PASS。

## 原因

- 三类失效同源（F2 基准错置 / F3 门路由缺失 / F6+F7 完成门不机械）：
  wizard 不判交付类别与基准物，载荷无从携带门包，完成门无法机械核对。
- eval 全项 pass：16 条新断言红绿验证（生产稿 11 failed / 5 passed，
  候选暂存全仓 426 passed = 前基线 410 + 16）；既有 27 条与族内跨
  skill 契约（载荷归属、真源、删除 id、相对链接可达、phase 枚举）不破。
- review subagent 六项复核 PASS：diff 零夹带（被替换行均有直接替换、
  无净删除）、无过拟合、跨 skill 相对链接与术语一致、与 taskflow
  收尾机械校核分工清晰无口径分裂、红绿数字独立复跑自洽、risk low 属实。
- 复核提出的术语对齐已落实：完成门第 5 条与模板字段改用上游规范词
  「未覆盖即降级」并回指 task-confirm。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 426 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- 未 push、未 dotf 同步。
- task-explore 侧的共享面冻结产物与 handoff 前置校核属 R4 轮次。
