# 接入 project-explore 取证交接

- target: skills/project-atlas
- mode: update
- patch: 20261113-215247-project-explore-handoff
- risk: medium
- status: proposed

## Intent

将一次性项目问答与代码取证入口改为 project-explore。Atlas 可接收 ExplorationBrief 和持久化建议，但仍须按 sources 语义复核并执行 verify/build/check；wiki-data 联动保持不变。

## Conflict check

project-explore 已收缩为只读取证和路由，不与 Atlas 争抢当前系统说明的写入权。本轮不改 atlasctl、页面 schema 或静态站点契约。

## Rationale

明确 Brief 是调查输入而非已核实正文，可复用探索结果且不降低 Atlas 验证门槛。契约测试与 eval 覆盖该交接。

## Files

- skills/project-atlas/SKILL.md：更新边界并增加 project-explore 联动。
- skills/project-atlas/tests/test_project_atlas_contract.py：守卫 Brief 复核与验证交接。
- skills/project-atlas/evals/cases.yaml：增加探索结果进入 Atlas 的案例。

## Validation

- 机械生成 change.patch，git apply --check --recount。
- 用户已批准具体集成方案，medium 风险门禁已通过。
- 应用后运行 git diff --check 和 project-atlas 测试。
