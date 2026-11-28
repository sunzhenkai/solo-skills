# 新增「接口访问统计」模式卡

- target: skills/project-patterns
- mode: update
- patch: 20261128-202000-add-api-access-stats-pattern
- risk: low
- status: proposed

## Intent

将 14 个在线服务统一落地的「接口访问统计（有界异步采集 + 路由归一化 + 5 端点只读查询 + API Key 专项与零明文门禁）」方案沉淀为 `project-patterns` 新模式卡，供后续新服务设计或存量服务评审直接复用。

## Conflict check

- 仓内引用：仅新增 `references/api-access-stats.md`，在 `SKILL.md` 一层直链，不引入跨 skill 相对链接或超一层引用链。
- 命名与脱敏合规：14 处先例全部使用泛化应用形态描述，不含 `.project-denylist` 中的项目名、公司信息、真实内网域名/IP 或密钥前缀。

## Files

- `skills/project-patterns/references/api-access-stats.md`（新增模式卡）
- `skills/project-patterns/SKILL.md`（version 升至 `1.4.0`，更新 description 与模式索引）
- `skills/project-patterns/tests/test_project_patterns_contract.py`（新增模式卡契约测试）
- `README.md`（仓库级清单同步描述）

## Validation

- `python3 -m unittest discover -s skills/project-patterns/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names`
- `make check-style`
