# Decision: promote

- patch: evolutions/20261011-execution-spine
- decision: promote
- date: 2026-10-11
- 用户确认: 优化方案 v4 之 R2 经用户「继续」放行；subagent 复核 PASS。

## 原因

- 五类失效同源（F4 契约未冻结即并行 / F5 同类失败不升级 / F6 评审
  集中收尾 / F8 证据无契约 / F9 归档无机械校核），且都属「执行段缺
  可机械核对的脊梁」。
- eval 全项 pass：22 条新断言红绿验证（生产稿 19 failed / 3 passed，
  候选暂存全仓 410 passed = 前基线 388 + 22）；既有 40 条锁测试
  （Driver 协议逐字、Self-evolution 四 skill 逐字一致、模板）不破。
- review subagent 六项复核 PASS：diff 零夹带、无过拟合、跨 skill
  相对路径与术语一致、机制不与既有节重复冲突、红绿数字独立复跑
  自洽、risk low 属实。
- 复核提出的三处措辞已修：旗舰适用口径与 quality-loop 对齐（并入
  「首次实现或大改」）、增量评审批次改为「实施段开始前声明」、
  rubric 审阅边界列举回指 task-confirm 权威列举（补「审与不审」）。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 410 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- 未 push、未 dotf 同步。
- taskrail / task-explore 对本轮新纪律的引用属各自后续轮次（R3/R4）。
