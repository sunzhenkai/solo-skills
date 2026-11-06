# llm-wiki 改名 wiki-data 并接入可选排查归档

- target: skills/llm-wiki → skills/wiki-data
- mode: update
- patch: 20261106-184157-rename-wiki-data
- risk: medium
- status: proposed

## Intent

将 skill 标识与目录统一改为 `wiki-data`，保持既有 Markdown 工作区、typed 页面和 lint 行为兼容。增加按需接收 `trouble-grill` 排查记录的摄入规则；根因排查仍由 `trouble-grill` 独立承担。

## Conflict check

`llmwiki` 是正文明确排除的外部工具名，不在改名范围内。历史 `patches/` 只随目录迁移，不改写内容。复用现有 `source` / `synthesis` 类型，不改变工作区 schema。

## Rationale

名称与职责统一，同时通过现有 ingest 流程承接经过证据分级的排查知识。显式归档和既有页面类型使联动可选、可验证且无运行时依赖。

## Files

- `skills/llm-wiki/` → `skills/wiki-data/`：目录及全部生产文件改名，历史 patches 仅随容器迁移。
- `SKILL.md`：frontmatter、标题、slash 命令与 `trouble-grill` 职责边界。
- `references/ingest.md`：排查记录的来源映射、证据保留与 confirmed 门禁。
- `agents/openai.yaml`：展示名与默认命令。
- `scripts/lint_wiki.py`：生成索引中的维护者名称。
- `tests/test_llm_wiki_contract.py` → `tests/test_wiki_data_contract.py`：新名称与联动契约。
- `tests/test_lint_wiki.py`：索引维护者断言。

## Validation

- `git apply --check --recount` 通过后应用；目录名与 frontmatter `id` / `name` 一致。
- 目标测试与全仓 `python3 -m pytest skills -q`。
- `make check-names`、`make check-style`、`git diff --check`。
- 检查有效引用已迁移，历史 patch 与外部工具名 `llmwiki` 未被误改。
