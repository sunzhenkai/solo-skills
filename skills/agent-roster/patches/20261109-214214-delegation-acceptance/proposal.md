# 委派任务完成条件与 Handoff 验收

- target: skills/agent-roster
- mode: update
- patch: 20261109-214214-delegation-acceptance
- risk: medium
- status: proposed

## Intent

让每次委派在 prompt 中明确 Goal、Context、Constraints、Done when，并要求 Orchestrator 按 Done when 逐项验收 Handoff。执行器的 completed 只表示执行结束，不代表任务质量验收通过。非目标：不调整选人、权限、执行器、Run 状态判定或 Trace 规则。

## Conflict check

现有流程已经要求显式说明期望产出，并在产出不对时返工；本更新把完成条件前置到 prompt，并把既有返工分类接入回收验收，不改变其他 Skill 的职责。

## Rationale

可检查的 Done when 让受派方知道完成标准，让 Orchestrator 能用实际 Handoff 而不是受派方自我声明验收。文本契约测试可固定输入要求、回收顺序和验收语义。

## Files

- skills/agent-roster/SKILL.md：在完整顺序的回收阶段加入 Done when 验收。
- skills/agent-roster/references/delegation-contract.md：定义 prompt 四要素与 Handoff 验收门禁。
- skills/agent-roster/tests/test_agent_roster_contract.py：增加委派输入与验收契约断言。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、agent-roster 契约测试、`make check-names` 和 `make check-style`。
- 核对实际 diff 仅包含上述文件，且无隐私信息。
