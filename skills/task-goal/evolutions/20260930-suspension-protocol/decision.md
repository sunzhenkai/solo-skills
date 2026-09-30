# Decision: promote

- patch: evolutions/20260930-suspension-protocol
- decision: promote
- date: 2026-09-30
- 用户确认: Proposal 于 2026-09-30 当轮以「两个都按顺序做」确认（risk: low，纯新增）。

## 原因

- 同族审计发现 5 个卡点同根（无挂起状态）；task-goal 的 blocked 交接
  形态已经两个真实 case 验证，模式稳定，可抽象为通用协议。
- eval 全项 pass：新增 6 条契约断言；全仓 364 passed；既有规则零删除，
  权限未放宽。
- 改动与 Proposal 一致：新增 references/suspension.md + 「授权」节
  两处引用改写 + 契约测试，无夹带编辑。

## 晋升后验证

- 覆盖生产稿后 `python3 -m pytest skills -q` → 364 passed, 1 skipped。

## 未做（按 skill-evolver 边界）

- 未 commit、未 push、未执行 dotf 同步；由使用者经安装通道同步。
- taskflow / task-delivery / task-explore 接入 suspension.md 属各自
  进化轮，未在本轮修改。
