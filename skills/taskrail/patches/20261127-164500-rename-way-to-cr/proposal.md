# 更新跨 skill 引用为 way-to-cr

- target: skills/taskrail
- mode: update
- patch: 20261127-164500-rename-way-to-cr
- risk: low
- status: applied

## Intent

随 `solo-code-review` 改名为 `way-to-cr`，同步更新 `taskrail` 的 references、evals 与契约测试。

## Files

- `skills/taskrail/references/close.md`
- `skills/taskrail/references/router.md`
- `skills/taskrail/references/review.md`
- `skills/taskrail/evals/cases.yaml`
- `skills/taskrail/tests/test_taskrail_contract.py`
