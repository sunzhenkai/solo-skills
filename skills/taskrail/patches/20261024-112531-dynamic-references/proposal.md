# Proposal: dynamic references and workspace task tree

- mode: update
- risk: high
- scope: `skills/taskrail/` production files, tests and evals only
- approval: user approved the reviewed multi-skill remediation plan with “落地吧”.

## Intent

Replace the fixed skip/full lifecycle with evidence-driven, re-enterable references. Make workspace the planning root, add automatic slice/subtask planning and recovery, separate hot recovery state from cold history, and make final verification independent of OpenSpec driver archival.

## Compatibility

Preserve the taskrail/taskflow public entry points, existing intent confirmation, human/goal confirmation policy, UI delivery gates and archived task layout. Legacy task metadata is reconciled from artifacts instead of being mapped to two fixed pipelines.

## Validation

Run the complete taskrail unittest suite, deterministic workspace/state tests, reference existence checks and diff checks. No production file is changed before `change.patch` passes `git apply --check`.
