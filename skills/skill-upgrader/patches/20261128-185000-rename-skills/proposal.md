# 同步改名引用（skill-upgrader）

- target: skills/skill-upgrader
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

随 agent-docs-writer 改名为 agent-docs，同步 SKILL.md、evolve.md 与契约测试。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/skill-upgrader/SKILL.md`
- `skills/skill-upgrader/references/evolve.md`
- `skills/skill-upgrader/tests/test_skill_upgrader_contract.py`

## Validation

- `python3 -m unittest discover -s skills/skill-upgrader/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
