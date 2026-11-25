# Result

- target: skills/session-wrap
- mode: update
- patch: 20261125-100000-release-deploy-signal-check
- risk: medium
- status: applied
- applied-at: 2026-11-25T10:01:43+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check -- skills/session-wrap README.md`: pass
- target tests: `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v` -> 12 tests OK
- repo tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v` -> 21 tests OK (1 skipped: 需要 openspec CLI)
- `make check-style`: pass (0 warnings; `SKILL.md` 6644 B)
- `make check-names`: pass
- privacy check: pass
- mode check: pass

## Notes

`README.md` 的 `session-wrap` 一行简介随本次同步更新（属仓级文档，不含在本 skill 的 `change.patch` 内）。
