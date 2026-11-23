# 明示 flow 与 taskrail 边界、将 grill-with-docs 降级为可选并精简 SKILL.md

- target: skills/agent-roster
- mode: update
- patch: 20261123-202200-trim-and-optional-matt-deps
- risk: medium
- status: proposed

## Intent

在 `SKILL.md` 明确常规单机多阶段任务走 `taskrail`、按 Stage 跨 Endpoint 派单才用 `flow`；将 Simple/Medium 对 `$grill-with-docs` 的依赖降为可选（未安装时本会话复述+自问自答）；精简 SKILL.md 留出 8KB 裕度（不动 gate_lines 锁行）。

## Conflict check

配套修改：README「外部依赖」、AGENTS.md、Makefile 将 mattpocock/skills 降级为可选外部依赖。

## Rationale

缓解与 taskrail 的双头编排歧义，并消除整个仓库对 3 个仓外 skill 的强制检查依赖，同时让 SKILL.md 远离 8192B 上限。

## Files

- `skills/agent-roster/SKILL.md`：明示与 taskrail 边界并精简非门禁段落体量
- `skills/agent-roster/references/flow-tracks.md`：Simple/Medium 理解阶段将 `$grill-with-docs` 改为可选并附未安装回退
- `skills/agent-roster/references/flow-stages.md`：understand 阶段将 `$grill-with-docs` 改为可选并附未安装回退
- `skills/agent-roster/tests/test_flow_contract.py`：新增与 taskrail 边界、可选 grill-with-docs 及体量守卫断言

## Validation

- `git apply --check --recount skills/agent-roster/patches/20261123-202200-trim-and-optional-matt-deps/change.patch`
- `python3 -m unittest discover -s skills/agent-roster/tests -p 'test_*.py'`
- `make check-style && make check-names`
