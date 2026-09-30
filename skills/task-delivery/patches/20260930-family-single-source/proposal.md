# Proposal：失败计数改引用真源 + 修 loop-protocol 的两处跨 skill 引用（批 B·task-delivery 侧）

## 背景

`SKILL.md` 的硬边界与 `references/loop-protocol.md` 的 Stop conditions 各自复述了失败计数的数字口径（「假设累计封顶 3」「累计假设已达 3 个仍失败」「同一条 P0/P1 连续两轮修复仍在」）。数字口径的真源在 `task-goal/SKILL.md` 的退出点节；副本曾漂移过一次（提交 `38983ee` 是手工同步记录）。

`loop-protocol.md` 里两处指向 task-goal 的链接本身深度正确（该文件在 `references/` 下），但引用目标在去重后要改。

## 决定

- `SKILL.md` 硬边界：两条（A/B 降级、失败计数）合并为一条「唯一真源是 task-goal」+ 指向 `quality-profile.md` 的「显式降级」节与 `task-goal/SKILL.md` 的退出点；保留 hooks（A 类 pending 停机、B 类不停机、命中上限即停并输出诚实报告）。
- `loop-protocol.md` Stop conditions：两条计数项合并为「失败计数命中上限（唯一真源见 task-goal 退出点）」；保留 delivery 特有的「假设与判伪差异记入验证记录」。
- `loop-protocol.md` Stage 2 的降级定级引用改指 `../task-goal/references/quality-profile.md`。

## 理由

消费者不复述数字，改一处即全局生效；delivery 特有的记录要求（验证记录、判伪差异）保留，因为那是 delivery 的产物形态，不属于 task-goal 的计数定义。

## 验证

- 族级测试 `TestFailureCountingSingleSource`：delivery 正文不得出现「假设累计封顶 3」与「累计假设已达 3 个」。
- 同步改 `tests/test_task_delivery_contract.py` 三条断言：从「副本逐字一致」改为「引用真源且不复述数字」。改测试的理由：原断言锁的是本次要消除的重复本身。

## 明确不改

Stage 9 修复循环的流程（按 finding 计数、语义指纹跟踪）、预算语义、增量验证协议、其余 Stop conditions。
