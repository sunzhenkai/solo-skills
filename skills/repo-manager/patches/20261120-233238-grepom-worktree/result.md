# Result

- target: skills/repo-manager
- mode: update
- patch: 20261120-233238-grepom-worktree
- risk: low
- status: applied
- applied-at: 2026-11-20T23:33:44+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- `make check-names`: pass
- `make check-style`: pass（0 条告警）
- `python3 -m pytest skills/repo-manager/tests -q`: 1 passed
- privacy check: pass
- mode check: pass

## Notes

只补充 linked worktree 下的报错分流经验，不改命令默认行为；未 commit、push。
