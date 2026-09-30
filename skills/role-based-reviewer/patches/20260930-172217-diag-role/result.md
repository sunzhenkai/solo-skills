# Result

- target: skills/role-based-reviewer
- mode: update
- patch: 20260930-172217-diag-role
- risk: medium
- status: applied
- applied-at: 2026-09-30T17:22:17+08:00

## Validation

- `git apply --check --recount`: pass
- `git apply --recount` + `git diff --check -- skills/role-based-reviewer`: pass
- `python3 -m pytest skills/role-based-reviewer/tests -q`: 6 passed
- `python3 -m pytest skills -q`（全仓契约）: 426 passed, 1 skipped
- privacy check: pass（无个人/凭据/内部 URL）
- mode check: pass（update 模式，未引入 examples/evals/experience）

## Notes

- 7 个文件落盘（+68/-13）：SKILL.md（description / 合法值 / 推断信号）、role-vocabulary.md（矩阵行）、constraints.md（命令边界列 + 2 条 redirect）、brief-protocol.md（枚举 + 运行态字段）、preload-protocol.md（运行态角色）、tests（枚举 + THICKENED_FULL 第三批）、新增 references/roles/diag.md（6 条带命中判据清单，🔴1 / 🟡4 / ⚪1）。
- 边界：定位归 diag，已定根因的修复归 engineer；应用内根因归 diag，部署/资源/集群侧归 sre。
- 默认角色不变（仍 engineer）；diag 需显式 roles= 或「目标主体就是根因排查」强信号。
- 与 proposal 无偏差。未 commit、未 push（按协议不自动提交）。
