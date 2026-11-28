# 同步改名引用（taskrail）

- target: skills/taskrail
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

随 role-based-reviewer → role-review、agent-docs-writer → agent-docs、project-design-patterns → project-patterns 改名，同步 SKILL.md、evals、references 与契约测试。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/taskrail/SKILL.md`
- `skills/taskrail/evals/cases.yaml`
- `skills/taskrail/references/close.md`
- `skills/taskrail/references/design.md`
- `skills/taskrail/references/review.md`
- `skills/taskrail/tests/test_taskrail_contract.py`

## Validation

- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
