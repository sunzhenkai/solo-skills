# Result

- target: skills/agent-docs
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: applied
- applied-at: 2026-11-28T18:54:00+08:00

## Validation

- `python3 -m unittest discover -s skills/agent-docs/tests -p 'test_*.py'` -> 17 passed
- `python3 -m unittest discover -s tests -p 'test_*.py'` -> 22 passed (skipped=1)
- `make check-names && make check-style` -> pass

## Notes

none
