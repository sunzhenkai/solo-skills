# 契约守卫测试：task-explore 新增规则

- target: skills/task-explore
- mode: update
- patch: 20261010-221500-grill-quality-guard-tests
- risk: low
- status: proposed

## Intent

为上一轮（20261010 同批）刚写入 task-explore 的契约规则补确定性守卫断言，防止后续编辑无声抹掉规则。仅新增测试断言，不改生产正文。

## Conflict check

none —— 断言内容与已应用的契约正文一一对应。

## Rationale

本仓惯例：每个 skill 用 `tests/test_*_contract.py` 以文本断言钉契约条款（`skills-store` 亦有同类 patch 先例）。新规则若无断言，属未守卫契约。

## Files

- `skills/task-explore/tests/test_task_explore_contract.py` — 追加一个测试方法。

## Validation

- 应用前：`git apply --check`。
- 应用后：`python3 -m pytest skills/task-explore/tests -q` 全绿。
