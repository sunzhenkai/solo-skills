# 已下线 skill 的指针不再指向源仓 archive

- target: skills/wiki-data
- mode: update
- patch: 20261118-014611-retired-skill-pointer
- risk: low
- status: proposed

## Intent

非目标里「`project-spec-mirror` 已归档在 `archive/skills/`，需要时从那里恢复」改为「原 `project-spec-mirror` 已下线；项目现行说明交给 `project-atlas`」。非目标：其他非目标与阶段不变。

## Conflict check

none。安装副本里没有源仓的 `archive/`，原句在运行时无法执行。

## Rationale

指针改为当前承担该职责的 skill，安装后仍可执行。

## Files

- skills/wiki-data/SKILL.md：非目标第 2 条。
- skills/wiki-data/tests/test_wiki_data_contract.py：断言改锚新句。

## Validation

- `python3 -m pytest skills/wiki-data/tests -q`
