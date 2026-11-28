# Proposal: add-agent-friendly-api

## 动机
从 `llmwiki` 面向 Agent 的 Wiki 与档案 HTTP API / MCP 全面优化实践中，提炼跨项目可复用的 Agent 友好 API 设计模式，并与既有负责鉴权与接入话术的 `agent-api-access.md` 解耦。

## 改动范围
- `skills/project-patterns/references/agent-friendly-api.md`：新增模式卡（动机、参与者、六件套落地件、边界、先例、更正记录）。
- `skills/project-patterns/references/agent-api-ops.md`：在 `## 操作纪律` 增补优先局部修改、携带乐观锁、批量先 `dry_run` 三条调用规范。
- `skills/project-patterns/SKILL.md`：登记新模式卡索引并升级版本 `1.4.0 -> 1.5.0`。
- `skills/project-patterns/tests/test_project_patterns_contract.py`、`test_agent_api_ops_contract.py`：补充契约断言。

## 预期影响
- 新建或重构个人知识库、文档、个人资产类服务时，可直接按六件套对照设计或评审 Agent 友好 API。
- 无私有项目名、内部主机名或凭据引入。
