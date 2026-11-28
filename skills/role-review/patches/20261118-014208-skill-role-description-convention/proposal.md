# skill 角色的 description 判据对齐仓库约定

- target: skills/role-based-reviewer
- mode: update
- patch: 20261118-014208-skill-role-description-convention
- risk: medium
- status: proposed

## Intent

`roles=skill` 评审 description 时按正向 WHAT + WHEN 判定（关键词前置、每个真分支一个触发词、边界放正文），不再把「缺何时不用」当 🔴；写明与 `agent-docs-writer` review 路径的级别对应；下游建议从仓内不存在的 `skill-creator` 改为 `agent-docs-writer`。非目标：其余检查清单、三道门与输出骨架不变。

## Conflict check

原判据与 AGENTS.md「description 只写正向 WHAT + WHEN，不写何时不用」及 `agent-docs-writer/references/skill-authoring.md` 相反，会把合规 skill 报成 Blocker。本改动消除冲突。

## Rationale

同一类评审在仓内有两处入口，判据必须一致；级别对应关系让两边的结论可以互相引用。

## Files

- skills/role-based-reviewer/references/roles/skill.md：级别对应、清单第 1 条、下游建议。
- skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py：新增守卫断言。

## Validation

- `python3 -m pytest skills/role-based-reviewer/tests -q`
- 全量测试与 `make check-style`
