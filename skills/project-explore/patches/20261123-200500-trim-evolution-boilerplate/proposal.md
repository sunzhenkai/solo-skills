# 精简文末「经验回灌」样板为紧凑指针

- target: skills/project-explore
- mode: update
- patch: 20261123-200500-trim-evolution-boilerplate
- risk: low
- status: proposed

## Intent

对齐 AGENTS.md「各 skill 正文不复制自进化样板」原则，将文末 7 行「经验回灌」压缩为 2 句紧凑声明，同时保留运行时只读与显式进化契约。

## Conflict check

none

## Rationale

减少与 skill-upgrader 重复的样板表述，同时不破坏现有契约测试。

## Files

- `skills/project-explore/SKILL.md`：压缩「经验回灌」段落为紧凑指针

## Validation

- `git apply --check --recount skills/project-explore/patches/20261123-200500-trim-evolution-boilerplate/change.patch`
- `python3 -m unittest discover -s skills/project-explore/tests -p 'test_*.py'`
- `make check-style && make check-names`
