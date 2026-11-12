# 恢复 router 契约锚点

- target: skills/taskrail
- mode: update
- patch: 20261112-174022-router-contract-anchor
- risk: low
- status: proposed

## Intent

恢复 router 第三步的“当前最关键不确定性”原文，保留从 context/current 选择依赖就绪 U-n 的新行为，修复上一轮引入的文本契约回归。

## Conflict check

不改变动态路由、goal 连续推进或 U-n / F-n 契约；既有测试保持原样。

## Rationale

失败仅由既有锚点措辞被无意缩短引起。恢复原措辞是根因修复，不改变测试来换取通过。

## Files

- skills/taskrail/references/router.md：恢复“当前最关键不确定性”原文。

## Validation

- git apply --check --recount。
- git diff --check -- skills/taskrail。
- python3 -m pytest skills/taskrail/tests -q。
- python3 -m pytest skills -q。
- make check-names 与 make check-style。
