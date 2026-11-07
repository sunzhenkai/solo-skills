# 将模板状态说明移到 TASK 标题前

- target: skills/taskrail
- mode: update
- patch: 20261107-081212-template-heading-compat
- risk: low
- status: proposed

## Intent

仅移动上一 patch 新增的说明文字，使 `## TASK.md` 后仍紧跟 markdown 代码块，满足 taskflow 既有模板提取契约。规则与示例字段不变。

## Conflict check

无；不改 taskflow，不改实际任务状态。

## Rationale

保持模板机器可提取，同时保留“新建根任务从 intake 开始”的说明。

## Files

- skills/taskrail/references/templates.md：移动说明位置。

## Validation

- `git apply --check --recount`。
- 运行 taskflow 模板兼容测试、taskrail 测试、全量测试与公开仓检查。
