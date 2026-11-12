# 对齐新增测试的既有锚点

- target: skills/taskrail
- mode: update
- patch: 20261112-174225-uncertainty-test-anchor
- risk: low
- status: proposed

## Intent

把新增 uncertainty 契约测试的路由锚点改为既有规范“当前最关键不确定性”，与已恢复的 router 正文和既有契约测试保持一致。

## Conflict check

只改本轮新增测试中的错误锚点，不修改既有测试，不改变 U-n 路由行为，不放宽断言范围。

## Rationale

同一行为规范应使用同一原文锚点。候选目录将先运行完整 taskrail 回归，确认没有第二轮措辞漂移。

## Files

- skills/taskrail/tests/test_uncertainty_contract.py：使用“当前最关键不确定性”锚点。

## Validation

- 候选目录运行 python3 -m pytest skills/taskrail/tests -q。
- git apply --check --recount。
- git diff --check -- skills/taskrail。
- 应用后运行 python3 -m pytest skills/taskrail/tests -q 与 python3 -m pytest skills -q。
