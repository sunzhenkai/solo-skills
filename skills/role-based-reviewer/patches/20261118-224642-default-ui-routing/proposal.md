# Proposal：design 评审返修交回 ui-kit

## Intent
design 角色继续使用 pretty-ui 规则号，但视觉返修先交回 ui-kit 选择通用或模板路线，避免评审下游绕过默认入口。

## Files
- `skills/role-based-reviewer/references/roles/design.md`
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`
- `README.md` 依赖组由 ui-kit patch 一并收录

## Tests
验证 ui-kit 链接可解析、通用与模板承接方明确；既有视觉规则号和评审级别不变。
