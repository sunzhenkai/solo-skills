# 可选 Worker 座位：宿主 subagent 推荐派出

- target: skills/taskrail
- mode: update
- patch: 20261010-224056-optional-worker-seat
- risk: medium
- status: applied

## Intent

在 taskrail 契约中增加精简的「执行座位」：高噪声单位**推荐**交给 worker（同机通道抽象为宿主 subagent）；派出非强制，缺能力时主会话自做。不改阶段枚举、不改闸口归属、不新增 skill / reference 文件。

## Conflict check

- 与 task-confirm 审阅三选一不冲突：审阅仍只读；本轮不另造 reviewer 座位。
- 与 taskflow 并行 / implementer-isolation 不冲突：apply 细节只引用，不复制。
- 经另一模型评审后删减：去掉独立 `worker-brief.md`、CONTEXT 术语、YAML Brief、过宽推荐表。

## Rationale

同会话堆探索/实现噪声污染编排注意力；真边界靠可选派出。推荐非强制，避免无宿主 subagent 时断轨。

## Files

- `skills/taskrail/references/contract.md` — 「执行座位」一节（约 15 行）。
- `skills/taskrail/SKILL.md` — 主循环一句 + 硬边界非强制。
- `skills/taskrail/tests/test_taskrail_contract.py` — 4 条守卫断言。
- `skills/taskrail/evals/cases.yaml` — optional-worker 案例。

## Validation

- 应用前：`git apply --check --recount`。
- 应用后：`python3 -m pytest skills/taskrail/tests -q`；`git diff --check -- skills/taskrail`（排除 patches/）。
