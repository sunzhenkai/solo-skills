# 同步改名引用（agent-roster）

- target: skills/agent-roster
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

随 role-based-reviewer 改名为 role-review，同步 flow-stages.md 与 flow-tracks.md 中的引用。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/agent-roster/references/flow-stages.md`
- `skills/agent-roster/references/flow-tracks.md`

## Validation

- `python3 -m unittest discover -s skills/agent-roster/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
