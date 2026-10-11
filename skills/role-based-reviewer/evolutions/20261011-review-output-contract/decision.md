# Decision: promote

- patch: evolutions/20261011-review-output-contract
- decision: promote
- date: 2026-10-11
- 用户确认: 优化方案 v4 之 R5 经用户「继续」放行；subagent 复核 PASS。

## 原因

- 三类失效同源（F8 证据无状态绑定 / F6 findings 无编号与处置位 /
  F7 未覆盖项无降级语义）：评审报告是交付收敛链的证据源，却
  没有「状态绑定 + 可引用编号 + 未覆盖降级建议」三条证据契约，
  调用方拿到的是散文式结论而非可登记的台账输入。
- eval 全项 pass：14 条新断言红绿验证（生产稿 10 failed / 4 passed，
  候选暂存全仓 450 passed = 前基线 436 + 14）；既有 8 条不破。
- review subagent 六项复核 PASS：diff 零夹带（三道门禁 / 角色枚举 /
  RoleBrief / 既有字段约定逐字未改）、无过拟合、与 R1/R2 术语 token
  级一致且分工无越界（本 skill 不代判收敛）、机制收紧而非放宽、
  红绿与全仓数字逐数自洽、risk low 属实。
- 复核提出的两处建议已处置：门 1 「三样齐备」与缺项容忍并存导致
  的措辞张力已收敛（mode/roles 为硬条件，边界为「应尽量齐备 +
  缺项义务」）；契约测试随本轮一并提交（与前四轮做法一致）。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 450 passed, 1 skipped；
  两份生产稿与候选 diff 全等。

## 未做（按 skill-evolver 边界）

- 未 push、未 dotf 同步。
- 优化方案 v4 的 R1–R5 已完成；产品侧（web 代码）按用户要求不动。
