# 回指 agent-docs-writer，允许跨 Skill 问题各写一份 patch

- target: skills/skill-upgrader
- mode: update
- patch: 20261118-014403-cross-skill-boundaries
- risk: medium
- status: proposed

## Intent

1. 关系表加 `agent-docs-writer` 一行；「从零创建 Skill」的停止分支与 evolve 非目标都点名交给 `agent-docs-writer`。
2. 「一次会话只处理一个目标 Skill」改为「一轮 patch 只解决一个内聚问题、一种模式」；同一问题跨多个 Skill 时每个 Skill 各建 patch 目录，proposal 互相注明配套 patch。

非目标：模式门禁、先 patch 后应用、`gate_lines.txt` 锁定的门禁句、evolve 的「一次会话最多推进一个目标 Skill 的一轮进化」均不变。

## Conflict check

`agent-docs-writer` 已声明「已有 Skill 修改交给 skill-upgrader」，本 skill 此前未回指。原「一个目标 Skill」规则与仓库实际做法冲突：跨 Skill 边界修复（如提交 ea49287、3096cc4）都在一次改动里给多个 Skill 各写 patch。

## Rationale

修 Skill 之间的关联天然涉及多个 Skill；按问题而不是按 Skill 划分一轮 patch，审计粒度不变（仍是一 Skill 一 patch 目录），只去掉不必要的会话限制。

## Files

- skills/skill-upgrader/SKILL.md：关系表、模式判定第 5 条、会话范围句。
- skills/skill-upgrader/references/evolve.md：非目标一句。
- skills/skill-upgrader/tests/test_skill_upgrader_contract.py：新增两条守卫断言。

## Validation

- `python3 -m pytest skills/skill-upgrader/tests -q`（含 gate lock）
