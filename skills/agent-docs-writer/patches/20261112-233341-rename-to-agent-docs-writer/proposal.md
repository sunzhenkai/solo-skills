# 重命名 agent-wizard 为 agent-docs-writer

- target: skills/agent-wizard
- mode: update
- patch: 20261112-233341-rename-to-agent-docs-writer
- risk: medium
- status: proposed

## Intent

将 skill 目录 skills/agent-wizard 重命名为 skills/agent-docs-writer，同步更新 frontmatter id/name、正文自称、evals 的 skill 字段、契约测试的文件名与断言。非目标：行为、流程、门禁、description 触发词、references 内容不变。

## Conflict check

与 skill-upgrader 的职责边界不变（本 skill 仍只管从零创建与只读评审，修改走 patches/ 审计）。仓内 grep 确认除本 skill 目录与 README 清单外无其他 agent-wizard 引用；根目录 .claude/skills 为整目录软链，随重命名自动生效，无悬空引用。

## Rationale

原名 wizard 暗示交互式向导，与本 skill「撰写与评审 agent 文档」的实际职责不符；新名直接表达用途。改名已经用户确认；可验证性由契约测试的 frontmatter 断言守卫（同轮更新，不新增测试文件）。

## Files

- skills/agent-wizard/SKILL.md → skills/agent-docs-writer/SKILL.md（frontmatter id/name、标题、正文自称）
- skills/agent-wizard/evals/cases.yaml → skills/agent-docs-writer/evals/cases.yaml（skill 字段）
- skills/agent-wizard/tests/test_agent_wizard_contract.py → skills/agent-docs-writer/tests/test_agent_docs_writer_contract.py（文件名、docstring、frontmatter 正则）
- README.md（仓库级清单条目；受 patch 协议限制不进入 change.patch，在 patch 之外同轮更新并记入 result.md）

## Validation

- 应用前：git apply --check --recount
- 应用后：python3 -m pytest skills -q；make check-names；make check-style
