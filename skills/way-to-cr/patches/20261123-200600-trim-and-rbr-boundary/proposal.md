# 补齐 role-based-reviewer 边界指针并精简 SKILL.md 体量

- target: skills/solo-code-review
- mode: update
- patch: 20261123-200600-trim-and-rbr-boundary
- risk: low
- status: proposed

## Intent

将岗位/架构/规格评审边界显式指向 `role-based-reviewer`，并精简 SKILL.md 冗长段落以从 8094B 降至 7600B 以下。

## Conflict check

配套 patch：skills/role-based-reviewer 将在 Phase 2 补齐反向边界。

## Rationale

原 SKILL.md 距 8192B 红线仅 98B，且未按名指回 role-based-reviewer。

## Files

- `skills/solo-code-review/SKILL.md`：指向 role-based-reviewer 并精简重复表述
- `skills/solo-code-review/tests/test_skill_contract.py`：增加 role-based-reviewer 边界与体量守卫断言

## Validation

- `git apply --check --recount skills/solo-code-review/patches/20261123-200600-trim-and-rbr-boundary/change.patch`
- `python3 -m unittest discover -s skills/solo-code-review/tests -p 'test_*.py'`
- `make check-style && make check-names`
