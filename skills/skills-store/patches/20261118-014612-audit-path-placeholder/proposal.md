# 审计脚本路径改用 skill 安装目录占位

- target: skills/skills-store
- mode: update
- patch: 20261118-014612-audit-path-placeholder
- risk: low
- status: proposed

## Intent

审计脚本定位从 `BASH_SOURCE` 推算改为 `<this-skill>/scripts/audit-skill.sh`，执行前替换成实际安装路径。非目标：审计流程、退出码与豁免规则不变。

## Conflict check

none。

## Rationale

agent 在交互 shell 里直接执行该片段时，`${BASH_SOURCE[0]:-$0}` 解析为 shell 自身，得到错误目录；原注释里的 `.cursor/skills/...` 也只覆盖一种 agent。仓内其他 skill 都用 `<this-skill>` 类占位。

## Files

- skills/skills-store/SKILL.md：审计脚本定位段。
- skills/skills-store/tests/test_skills_store_contract.py：新增守卫断言。

## Validation

- `python3 -m pytest skills/skills-store/tests -q`
