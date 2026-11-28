# Result

- target: skills/role-based-reviewer
- mode: update
- patch: 20261118-014208-skill-role-description-convention
- risk: medium
- status: applied
- applied-at: 2026-11-18T01:42:08+08:00

## Validation

- `git apply --check --recount --reverse`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/role-based-reviewer/tests skills/agent-docs-writer/tests -q`，29 passed
- privacy check: pass
- mode check: pass

## Notes

- 用户在评审后明确批准本批改动（跨 skill 漂移修复第一批）。
- patch 由任务 worktree 中的改动机械导出，以 `--reverse` 校验与生产改动一致。
- 配套改动在 `agent-docs-writer` 的 `20261118-014209-review-severity-mapping`。
