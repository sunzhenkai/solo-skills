# 去特例化任务边界（事故补丁抽象）

- target: skills/role-based-reviewer
- mode: update
- patch: 20261015-234800-despecialize-task-boundary
- risk: medium
- status: applied

## Intent

把近期事故补丁里的具名例（部署映射 / agent_api / Dify / mcp-admin / i18n / 拓扑导入等）收成抽象原则；「不可跳过」只留「注意任务边界」；「不提问」真源只留 user-report；审美关键词改「观感类目标」；合同测试与 evals 锁抽象原则句。

## Conflict check

不改 UI 机械门、真阻塞类别、TASK.md「已做决定」契约名、intent 三项检查本身、pretty-view-html REFERENCE 路径。

## Files

见 change.patch。
