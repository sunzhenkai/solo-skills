# 增加 wiki 页面归档与重开生命周期

- target: skills/wiki-data
- mode: update
- patch: 20261107-100031-page-archive-reopen
- risk: medium
- status: proposed

## Intent

为已有知识页增加通用、可逆的 `archive` / `reopen` 阶段。归档采用原地元数据标记，保留来源、链接和历史；查询与索引默认隔离归档页。知识摄入仍走 `ingest`，经验验证状态与业务台账状态保持不变。

## Conflict check

不引入 `wiki/archive/` 目录，避免破坏 typed 目录和现有链接。不复用 `status` 表示归档，避免与 experience / ledger 的既有语义冲突。不修改其它 Skill 的职责或安装镜像。

## Rationale

现有 ingest 已覆盖保存计划、来源、置信度、时效与排查记录，但缺少整页退役和恢复契约。原地归档适合高密度互链的 Markdown wiki；确定性 lint、索引分组和行为测试可验证该能力。所有示例与字段均为通用内容，不含个人、机器或私有项目数据。

## Files

- `skills/wiki-data/SKILL.md`：注册 archive / reopen 阶段与按需加载入口。
- `skills/wiki-data/references/archive-reopen.md`：新增原地归档、重开及完成门。
- `skills/wiki-data/references/page-types.md`：定义归档元数据及其与 status 的边界。
- `skills/wiki-data/references/ingest.md`：覆盖替代旧页和归档命中的摄入行为。
- `skills/wiki-data/references/query.md`：默认排除归档页并提供历史查询语义。
- `skills/wiki-data/references/lint.md`：记录归档检查码和索引行为。
- `skills/wiki-data/scripts/lint_wiki.py`：校验归档元数据、归档引用、孤立页及索引分组。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：补充生命周期文本契约，遵循本仓测试不模拟执行的约定。

## Validation

- 应用前执行 `git apply --check --recount`。
- 应用后执行 `git diff --check`、wiki-data unittest、全仓测试、公开名称与输出风格检查。
- 用临时 Markdown 工作区运行真实 lint CLI，验证归档索引、历史查询元数据、重开后恢复及 raw 不变；临时夹具不进入仓库。
