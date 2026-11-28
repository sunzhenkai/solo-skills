# 同步改名引用（way-to-cr）

- target: skills/way-to-cr
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

随 role-based-reviewer 改名为 role-review，同步 SKILL.md 与契约测试。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/way-to-cr/SKILL.md`
- `skills/way-to-cr/tests/test_skill_contract.py`

## Validation

- `python3 -m unittest discover -s skills/way-to-cr/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
