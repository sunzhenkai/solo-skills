# 将 taskrail 中的 solo-code-review 降为仅作提示

- target: skills/taskrail
- mode: update
- patch: 20261127-085500-solo-code-review-hint-only
- risk: medium
- status: proposed

## Intent

将 `solo-code-review` 在 `taskrail` 中彻底降为「仅作提示」，不再作为 `review` 环节的执行分支：

1. `references/review.md` 移除 `solo-code-review` 调用分支，仅保留「纯 Git diff / MR / PR 自动化代码审查不纳入本环节，如需可提示用户另行调用 `solo-code-review`」的边界提示。
2. `references/close.md` 在完成通知中顺带提示用户需要 diff / MR 级代码审查时可另行运行 `solo-code-review`，明确本环节不自动调用。
3. 同步更新 `tests/test_taskrail_contract.py` 与 `evals/cases.yaml`。

非目标：不修改 `agent-roster`、不修改 `solo-code-review` 自身、不修改历史 `patches/`。

## Conflict check

- 无冲突；不动 `agent-roster` 与历史 `patches/`；保留 `review.md` 八节结构、`RF-n`、`role-based-reviewer`、`solo-code-review` 与 `agent-roster` 软指针。

## Rationale

`taskrail` 常规开发已由 `execute` 自检与 `verify` 闭环，独立评审仅在用户/方案明确要求或观感验收时进入且走 `role-based-reviewer` / 异源模型审。将 `solo-code-review` 从 `review.md` 执行分流移除、改为 `close` 完成通知中的可选提示，可彻底解耦 `taskrail` 与 OCR 执行门。

## Files

- `skills/taskrail/references/review.md`：移除 `solo-code-review` 调用分支，仅留边界提示。
- `skills/taskrail/references/close.md`：完成通知中增加 `solo-code-review` 可选提示与不自动调用声明。
- `skills/taskrail/tests/test_taskrail_contract.py`：更新 `review` 与 `close` 契约守卫断言。
- `skills/taskrail/evals/cases.yaml`：更新 `review-explicit-only-no-auto-code-review` 用例期望。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-085500-solo-code-review-hint-only/change.patch`
- `git diff --check -- skills/taskrail/references skills/taskrail/tests skills/taskrail/evals docs/task-flow/README.md`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
