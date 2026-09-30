# Decision: promote

- patch: evolutions/20260930-review-loss-streak
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 于 2026-09-30 当轮以「两个都按顺序做」确认（risk: medium 已明示）。

## 原因

- 同类失败两个真实 case（2026-09-30 两个复杂档 goal blocked，结构相同：
  旧账全消、新账全是修复引入的回归条，轮次封顶焊死唯一修改通道），
  同族审计确认缺陷在 task-delivery 修复循环复发——模式稳定。
- eval 全项 pass：新增 7 条契约断言对旧稿失败、对候选稿全过；
  全仓 358 passed；真失败形态（连败/恶化）仍封顶，权限只严不松。
- 改动与 Proposal 一致：仅核对网格两条 + 退出点定义一句 +
  state-machine.md 事件定义一行同步，无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 358 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
- task-delivery loop-protocol.md:143 的同族缺陷（窄切片两轮修复封顶）
  未在本轮修改——属 task-delivery 自己的进化轮。
