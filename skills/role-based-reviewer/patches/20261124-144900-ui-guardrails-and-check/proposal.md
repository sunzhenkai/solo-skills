# 明确 design 评审与运行态机械门的分工

- target: skills/role-based-reviewer
- mode: update
- patch: 20261124-144900-ui-guardrails-and-check
- risk: low
- status: applied

## Intent

当调用方提供 `ui_evidence_check` 的 `report.json` 时，运行时报错、裂图、溢出、环被裁、极小热区、焦点遮挡、浮层内边距/焦点进出与 axe WCAG 2.2 AA 直接以报告为准，避免 `design` 角色重复人肉扫查，把注意力集中在交互逻辑、信息架构与视觉层级。

## Files

- `skills/role-based-reviewer/references/roles/design.md`：新增「与运行态机械门分工」。
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`：新增守卫断言。
