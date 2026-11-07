# 自动提取有用知识并制定保存计划

- target: skills/wiki-data
- mode: update
- patch: 20261107-091316-useful-knowledge-plan
- risk: medium
- status: proposed

## Intent

明确上下文摄入会自动完成候选提取与保存计划，但仍遵守既有确认门禁，不在普通对话中自动写盘。以 `purpose.md` 和后续复用价值筛选信息，保存计划同时列出拟保存项与不纳入项及理由；补全决策、状态、对比、综合和问答等候选到现有 typed 页面的映射，不新增页面类型、目录或依赖。

## Conflict check

现有流程已有自动提取与归档列表，本改动只补足价值筛选、计划内容和候选类别。`source` 仍保存单次来源摘要，`experience` 保存可复用经验，`ledger` 保存对象状态与历史，`comparison` / `synthesis` / `query` 各承担既有职责；范围确认、隐私、证据和写盘门禁保持不变。

## Rationale

“提取全部信息”容易把重复过程和一次性细节搬进 wiki。用保存价值与不纳入理由约束候选，再按现有类型规划新建、更新或合并，可减少噪声与重复页面；契约测试可直接守卫自动提取不等于自动写盘、保存计划包含取舍以及知识类别完整。

## Files

- `skills/wiki-data/references/ingest.md`：明确自动行为边界、价值筛选、知识类别和保存计划字段。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：增加上述流程的文本契约断言。

## Validation

- 在仓库根运行 `git apply --check --recount`，通过后按 medium 风险门禁确认。
- 应用后运行 `python3 -m pytest skills/wiki-data/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style` 和 `git diff --check -- skills/wiki-data`。
- 核对实际 diff 仅包含 proposal 声明的生产文件，且无隐私信息。
