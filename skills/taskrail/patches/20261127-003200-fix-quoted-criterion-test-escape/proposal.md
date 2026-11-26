# 修复引号往返单测断言字面量转义

- target: skills/taskrail
- mode: update
- patch: 20261127-003200-fix-quoted-criterion-test-escape
- risk: low
- status: proposed

## Intent

修复 `20261127-002600-p0-contract-and-gates` 新增单测 `test_criterion_with_quotes_round_trips_cleanly` 中断言字符串的转义错误，改用 `json.dumps(text, ensure_ascii=False)` 构造精确期望行。

非目标：不修改生产脚本与文档。

## Conflict check

none（承接 `skills/taskrail/patches/20261127-002600-p0-contract-and-gates/`，仅修复测试字面量转义）。

## Rationale

`task_state.py` 已正确往返保留转义双引号，仅测试断言因普通单引号字符串将 `\"` 解释为 `"` 而误报。

## Files

- `skills/taskrail/tests/test_task_state.py`：修正 `test_criterion_with_quotes_round_trips_cleanly` 的期望字符串构造。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-003200-fix-quoted-criterion-test-escape/change.patch`
- `git diff --check -- skills/taskrail`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`、`python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`、`python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names` 与 `make check-style`
