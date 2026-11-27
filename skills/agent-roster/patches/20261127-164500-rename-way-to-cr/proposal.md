# 更新跨 skill 引用为 way-to-cr

- target: skills/agent-roster
- mode: update
- patch: 20261127-164500-rename-way-to-cr
- risk: low
- status: applied

## Intent

随 `solo-code-review` 改名为 `way-to-cr`，同步更新 `agent-roster` flow 模式 references、evals 与契约测试。

## Files

- `skills/agent-roster/references/flow-context.md`
- `skills/agent-roster/references/flow-stages.md`
- `skills/agent-roster/references/flow-tracks.md`
- `skills/agent-roster/references/flow.md`
- `skills/agent-roster/evals/cases.yaml`
- `skills/agent-roster/tests/gate_lines.txt`
- `skills/agent-roster/tests/test_flow_contract.py`
