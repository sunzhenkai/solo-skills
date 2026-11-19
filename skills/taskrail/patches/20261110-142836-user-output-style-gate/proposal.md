# 补齐精简表达的风格门禁对照

- target: skills/taskrail
- mode: update
- patch: 20261110-142836-user-output-style-gate
- risk: low
- status: proposed

## Intent

为 user-report 补三组方法论层面的前后对比，满足仓库现有输出风格门禁；不恢复具体任务话术，不改变已应用的行为契约。

## Conflict check

none

## Rationale

现有检查明确要求至少三组前后对比。用抽象对照说明结论先行、增量同步和风险完整，既保留门禁，也维持本轮精简具体描述的目标。

## Files

- skills/taskrail/references/user-report.md：增加三组方法论前后对比。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后重跑全仓测试、check-names、check-style 和 diff 检查。
