# 新增「模型供应商管理」模式卡与可复用实现 Prompt

- target: skills/project-design-patterns
- mode: update
- patch: 20261126-142600-add-model-provider-pattern
- risk: low
- status: proposed

## Intent

将跨项目重复验证的「模型供应商配置（`models.dev` 目录加载 + 多选实例模型 + 消费端两级联动）」方案沉淀为 `project-design-patterns` 新模式卡，并提供可直接复用的实现 Prompt 引用件，供新项目或已有项目快速复用。

## Conflict check

- 仓内引用：仅新增 `references/model-provider-management.md` 与 `references/model-provider-impl-prompt.md`，在 `SKILL.md` 一层直链，不引入跨 skill 相对链接。
- 命名合规：两处先例分别记为「通用 Agent 平台」与 `llmwiki`，不引入 `.project-denylist` 中的项目名。

## Files

- `skills/project-design-patterns/references/model-provider-management.md`（新增模式卡）
- `skills/project-design-patterns/references/model-provider-impl-prompt.md`（新增可复用实现 Prompt）
- `skills/project-design-patterns/SKILL.md`（version 升至 `1.2.0`，更新 description、使用方式与模式索引）
- `skills/project-design-patterns/tests/test_project_design_patterns_contract.py`（新增模式卡与 Prompt 契约测试）
- `README.md`（仓库级清单同步描述）

## Validation

- `python3 -m unittest discover -s skills/project-design-patterns/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names`
- `make check-style`
