# flow Complex 轨道改按 taskrail 当前路由绑定

- target: skills/agent-roster
- mode: update
- patch: 20261118-013909-flow-taskrail-routing
- risk: medium
- status: proposed

## Intent

Complex 轨道的「理解 / 定方案 / 方案评审 / 实现 / 收尾」改为绑定 taskrail 当前的动态主干：理解走 `intent` 后按路由按需 explore / grill；定方案按路由产出当前最小计划，design / approve / decompose 命中才进入；执行由 taskflow 按 direct 或 OpenSpec 实施；收尾由 taskrail verify / close 写 `done`。非目标：Simple / Medium 轨道、Stage 顺序、Assignment 与委派规则不变。

## Conflict check

原文引用 taskrail 已移除的 wizard 与「design 第一步的 grill」，并把 approve、handoff、OpenSpec 写成必经步骤，与 taskrail `router.md`（按证据 enter / skip）和 contract.md（direct / OpenSpec 正交）冲突。本改动消除该冲突，不改 taskrail。

## Rationale

flow 模式在 Complex 轨道会按不存在的入口执行或强行走 OpenSpec。改为指向 taskrail 的路由后，taskrail 再演进时 flow 不需要跟着复制其内部步骤。

## Files

- skills/agent-roster/references/flow-tracks.md：重写 Complex 表五行。
- skills/agent-roster/references/flow-stages.md：理解、定方案、收尾三处 Complex 描述。
- skills/agent-roster/tests/test_flow_contract.py：新增 `test_complex_follows_taskrail_routing` 守卫断言。

## Validation

- `python3 -m pytest skills/agent-roster/tests -q`
- 全量 `python3 -m pytest skills tests -q`、`make check-style`、`make check-names`
