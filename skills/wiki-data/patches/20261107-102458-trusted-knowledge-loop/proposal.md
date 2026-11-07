# 加固可信知识闭环与默认保存位置

- target: skills/wiki-data
- mode: update
- patch: 20261107-102458-trusted-knowledge-loop
- risk: medium
- status: proposed

## Intent

在已有摄入、查询和 archive / reopen 主干上补齐确定性保障：来源可验证、链接无歧义、索引可检查、归档免复审、重开处理替代关系；同时支持别名解析、摘要提示和健康统计。业务文档默认保存位置明确为 `{WIKI_ROOT}/wiki/` 下对应 typed 目录，目录结构不变。

## Conflict check

保持纯 Markdown、本地文件和 Python stdlib，不引入数据库或外部服务。`experience.status` / `ledger.status` 语义不变。新增来源要求只强制活跃业务页，归档页保留历史兼容。`--check-index` 只读，与 `--write-index` 分开。

## Rationale

来源、链接和索引直接决定查询是否可信；归档复审和替代页关系决定生命周期是否一致。所有规则均可由本地脚本和临时工作区验证。示例使用通用虚构内容，无个人、机器、私有项目或绝对路径。

## Files

- `skills/wiki-data/SKILL.md`：明确默认保存位置、索引检查和可信查询门禁。
- `skills/wiki-data/references/layout.md`：明确 wiki 保存位置及 guide 统计。
- `skills/wiki-data/references/page-types.md`：定义 sources、source 元数据、description 和 aliases 契约。
- `skills/wiki-data/references/ingest.md`：摄入时写来源元数据、摘要、别名并验证索引。
- `skills/wiki-data/references/query.md`：查询前检查索引，过期时回退文件系统。
- `skills/wiki-data/references/archive-reopen.md`：归档免复审与 reopen 替代页关系。
- `skills/wiki-data/references/lint.md`：新增检查码、CLI 和统计说明。
- `skills/wiki-data/scripts/lint_wiki.py`：实现受限 frontmatter 解析、来源校验、消歧、索引检查、别名与统计。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：补充行为文本契约。
- `skills/wiki-data/tests/test_lint_wiki.py`：补充确定性行为回归。

## Validation

- 应用前在临时完整副本跑目标测试，并执行 `git apply --check --recount`。
- 应用后执行 `git diff --check`、目标 unittest、全仓 pytest、公开名称与输出风格检查。
- 用临时工作区验证 init 后的 wiki 默认位置、来源、歧义链接、索引过期、archive / reopen、别名和 JSON 统计；raw 校验和保持不变。
