# 修正精简表达后的契约兼容

- target: skills/taskrail
- mode: update
- patch: 20261110-142709-user-output-contract-compat
- risk: medium
- status: proposed

## Intent

修复上一 patch 的验证失败：恢复难回头决定必须突出展示的行为，保留内部记账与调度直接执行的边界；将仍锁定旧固定措辞的测试改为校验普通可逆取舍、恢复上下文和意图纠偏的正向行为。

## Conflict check

本 patch 不恢复固定话术，不改变上一 patch 的方法论；仅补齐被漏掉的突出风险要求，并让测试锚定当前契约。

## Rationale

测试失败提供了明确兼容缺口。难回头决定的可见性属于风险披露，应保留；其余断言可通过更通用的行为句守卫，避免重新绑定模板。

## Files

- skills/taskrail/references/user-report.md：恢复难回头决定单独说和内部操作直接做。
- skills/taskrail/tests/test_decision_boundary_contract.py：普通取舍断言改用统一术语。
- skills/taskrail/tests/test_decompose_contract.py：父子恢复改校验已验证现状与下一动作。
- skills/taskrail/tests/test_no_bookkeeping_questions.py：意图纠偏改校验明确邀请，而非固定话术。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后重跑 taskrail / taskflow 测试；通过后运行全仓测试与公开仓检查。
