# 改名为 agent-docs

- target: skills/agent-docs
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

将 agent-docs-writer 改名为 agent-docs（对齐 agent-roster），并同步内部对 role-review 的引用。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/agent-docs/SKILL.md`
- `skills/agent-docs/evals/cases.yaml`
- `skills/agent-docs/patches/20261112-233341-rename-to-agent-docs-writer/change.patch`
- `skills/agent-docs/patches/20261112-233341-rename-to-agent-docs-writer/proposal.md`
- `skills/agent-docs/patches/20261112-233341-rename-to-agent-docs-writer/result.md`
- `skills/agent-docs/patches/20261112-233516-fix-self-reference-after-rename/change.patch`
- `skills/agent-docs/patches/20261112-233516-fix-self-reference-after-rename/proposal.md`
- `skills/agent-docs/patches/20261112-233516-fix-self-reference-after-rename/result.md`
- `skills/agent-docs/patches/20261118-014209-review-severity-mapping/change.patch`
- `skills/agent-docs/patches/20261118-014209-review-severity-mapping/proposal.md`
- `skills/agent-docs/patches/20261118-014209-review-severity-mapping/result.md`
- `skills/agent-docs/patches/20261124-234800-review-interaction-gates/change.patch`
- `skills/agent-docs/patches/20261124-234800-review-interaction-gates/proposal.md`
- `skills/agent-docs/patches/20261124-234800-review-interaction-gates/result.md`
- `skills/agent-docs/references/agents-md.md`
- `skills/agent-docs/references/review.md`
- `skills/agent-docs/references/skill-authoring.md`
- `skills/agent-docs/tests/test_agent_docs_contract.py`

## Validation

- `python3 -m unittest discover -s skills/agent-docs/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
