# confirm-destructive-ops

- target: skills/repo-manager
- mode: update
- patch: 20261124-234800-confirm-destructive-ops
- risk: low
- status: applied

## Intent

将未确认禁令从 --force push 扩展至 grepom prune --apply 与 grepom pull --force，并同步 gate_lines.txt。

## Conflict check

none
