# review：按需独立评审

## 目的
仅在用户或方案明确要求独立评审，或命中观感交付验收时引入独立只读评审，暴露实现者盲区。

## 进入条件
用户明确要求独立评审、已确认方案（PLAN / design / approve）写明评审项，或任务命中观感交付验收（见 [done.md](done.md)「观感验收」）。

## 跳过条件
默认跳过。未显式要求独立评审且非观感交付的常规代码任务（含跨模块、公共契约或较大 diff），由 execute 阶段 diff 自检与 verify 验证直接闭环，不自动进入本环节。

## 所需输入
criterion、当前提交号或 worktree diff、审与不审范围、相关 design / 契约与运行态证据（截图 / 测试输出）。

## 执行方法
1. 调用 `role-based-reviewer`（`mode=review` + 完整 `roles=` 与审阅边界）；需跨机器 / 跨模型 Endpoint 派发时带 `endpoint=` 经 `agent-roster` 执行。对应下游 skill 未安装或不可用时，按 [confirm-protocol.md](confirm-protocol.md)「异源模型审」派异源模型或显式记录降级自审，不静默宣称独立通过。纯 Git diff / MR / PR 自动化代码审查不纳入本环节，如需可提示用户另行调用 `solo-code-review`。
2. 评审报告落 `reviews/<topic>.md`；Blocker / Major 按稳定编号 `RF-n` 跟踪。
3. 处置记录由本任务维护：`fixed` 需附修复后重验证据；`accepted-recorded` 在 human 需用户明确接受，goal 不放行 Blocker / Major。

## 产出
`reviews/<topic>.md` 评审报告与 findings 处置记录。

## 完成门
所有 Blocker / Major 已 `fixed` 并重验，或按确认协议记为 `accepted-recorded`。

## 退出与重入
全部处置通过转 verify；指向实现回 execute，指向方案回 design / grill。代码变化后受影响的 findings 作废重审。
