# 知识置信度、时效与踩坑复用闭环

- target: skills/wiki-data
- mode: update
- patch: 20261107-001422-confidence-freshness-reuse
- risk: medium
- status: proposed

## Intent

让大型项目、重复工作和业务知识在保存后能被安全复用：所有 typed 页面用 `confidence` 表达证据强度，用 `last_verified` / `review_after` 表达核实与复审时间；经验页补全触发信号、预防处理与验证方式；相似任务执行前先检索经验，回答时同时保留出处、置信度、适用范围和时效。临时、冲突、错误或过期信息保留历史与状态，但不作为当前事实或已验证建议输出。保持纯 Markdown、现有 typed 页面和 Python 标准库实现，不引入服务、数据库或数值概率。

## Conflict check

沿用 `code-explore` 已有的 `confidence: high | medium | low` 词表。`confidence` 只表示证据强度，与 `status` 的生命周期含义和 `review_after` 的时效含义分离；`ledger.status` 继续沿用业务词表。既有 `experience.status` 的 `draft | validated | deprecated` 保持不变。旧页面缺少新元数据时由 lint 指出，修复只补元数据，不改写历史来源。

## Rationale

单页默认置信度配合主张级例外，能以较低记录成本覆盖普通知识，同时避免高置信度页面掩盖个别低置信度主张。写入日期、证据强度与复审时间分离，可防止把“最近编辑”误当“仍然有效”。执行前检索与经验页的预防/验证章节把“保存踩坑”推进到“下次执行前可用”。lint 与索引提供确定性检查和大库候选筛选，契约测试及临时工作区端到端检查可验证行为。

## Files

- `skills/wiki-data/SKILL.md`：增加相似任务前检索触发及可信度核心不变量。
- `skills/wiki-data/references/layout.md`：初始化写作规则加入置信度与时效。
- `skills/wiki-data/references/page-types.md`：定义置信度、核实/复审字段、主张级标注和防复发经验模板。
- `skills/wiki-data/references/ingest.md`：写入时定级、纠正与失效处理、经验验证门禁。
- `skills/wiki-data/references/query.md`：相似任务预检及按证据、状态、时效回答。
- `skills/wiki-data/references/lint.md`：记录新增检查码与修复语义。
- `skills/wiki-data/scripts/lint_wiki.py`：校验置信度/日期/经验验证元数据，提示复审逾期，并扩展索引。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：守卫定级、时效、纠正和执行前复用契约。
- `skills/wiki-data/tests/test_lint_wiki.py`：覆盖元数据错误、复审逾期、索引与有效页面。
- `skills/wiki-data/agents/openai.yaml`：同步默认提示中的可信度与预检入口。

## Validation

- 基于当前 worktree 已有未提交改动生成增量 unified diff，运行 `git apply --check --recount`，按 medium 风险门禁展示并等待确认。
- 应用后运行 `python3 -m pytest skills/wiki-data/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style` 和 `git diff --check -- skills/wiki-data`。
- 用临时工作区覆盖高/中/低置信度、逾期复审、draft/validated/deprecated 经验和相似任务查询输出；核对实际 diff 仅含声明文件且无隐私信息。
