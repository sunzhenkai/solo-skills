# Result

- target: skills/taskrail
- mode: update
- patch: 20261107-081107-template-compat
- risk: low
- status: failed
- applied-at: 2026-11-07T08:12:12+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/taskrail/tests -q` — 139 passed, 2 skipped, 2 subtests passed
- repository tests: `python3 -m pytest skills -q` — 1 failed, 521 passed, 3 skipped, 2 subtests passed
- repository checks: `make check-names` and `make check-style` — pass, 0 warnings
- privacy check: pass
- mode check: pass

## Notes

taskflow 的模板提取正则要求 `## TASK.md` 后直接跟代码块；上一 patch 的说明文字位于二者之间，导致未匹配。下一 patch 仅移动说明位置。
