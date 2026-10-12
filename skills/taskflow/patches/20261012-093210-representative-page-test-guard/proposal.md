# 代表页规则的测试守卫

- target: skills/taskflow
- mode: update
- patch: 20261012-093210-representative-page-test-guard
- risk: low
- status: proposed

## Intent

契约测试与 eval 改为断言代表页先实现，以及无 Active Instance 时先建立再写页面。

## Conflict check

none

## Rationale

上一轮正文已改，测试仍锁旧句，会误报失败。

## Files

- skills/taskflow/tests/test_execution_spine_contract.py
- skills/taskflow/evals/cases.yaml

## Validation

- git apply --check
- python3 -m unittest skills/taskflow/tests/test_execution_spine_contract.py
