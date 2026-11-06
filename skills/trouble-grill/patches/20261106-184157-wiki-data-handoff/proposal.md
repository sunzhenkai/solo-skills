# 增加 wiki-data 可选归档出口

- target: skills/trouble-grill
- mode: update
- patch: 20261106-184157-wiki-data-handoff
- risk: medium
- status: proposed

## Intent

用户明确要求把排查结果沉淀到知识 wiki 时，将既有持久化记录交给 `wiki-data ingest`。默认台账与工作区存档路径保持不变，未安装或未调用 `wiki-data` 时仍可独立完成排查。

## Conflict check

不改变锚点、假设板、四道门禁、证据升级或既有落盘优先级。归档只消费已分级记录，不把 weak / guess 固化为根因。

## Rationale

在收口阶段复用 `wiki-data` 的知识摄入能力即可形成轻量联动，无需共享状态、自动调用或新增运行依赖。

## Files

- `skills/trouble-grill/SKILL.md`：增加显式归档出口与独立使用约定。
- `skills/trouble-grill/tests/test_trouble_grill_contract.py`：守护可选归档、证据保留和默认独立落盘行为。

## Validation

- `git apply --check --recount` 通过后应用。
- 目标测试与全仓 `python3 -m pytest skills -q`。
- `make check-names`、`make check-style`、`git diff --check`。
