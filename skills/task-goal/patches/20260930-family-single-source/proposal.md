# Proposal：族级规则单一真源 + 修坏链 + 跨 skill 契约测试（批 B）

## 背景

查证后修正了原先的判断：**族级公共层已经存在**——`task-goal/references/suspension.md`（自述「族内通用定义」，taskflow 与 task-delivery 已在引用）与 `task-goal/references/quality-profile.md`（A/B 降级与确认门真源）。真正的问题是三件：

1. **副本没改引用**：task-delivery 的 `SKILL.md` 与 `references/loop-protocol.md` 复述了失败计数的数字口径（「假设累计封顶 3」「累计假设已达 3 个仍失败」「同一条 P0/P1 连续两轮修复仍在」），与 task-goal 的定义各写一份，已漂移过（提交 `38983ee` 是手工同步痕迹）。
2. **taskflow 三处跨 skill 链接深度写错**：`../../task-goal/...` 多退一层，实际是坏链；现有 `test_referenced_references_exist` 只查各 skill 自己目录，跨 skill 链接无人测。
3. **「在 goal 里」的触发判据两套**：`task-goal/SKILL.md` 与 `task-explore/SKILL.md` 各写一份，第三条不同。

## 决定

- **task-delivery**：`SKILL.md` 的硬边界与 `loop-protocol.md` 的 Stop conditions 去掉数字口径复述，改为「失败计数命中上限」+ 指向 task-goal 真源；delivery 特有的记录要求（假设与判伪差异记入验证记录）保留为 hook。同时把 `loop-protocol.md` 两处 `../../task-goal/` 修对（它在 `references/` 下，深度本来正确，本次只改引用目标）。
- **taskflow**：三处 `../../task-goal/...` 修为 `../task-goal/...`（`SKILL.md` 在 skill 根，只需退一层）。
- **新增族级契约测试** `task-goal/tests/test_task_family_contract.py`：4 组断言——载荷归属、失败计数单一真源、族内相对链接全可达、五个 task\* skill 齐备。
- **同步改 2 条既有断言**：`test_task_delivery_contract.py` 的 `TestRepairLossStreak::test_hard_boundary_synced` 与 `TestHypothesisStreakSync::test_hard_boundary_synced` / `test_stop_condition_synced`——它们原本断言「两处副本逐字一致」，去重后改为断言「引用真源且不复述数字」。

## 理由

- 副本改成引用是唯一能防漂移的做法：数字口径只写一处，改一处即全局生效。
- 链接测试用正则解析族内全部 markdown 的相对链接并逐个 `is_file()`——这是目前完全缺失的检查，也是那三处坏链能长期存在的原因。
- 触发判据的两套写法未在本次合并：它属于 owner 条款那一批（goal 是否接管 lifecycle）的范畴，与本次的引用去重不同源。

## 验证

- 族级测试 9 条全过；全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**。
- 反向验证：把 taskflow 一处链故意改回 `../../` 后，链接测试报出 `skills/taskflow/SKILL.md -> ../../task-goal/SKILL.md`；恢复后通过（测试有牙齿）。

## 明确不改

`suspension.md` 与 `quality-profile.md` 的内容与位置（它们已是真源）、`goal_transition.py`、状态机网格、触发判据的两套写法（留待 owner 批）。
