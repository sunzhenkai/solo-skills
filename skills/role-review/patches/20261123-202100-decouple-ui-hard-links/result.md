# Result

- target: skills/role-based-reviewer
- mode: update
- patch: 20261123-202100-decouple-ui-hard-links
- risk: medium
- status: applied
- applied-at: 2026-11-23T20:11:25+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m unittest discover -s skills/role-based-reviewer/tests -p 'test_*.py'` -> OK
- privacy check: pass
- mode check: pass

## Notes

none
