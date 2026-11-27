# 恢复 intent.md 纠偏重查守卫短语并保留 anti-lazy 接线

- target: skills/taskrail
- mode: update
- patch: 20261127-105700-preserve-intent-reread-phrase
- risk: low
- status: proposed

## Intent

恢复 `skills/taskrail/references/intent.md` 中被 `test_intent_source_first.py` 锁定的短语「用户指出错误先回一手资料重查」，同时保留 `anti-lazy` 纠偏重启接线（「走纠偏重启」）。

## Conflict check

none

## Rationale

`test_intent_source_first.py::SourceFirstTest::test_correction_reread` 断言 `intent.md` 包含「用户指出错误先回一手资料重查」。将该句保留在行首并把 `anti-lazy` 纠偏重启要求紧随其后，可同时满足两个契约。

## Files

- `skills/taskrail/references/intent.md`：保留原守卫短语并衔接 `anti-lazy` 纠偏重启

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-105700-preserve-intent-reread-phrase/change.patch`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-names && make check-style`
