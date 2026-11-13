# 接入 project-explore 查询与摄入交接

- target: skills/wiki-data
- mode: update
- patch: 20261113-215332-project-explore-handoff
- risk: medium
- status: proposed

## Intent

将业务源码探索入口改为 project-explore。wiki-data 可接收 ExplorationBrief 与 Atlas 回执作为候选材料；Atlas 缺失、未覆盖、过期或冲突且需要核实代码时交给 project-explore，query 保持只读。

## Conflict check

现有 Atlas/wiki 单一正文和先 Atlas 后 wiki 的顺序不变。Brief 只是候选材料，不替代归档列表、写盘确认、sources 或 lint。本轮不改 wiki 布局、页面类型和 lint 脚本。

## Rationale

该交接补齐联合查询的取证路径，同时保持 wiki-data 不直接探索源码的边界。契约测试可验证名称、只读查询和摄入门禁。

## Files

- skills/wiki-data/SKILL.md：更新源码探索 skill 名称。
- skills/wiki-data/references/ingest.md：接收 Brief 与 Atlas 回执为候选输入。
- skills/wiki-data/references/query.md：补 Atlas 缺口和冲突后的 project-explore 交接。
- skills/wiki-data/tests/test_wiki_data_contract.py：更新并增加交接断言。

## Validation

- 机械生成 change.patch，git apply --check --recount。
- 用户已批准具体集成方案，medium 风险门禁已通过。
- 应用后运行 git diff --check 和 wiki-data 测试。
