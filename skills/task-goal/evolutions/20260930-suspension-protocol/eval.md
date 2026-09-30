# Eval：suspension-protocol

## 回归

- 全仓契约测试：364 passed, 1 skipped（候选 staged 后）。新增 6 条
  TestSuspensionProtocol 断言在候选写入前 1 failed（引用计数）/
  写入后全过；写文件类断言（五元组字段、白名单、blocked 四段）针对
  新文件，本身即新契约。
- 既有规则零删除：diff 仅「授权」节两段改写——停下形状从散文描述
  （「写明事实、推荐意见与需要的一句话决定」）升级为指向五元组，
  推荐意见保留；自动续跑段只追加索引句并声明「以本节为准」，
  与 state-machine.md 的索引关系先例一致。
- goal_transition.py 的 state-file 字段集合未动（TestGoalTransitionScript
  全过）：五元组是回复呈现协议，不进状态文件，脚本无需改。

## 模式

- 两个真实 blocked case 的交接摘要（已完成/未完成/证据/下一步）正是
  本协议 blocked 四段的实例——协议是从已验证行为抽象，不是新发明。
- 审计发现的「非 goal 模式首次停下无形态」由「首次停下即按五元组
  呈现」条款覆盖（契约断言锁定）。
- 「恢复义务全在用户」由恢复触发条款部分缓解：恢复回复必须先核对
  授权形状、第一行写「已解除/仍未解除」——恢复动作本身有了协议形状。

## 契约

- `python3 -m pytest skills/task-goal/tests -q`：84 passed。
- `python3 -m pytest skills -q`：364 passed, 1 skipped。
- 跨 skill：taskflow / task-delivery 尚不引用 suspension.md（按提案，
  接入各走各的进化轮），无连带更新。

## 副作用

- 触发范围：纯新增 reference + 两句引用；无新允许动作，无新停止条件。
- 权限：白名单条款逐字沿用既有「授权」节的允许/禁止清单，未放宽。
- 风险点（诚实记录）：五元组是呈现协议，依赖执行者如实填写；与
  state-machine.md 的关系靠「以本节为准」声明，与现有索引先例同构。

## 结论

pass
