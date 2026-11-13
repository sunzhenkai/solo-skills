# 明确 wiki-data 与 Project Atlas 的边界和联动

- target: skills/wiki-data
- mode: update
- patch: 20261113-190313-wiki-atlas-boundary
- risk: medium
- status: proposed

## Intent

把当前项目的架构、业务流程和规则现行说明归给 `project-atlas`；wiki 保留决策背景、经验、台账与其他可累积知识。摄入混合材料时拆分归属，查询时组合现状与背景，项目实体页可用相对 Markdown 链接导航到已有 Atlas。不复制 Atlas 正文，不自动写另一个工作区，不改变现有来源和确认门禁。

## Conflict check

保留 `code-explore`、`trouble-grill` 和已归档 `project-spec-mirror` 的既有边界。Atlas 链接只作导航，不替代 wiki 的 `sources`；query 默认只读。现有 lint 已能检查指向工作区外现存文件的相对 Markdown 链接，无需修改脚本。

## Rationale

该更新用内容归属和单份正文消除两个 Skill 的重叠，同时利用现有文件格式与 lint 能力完成可追溯联动。文本契约和临时工作区可验证转交、查询及链接行为。

## Files

- `skills/wiki-data/SKILL.md`：声明 Atlas 边界与联动总原则。
- `skills/wiki-data/references/ingest.md`：拆分混合材料并约定 Atlas 导航链接。
- `skills/wiki-data/references/query.md`：组合查询、只读回退与冲突处理。
- `skills/wiki-data/references/page-types.md`：约定项目实体页的可选 Atlas 入口。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：守卫边界与联动文本契约。
- `skills/wiki-data/tests/test_lint_wiki.py`：验证指向 Atlas 的相对链接可通过 lint。

## Validation

- `git apply --check --recount` 校验补丁。
- 应用后运行 `git diff --check -- skills/wiki-data`。
- 运行 `python3 -m pytest skills/wiki-data/tests -q`。
- 检查 frontmatter、引用路径、公开仓隐私与 mode=update 范围。
