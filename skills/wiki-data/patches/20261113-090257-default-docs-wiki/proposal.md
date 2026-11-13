# 默认写入项目 docs/wiki

- target: skills/wiki-data
- mode: update
- patch: 20261113-090257-default-docs-wiki
- risk: medium
- status: proposed

## Intent

未显式指定工作区时，把项目知识 wiki 绑定到当前项目的 `docs/wiki`；`lint_wiki.py` 缺省读取同一路径。用户显式给出的 `WIKI_ROOT` 和 lint 位置参数继续覆盖默认值。

## Conflict check

保留现有布局、确认门禁和显式路径兼容，只改变未指定路径时的选择顺序，不影响已有工作区。

## Rationale

统一项目内文档落点，减少每次会话重新绑定路径的变动；CLI 与正文使用同一默认值，可用参数解析测试验证。

## Files

- `skills/wiki-data/SKILL.md`：默认绑定 `docs/wiki`。
- `skills/wiki-data/references/layout.md`：标明 canonical 项目落点。
- `skills/wiki-data/scripts/lint_wiki.py`：位置参数可选，默认 `docs/wiki`。
- `skills/wiki-data/tests/test_wiki_data_contract.py`：守卫路径约定与 CLI 默认值。

## Validation

- `git apply --check --recount`。
- `python3 -m pytest skills/wiki-data/tests -q`。
- 全仓测试、名称与风格检查。
