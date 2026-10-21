# flow 模式 Complex 轨道改绑 taskrail

- target: skills/agent-roster
- mode: update
- patch: 20261021-202819-merge-explore-intent
- risk: low
- status: proposed

## Intent

task-explore 并入 taskrail（同 id 的 taskrail patch）。flow 模式 Complex 轨道原来绑的是 `$task-explore` 的 `new` / `decide` / `archive`，其中 `new`、`decide` 早已不存在，explore 也不再委托 `grilling`。改为：理解 Stage 用 `$taskrail` 建任务并走 wizard / explore；定方案 Stage 用 `$taskrail` 的 design → approve → handoff，之后照旧 `$taskflow` → `$openspec-propose`；收尾按 taskrail 完成清单标 `done` 并归档。

非目标：Stage 划分、派出规则、Resident 规则不变。

## Conflict check

- 「不调用 `grill-with-docs`」这条约束保留（测试锚定）。
- 收尾从「探索任务保持 handed-off」改为「过完成清单后标 done 并归档」，与 taskrail 第 1 步补上的任务归档规则一致。

## Rationale

指向已删除或不存在的命令会让 Orchestrator 找不到入口。

## Files

- `skills/agent-roster/references/flow-tracks.md`
- `skills/agent-roster/references/flow-stages.md`
- `skills/agent-roster/evals/cases.yaml`
- `skills/agent-roster/tests/test_flow_contract.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/agent-roster`；`python3 -m pytest skills/agent-roster/tests -q`
