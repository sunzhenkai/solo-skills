# 修正改名后正文残留的旧自称

- target: skills/agent-docs-writer
- mode: update
- patch: 20261112-233516-fix-self-reference-after-rename
- risk: low
- status: proposed

## Intent

20261112-233341-rename-to-agent-docs-writer 重命名后，SKILL.md 第 19 行仍自称 `agent-wizard`，本 patch 将其改为 `agent-docs-writer`。非目标：其他内容不变。

## Conflict check

none；仅同步上一 patch 遗漏的一处自称。

## Rationale

skill 正文自称与 frontmatter id/name 不一致会让用户与 agent 困惑；契约测试暂未守卫该行，同轮不新增测试（一次最小修复）。

## Files

- skills/agent-docs-writer/SKILL.md（第 19 行自称）

## Validation

- 应用前：git apply --check --recount
- 应用后：grep 确认 skills/ 与 README.md 中无 agent-wizard 残留（patches/ 历史记录除外）；python3 -m pytest skills -q
