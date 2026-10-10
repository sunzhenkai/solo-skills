# 流程总览对齐规则落到执行侧（design 门禁 + approve 结构门）

- target: skills/task-explore
- mode: update
- patch: 20261010-222000-flow-align-execution-side
- risk: low
- status: proposed

## Intent

taskrail 契约的阶段载荷表新增「design 须把设计步骤对流程总览逐条映射、偏离写显式决策」，并注明由 approve 结构门核对。执行侧（phase-design 门禁、phase-approve 结构门）需各补一句，规则才不是悬空指针。

## Conflict check

none —— 与 phase-approve 既有结构门「写不出依据列入未决」同层，不新增门禁类型。

## Rationale

契约是载荷/闸口的唯一真源，但执行者读的是 phase 细则；两处各一句指向同一要求，避免规则只在编排层可见。

## Files

- `skills/task-explore/references/phase-design.md` — 门禁清单加一条流程总览对齐。
- `skills/task-explore/references/phase-approve.md` — 结构门核对项加流程总览对齐。

## Validation

- 应用前：`git apply --check`。
- 应用后：`python3 -m pytest skills/task-explore/tests -q` 全绿。
