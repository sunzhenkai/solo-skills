# Decision: promote

- patch: evolutions/20261011-reviewer-binding-and-gate-packs
- decision: promote
- date: 2026-10-11
- 用户确认: 优化方案 v4 之 R1 经用户「开工」放行；subagent 复核 PASS。

## 原因

- 证据稳定且可一般化：一次复杂档交付中三处评审全部退化为普通
  subagent 临时 prompt（应命中 role-based-reviewer 的 design 角色清单），
  验收方式被写成对照外部产品，未覆盖条目无人登记——三类根因同源：
  评审执行器、验收基准、覆盖缺口三者缺单一真源。
- eval 全项 pass：15 条新断言红绿验证（生产稿 9 failed + 6 errors，
  候选暂存全仓 388 passed = 前基线 373 + 15）；既有 41 条不破。
- review subagent 七项复核 PASS：diff 仅 4 处预期改动零夹带；
  机制三重封堵静默降级；「未覆盖即降级」正确接 quality-profile 的
  A/B 门；门包表五类字段齐、禁令可判、roles 与 role-based-reviewer
  合法集匹配；跨 skill 无矛盾文本；risk low 属实。
- 复核提出的两处措辞提示已在晋升前修掉：运行态提示改用 reviewer
  实际术语「⚠ 需运行态验证」；门包表去掉尚未定义的「工具不可用
  替代协议」悬空名，改为描述性要求。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 388 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- 未 push、未 dotf 同步；未改 taskrail / taskflow / task-explore
  （它们对本表的引用属各自后续轮次）。
- M8「工具不可用替代协议」作为独立机制留待后续轮次定义，本轮只
  在门包表留下描述性要求。
