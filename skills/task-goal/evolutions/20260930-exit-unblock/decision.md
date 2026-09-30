# Decision: promote

- patch: evolutions/20260930-exit-unblock
- decision: promote
- date: 2026-09-30
- 用户确认: 五项 Phase 计划（含 A/B 分级规则全文与「不可逆动作仍逐字
  点名」边界）于当轮批准，「开始」确认 Phase 1。risk: high 项（B 类
  降级放宽为审阅临时确认 + 追认）在计划表与 proposal.yaml 中单列。

## 原因

- 两个真实 blocked case + 一条真实用户纠正记录，病灶模式稳定
  （降级一刀切停机、授权逐字匹配、无进展轮括号反向）。
- eval 全项 pass：9 条新/改断言红绿验证；A 类硬门与「confirmed 只有
  用户能写」逐字保留；全仓 371 passed。
- 改动与 Proposal 一致：SKILL.md 四处（审阅边界、降级未确认、授权
  echo-back、无进展轮括号、做完完成门）、quality-profile.md（schema
  扩定级/回滚说明/provisional、显式降级六条、完成门）、
  state-machine.md（用户授权与判据成立定义、括号）、state-file.md
  （事件推断 2），无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 371 passed, 1 skipped。
- 候选目录与生产稿 diff 为空（四处文件逐一比对）。

## 未做（按 skill-evolver 边界）

- 未 commit 由本轮统一提交（用户已在计划中批准逐 Phase commit）；未
  push、未执行 dotf 同步，由使用者经安装通道同步。
- Phase 2（task-delivery / taskflow 接入非依赖面 + 修复连败计数）属
  后续各自进化轮。
