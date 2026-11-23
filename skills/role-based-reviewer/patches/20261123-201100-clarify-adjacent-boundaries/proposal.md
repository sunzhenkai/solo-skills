# 补齐与 solo-code-review、role-chat 的双向边界

- target: skills/role-based-reviewer
- mode: update
- patch: 20261123-201100-clarify-adjacent-boundaries
- risk: low
- status: proposed

## Intent

在 SKILL.md 正文明确纯 diff/MR 自动化审查交给 `solo-code-review`、无代码取证的多视角陪练交给 `role-chat`。

## Conflict check

配套 patch：solo-code-review（20261123-200600-trim-and-rbr-boundary）已指回本 skill。

## Rationale

消除审查与角色问答类 skill 的触发歧义，建立双向边界。

## Files

- `skills/role-based-reviewer/SKILL.md`：补充 solo-code-review 与 role-chat 边界一句
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`：新增相邻 skill 边界守卫断言

## Validation

- `git apply --check --recount skills/role-based-reviewer/patches/20261123-201100-clarify-adjacent-boundaries/change.patch`
- `python3 -m unittest discover -s skills/role-based-reviewer/tests -p 'test_*.py'`
- `make check-style && make check-names`
