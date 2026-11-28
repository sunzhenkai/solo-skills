---
id: 20261128-181200-worktree-node-deps-guidance
skill: taskflow
mode: update
status: applied
applied_at: 2026-11-28T18:13:00+08:00
---

# Result: taskflow patch applied

## Applied Files
- `skills/taskflow/references/worktree.md`
- `skills/taskflow/tests/test_taskflow_contract.py`

## Verification
- `git apply --check --recount`: passed
- `git apply --recount`: passed
- `git diff --check -- skills/taskflow`: passed
- `python3 -m unittest discover -s skills/taskflow/tests`: Ran 65 tests, OK
- `python3 -m unittest discover -s tests`: Ran 22 tests, OK (skipped=1)
- `make check-names`: passed (0 denylist matches)
- `make check-style`: passed
