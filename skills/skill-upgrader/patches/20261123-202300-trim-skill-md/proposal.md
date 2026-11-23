# 精简 SKILL.md 重复说明，留出 8KB 演进裕度

- target: skills/skill-upgrader
- mode: update
- patch: 20261123-202300-trim-skill-md
- risk: low
- status: proposed

## Intent

压缩「与相关 Skill 的关系」「公开性与隐私」和文末收尾指针的重复表述，不动任何门禁与锁行，为 SKILL.md 留出 8KB 缓冲。

## Conflict check

none

## Rationale

原 SKILL.md 达 8011B，接近 8192B 告警线；精简后全部契约与 gate_lines 断言完整保留。

## Files

- `skills/skill-upgrader/SKILL.md`：压缩非门禁重复表述

## Validation

- `git apply --check --recount skills/skill-upgrader/patches/20261123-202300-trim-skill-md/change.patch`
- `python3 -m unittest discover -s skills/skill-upgrader/tests -p 'test_*.py'`
- `make check-style && make check-names`
