# Result

- target: skills/taskrail
- mode: update
- patch: 20261127-164500-rename-way-to-cr
- risk: low
- status: applied
- applied-at: 2026-11-27T16:45:00+08:00

## Validation

- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'` -> 187 ran, OK (3 skipped)
