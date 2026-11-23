# 精简 SKILL.md 重复阶段段落，留出 8KB 演进裕度

- target: skills/wiki-data
- mode: update
- patch: 20261123-200300-trim-skill-md
- risk: low
- status: proposed

## Intent

合并「非目标」中重叠条目并移除文末与「阶段」「加载」表重复的 4 个空壳小节，在不改变任何规则与契约的前提下为 SKILL.md 留出演进空间。

## Conflict check

none

## Rationale

原 SKILL.md 达 8091B，距 8192B 红线仅余 101B，任何小改都会触发 check-style 告警。

## Files

- `skills/wiki-data/SKILL.md`：压缩「非目标」与文末重复阶段小节，保留全部阶段路由与确认门禁

## Validation

- `git apply --check --recount skills/wiki-data/patches/20261123-200300-trim-skill-md/change.patch`
- `python3 -m unittest discover -s skills/wiki-data/tests -p 'test_*.py'`
- `make check-style && make check-names`
