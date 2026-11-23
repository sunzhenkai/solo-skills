# review：按需独立评审

## 目的
在高风险、公共契约、复杂 diff、安全 / 性能敏感或观感交付时引入独立只读评审，暴露实现者盲区。

## 进入条件
公共契约 / 迁移变化、复杂或高风险 diff、安全 / 性能敏感改动、观感交付，或用户 / 方案要求独立评审。

## 跳过条件
小且可逆改动，execute 阶段的 diff 自检与测试已覆盖全部风险。

## 所需输入
criterion、当前提交号或 worktree diff、审与不审范围、相关 design / 契约与运行态证据（截图 / 测试输出）。

## 执行方法
1. 按评审目标分流：
   - 多岗位、方案、契约、观感或 Skill 评审：调用 `role-based-reviewer`（`mode=review` + 完整 `roles=` 与审阅边界）；需跨机器 / 跨模型 Endpoint 派发时带 `endpoint=` 经 `agent-roster` 执行。
   - 纯 Git diff / MR / PR 自动化代码审查：调用 `solo-code-review`。
   - 对应下游 skill 未安装时，按 [confirm-protocol.md](confirm-protocol.md)「异源模型审」派异源模型或显式记录降级自审，不静默宣称独立通过。
2. 评审报告落 `reviews/<topic>.md`；Blocker / Major 按稳定编号 `F-n` 跟踪。
3. 处置记录由本任务维护：`fixed` 需附修复后重验证据；`accepted-recorded` 在 human 需用户明确接受，goal 不放行 Blocker / Major。

## 产出
`reviews/<topic>.md` 评审报告与 findings 处置记录。

## 完成门
所有 Blocker / Major 已 `fixed` 并重验，或按确认协议记为 `accepted-recorded`。

## 退出与重入
全部处置通过转 verify；指向实现回 execute，指向方案回 design / grill。代码变化后受影响的 findings 作废重审。
