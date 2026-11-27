# 仅显式要求或观感交付时进入 review，禁止自动触发 solo-code-review

- target: skills/taskrail
- mode: update
- patch: 20261127-084500-review-explicit-only
- risk: high
- status: proposed

## Intent

收紧 `taskrail` 动态路由中 `review` 环节的进入条件，避免常规代码开发任务在验证后自动触发 `solo-code-review`（OCR）：

1. 将 `review` 的触发条件收敛为「用户 / 方案明确要求独立评审，或命中观感交付验收」；常规代码改动默认跳过 `review`，由 `execute` 自检与 `verify` 闭环。
2. 明确 `solo-code-review`（OCR / Git diff 自动化审查）仅在用户明确要求时调用，绝不在 `taskrail` 常规任务中自动触发。
3. 补齐契约测试与回归用例守卫该约束。

非目标：不修改 `solo-code-review` 自身行为，不移除 `review.md` 与 `role-based-reviewer` / `solo-code-review` / `agent-roster` 的软指针，不修改历史 `patches/`。

## Conflict check

- 无冲突；保留 `review.md` 八节结构、`RF-n` 编号以及 `role-based-reviewer`、`solo-code-review`、`agent-roster` 软指针。
- 仓级配套同步 `docs/task-flow/README.md`「动态 references 怎么选」对应行（不在本 patch diff 内）。

## Rationale

原先 `router.md` 与 `review.md` 将「复杂 diff」「公共契约」等列为 `review` 进入条件，且 `review.md` 将纯 Git diff 审查默认分流给 `solo-code-review`，导致跨模块常规开发在跑完测试后自动进入 `review` 并调起 OCR 交互门。收敛触发条件并在分流中限定 `solo-code-review` 为显式触发，可保持常规交付链路顺畅，同时保留显式评审与观感验收能力。

## Files

- `skills/taskrail/references/router.md`：更新 `review` 路由表触发条件与默认跳过说明。
- `skills/taskrail/references/review.md`：收紧目的、进入条件、跳过条件及 `solo-code-review` 分流条件。
- `skills/taskrail/tests/test_taskrail_contract.py`：新增 `review` 仅显式/观感触发且不自动调用 `solo-code-review` 的契约测试。
- `skills/taskrail/evals/cases.yaml`：新增 `review-explicit-only-no-auto-code-review` 回归用例。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-084500-review-explicit-only/change.patch`
- `git diff --check -- skills/taskrail/references skills/taskrail/tests skills/taskrail/evals docs/task-flow/README.md`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
