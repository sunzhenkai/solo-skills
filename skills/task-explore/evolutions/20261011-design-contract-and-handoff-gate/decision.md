# Decision: promote

- patch: evolutions/20261011-design-contract-and-handoff-gate
- decision: promote
- date: 2026-10-11
- 用户确认: 优化方案 v4 之 R4 经用户「继续」放行；subagent 复核 PASS。

## 原因

- 两类失效同源（F4 契约未冻结即并行 / F8 证据无契约 的探索侧表现）：
  design 产物清单不含共享面契约与证据计划，handoff 门禁不核对契约
  是否已在交付仓，契约只能由生产段现造。
- eval 全项 pass：10 条新断言红绿验证（生产稿 8 failed / 2 passed，
  候选暂存全仓 436 passed = 前基线 426 + 10）；既有 54 条与族内
  跨 skill 契约（含相对链接可达）不破。
- review subagent 六项复核 PASS：diff 零夹带、无过拟合、跨 skill
  链接与术语一致（门包表 / 执行段脊梁 / taskrail 载荷表三方闭合）、
  机制衔接无矛盾（指针产出 → 交接 → 派发前必须存在）、红绿数字
  独立复跑自洽、risk low 属实。
- 复核提出的轻微观察已处置：门禁第 5 条的「目标仓」就地消歧为
  「taskflow 涉及面表中角色为 `必须` 的修改仓」。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 436 passed, 1 skipped；
  三份生产稿与候选逐文件 diff 一致。

## 未做（按 skill-evolver 边界）

- 未 push、未 dotf 同步。
- R5（role-based-reviewer 输出契约）为下一轮。
