# Complex 轨道的 explore 改为 design 第一步的 grill

- target: skills/agent-roster
- mode: update
- patch: 20261021-204720-decompose-rolling
- risk: low
- status: proposed

## Intent

taskrail 同 id 的 patch 把 explore 并成 design 的第一步，phase 枚举里不再有 explore。flow 模式 Complex 轨道跟着改三处：

- 理解 Stage 原来写「走 wizard / explore」，改成「走 wizard 与 design 第一步的 grill」。
- 定方案 Stage 写明是「design（写方案）」。
- flow-stages 和 eval 里的说法同步改。

非目标：Stage 划分和派出规则不变；「不调用 `grill-with-docs`」这条保留。

## Conflict check

- `test_flow_contract.py` 锚定的两句「不调用 `grill-with-docs`」和「`$taskrail`」都保留。

## Rationale

指向已经不存在的 phase，会让 Orchestrator 在 taskrail 里找不到对应的阶段细则。

## Files

- `skills/agent-roster/references/flow-tracks.md`
- `skills/agent-roster/references/flow-stages.md`
- `skills/agent-roster/evals/cases.yaml`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/agent-roster`；`python3 -m pytest skills/agent-roster/tests -q`
