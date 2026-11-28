# Result

- target: skills/role-based-reviewer
- mode: update
- patch: 20260930-172942-skill-reviewer-role
- risk: medium
- status: applied
- applied-at: 2026-09-30T17:29:42+08:00

## Validation

- `git apply --check --recount`: pass
- `git apply --recount` + `git diff --check -- skills/role-based-reviewer`: pass
- `python3 -m pytest skills/role-based-reviewer/tests -q`: 6 passed
- `python3 -m pytest skills -q`（全仓契约）: 426 passed, 1 skipped
- privacy check: pass（无个人/凭据/内部 URL）
- mode check: pass（update 模式，未引入 examples/evals/experience）

## Notes

- 8 个文件落盘（+67/-66）：SKILL.md、role-vocabulary.md、constraints.md、brief-protocol.md、preload-protocol.md、tests 中 diag → skill；删除 references/roles/diag.md，新增 references/roles/skill.md（8 条带命中判据清单，🔴2 / 🟡4 / ⚪2）。
- 边界：SKILL.md/references 质量 → skill；scripts/ 代码缺陷 → engineer；契约测试对应缺口 → skill，通用可测性 → qa；存在价值 → product。skill 角色不启用运行态上下文。
- 默认角色不变（仍 engineer）；skill 需显式 roles= 或「目标主体就是 Agent Skill 质量」强信号。
- 历史 patch 20260930-172217-diag-role 保留未改（其 result.md 记录的 diag 已被本 patch 取代）。
- 与 proposal 无偏差。未 commit、未 push（按协议不自动提交）。
