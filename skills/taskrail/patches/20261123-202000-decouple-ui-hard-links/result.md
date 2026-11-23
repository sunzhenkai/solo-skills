# Result

- target: skills/taskrail
- mode: update
- patch: 20261123-202000-decouple-ui-hard-links
- risk: medium
- status: applied
- applied-at: 2026-11-23T20:11:25+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'` -> OK (skipped=2)
- privacy check: pass
- mode check: pass

## Notes

none
