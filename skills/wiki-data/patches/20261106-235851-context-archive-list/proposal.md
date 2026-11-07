# 上下文摄入先列归档清单

- target: skills/wiki-data
- mode: update
- patch: 20261106-235851-context-archive-list
- risk: medium
- status: proposed

## Intent

让 `ingest` 在用户要求从当前对话或上下文归档时，自动提取知识、主题、经验、踩坑和值得记录的操作信息；写盘前先向用户展示包含类型、目标页面与证据的归档列表，再严格按列表执行摄入。保留既有范围确认、隐私、来源追溯和复杂变更确认门禁，不新增页面类型、脚本或依赖。

## Conflict check

现有输入已包含对话结论，但没有自动提取范围与归档列表契约。本改动复用既有 `entity` / `concept` / `experience` / `ledger` 等类型，与文件摄入、`trouble-grill` 归档及其他 Skill 职责无冲突。

## Rationale

把候选提取与写入计划合并为可检查的归档列表，可减少上下文信息漏记和无计划写页；列表中的类型、目标与证据可直接由既有搜索、typed 页面和来源约束验证。

## Files

- `skills/wiki-data/references/ingest.md`：增加上下文自动提取类别、归档列表格式与先列表后写入的顺序。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：增加上下文提取和归档列表的文本契约测试。

## Validation

- 在仓库根运行 `git apply --check --recount`，通过后按 medium 风险门禁确认。
- 应用后运行 `python3 -m pytest skills/wiki-data/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style` 和 `git diff --check -- skills/wiki-data`。
- 核对实际 diff 仅包含 proposal 声明的生产文件，且无隐私信息。
