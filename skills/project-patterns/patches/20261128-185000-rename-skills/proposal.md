# 改名为 project-patterns

- target: skills/project-patterns
- mode: update
- patch: 20261128-185000-rename-skills
- risk: medium
- status: proposed

## Intent

将 project-design-patterns 改名为 project-patterns，version 升至 1.3.0，同步 /skill.md 声明约定并修复 test_agent_api_ops_contract.py 过时断言。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/project-patterns/SKILL.md`
- `skills/project-patterns/patches/20261123-142058-merge-agent-api-ops/change.patch`
- `skills/project-patterns/patches/20261123-142058-merge-agent-api-ops/proposal.md`
- `skills/project-patterns/patches/20261123-142058-merge-agent-api-ops/result.md`
- `skills/project-patterns/patches/20261126-142600-add-model-provider-pattern/change.patch`
- `skills/project-patterns/patches/20261126-142600-add-model-provider-pattern/proposal.md`
- `skills/project-patterns/patches/20261126-142600-add-model-provider-pattern/result.md`
- `skills/project-patterns/references/agent-api-access.md`
- `skills/project-patterns/references/agent-api-ops.md`
- `skills/project-patterns/references/model-provider-impl-prompt.md`
- `skills/project-patterns/references/model-provider-management.md`
- `skills/project-patterns/tests/test_agent_api_ops_contract.py`
- `skills/project-patterns/tests/test_project_patterns_contract.py`

## Validation

- `python3 -m unittest discover -s skills/project-patterns/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
