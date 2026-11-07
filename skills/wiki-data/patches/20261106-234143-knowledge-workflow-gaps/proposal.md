# 补齐经验、业务台账与检索闭环

- target: skills/wiki-data
- mode: update
- patch: 20261106-234143-knowledge-workflow-gaps
- risk: medium
- status: proposed

## Intent

围绕保存、检索知识、总结经验和记录业务对象台账补齐现有流程：新增 `experience` 与 `ledger` 页面类型，明确经验的适用边界与验证信息、台账的当前状态与追加历史，并将检索步骤下沉为按需加载的 reference。保持纯 Markdown、文件系统真相源和既有阶段，不引入数据库、搜索服务或新依赖。

## Conflict check

`wiki/log.md` 继续只记录 wiki 自身操作，业务对象状态与历史放入 `wiki/ledgers/`，两者不混用。`experience` 保存可复用且有证据的经验，`source` 仍保存单次材料摘要，`synthesis` 仍保存跨源分析。代码探索与根因排查职责仍分别属于 `code-explore` 和 `trouble-grill`。

## Rationale

现有 typed 页面和 lint/index 机制可直接扩展，改动向后兼容：既有页面无需迁移，新建工作区增加两个目录，索引增加两个分组。检索仍使用现有 `rg` 与全文读取，只补齐候选筛选、当前状态、证据与冲突的回答契约，避免为简单目标引入额外运行依赖。

## Files

- `skills/wiki-data/SKILL.md`：补充经验/台账触发、核心边界与 query reference 加载。
- `skills/wiki-data/references/layout.md`：增加 `experiences/`、`ledgers/` 布局和初始化规则。
- `skills/wiki-data/references/page-types.md`：定义两类页面、元数据与模板。
- `skills/wiki-data/references/ingest.md`：增加经验总结与台账更新规则。
- `skills/wiki-data/references/query.md`：新增检索、全文核对和引用协议。
- `skills/wiki-data/references/lint.md`：同步新类型的必需 frontmatter 字段。
- `skills/wiki-data/scripts/lint_wiki.py`：识别新类型并生成对应索引分组。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：守卫经验、台账与检索契约。
- `skills/wiki-data/tests/test_lint_wiki.py`：覆盖新类型索引与既有 lint 兼容。
- `skills/wiki-data/agents/openai.yaml`：同步展示说明与默认提示。

## Validation

- `git apply --check --recount` 通过后再按 medium 风险门禁确认。
- 应用后运行 `python3 -m pytest skills/wiki-data/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style` 和 `git diff --check -- skills/wiki-data`。
- 检查既有工作区无需新目录也可通过 lint，新增页面可进入索引，正文无隐私信息。
