# 坑与排查模式：按现象可检索、可归纳的经验

- target: skills/wiki-data
- mode: update
- patch: 20261118-103520-pitfall-pattern-experience
- risk: medium
- status: proposed

## Intent

让排查中踩过的坑以可复用的方式沉淀：`experience` 增加可选 `kind: practice | pitfall | pattern`。`pitfall` 一个坑一页，带现象检索词 `symptoms` 与「误判与弯路」「最短判别」「复发记录」三节；`pattern` 由 organize 从至少两个坑归纳出跨系统的识别信号与先做的判别。ingest 规定同坑复发追加原页、未坐实根因保持 draft；query 在排查开始或卡住时按现象词检索，并把最短判别排在检查项第一位；lint 校验 `kind`、缺 `symptoms` 与模式实例不足，索引摘要附 `kind` 与现象词。

非目标：不新增页面类型或目录；不改既有 experience / ledger 的状态与置信度规则；不迁移任何既有知识库数据。

## Conflict check

none。`kind` 缺省为 `practice`，既有页面与索引输出不变；`kind` 与 `status`、`confidence`、归档字段正交。配套 patch：`skills/session-wrap/patches/20261118-103520-detour-review/`（收尾弯路复盘产出坑候选，交本 skill 摄入）、`skills/trouble-grill/patches/20261118-103520-symptom-pitfall-lookup/`（立锚点后按现象查坑，走本 skill 的 query 预检）。

## Rationale

原 experience 按「经验结论」组织，缺少排查时最有用的三样：按现象检索的入口、被推翻的误判、一锤定音的判别；也没有同坑复发与多坑归纳的规则，经验难以在相似但不相同的问题上复用。复用既有 experience 生命周期只加一个维度，查询预检无需多扫目录；lint 规则可确定性验证。

## Files

- skills/wiki-data/SKILL.md：query 阶段补「排查时按现象查坑」。
- skills/wiki-data/references/page-types.md：`kind` / `symptoms` 字段、「坑与排查模式」章节说明、pitfall / pattern 模板。
- skills/wiki-data/references/ingest.md：「排查记录与坑」——现象词检索、复发追加、字段落点、模式候选；完成标准补一条。
- skills/wiki-data/references/query.md：排查开始或卡住时按现象词预检；查坑的回答要点。
- skills/wiki-data/references/organize.md：「归纳排查模式」。
- skills/wiki-data/references/lint.md：新增 `kind_invalid`、`symptoms_missing`、`pattern_instances_insufficient`，索引摘要说明。
- skills/wiki-data/scripts/lint_wiki.py：对应检查与索引摘要（仅标准库）。
- skills/wiki-data/tests/test_lint_wiki.py、tests/test_wiki_data_contract.py：守卫断言。

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/wiki-data/tests -q`
- 全量 `python3 -m pytest skills tests -q`；`make check-style`、`make check-names`、`git diff --check`
