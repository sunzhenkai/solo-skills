# Proposal: workspace worktrees and execution adapters

- mode: update
- risk: high
- scope: `skills/taskflow/` production files, tests and evals only
- approval: user approved the reviewed multi-skill remediation plan with “落地吧”.

## Intent

Make git worktree isolation independent of OpenSpec, keep all OpenSpec artifacts in the workspace planning root, support multiple repositories per task, and add deterministic, idempotent worktree preparation with identity checks.

## Compatibility

Keep `{task}-driver` and rolling slices for OpenSpec execution. Direct execution uses the same worktree protocol without creating a driver. Existing handoff checks remain specific to OpenSpec execution.

## Validation

Run real temporary-git-repository integration tests for create/resume/collision/dirty-tree/no-remote behavior, the complete taskflow unittest suite and diff checks. No production file is changed before `change.patch` passes `git apply --check`.
