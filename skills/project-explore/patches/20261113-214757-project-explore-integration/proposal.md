# project-explore 改名与只读持久化路由

- target: skills/code-explore → skills/project-explore
- mode: update
- patch: 20261113-214757-project-explore-integration
- risk: high
- status: proposed

## Intent

将 code-explore 改名为 project-explore，定位为项目理解与代码取证入口。保留 ask/explore 的只读问答和调查能力；archive/ingest/project 改为持久化路由，不再直接维护知识文档、摄入 wiki 或创建独立 project profile。当前系统说明交给 project-atlas，长期知识交给 wiki-data。

## Conflict check

现有 archive/ingest/project 与 project-atlas、wiki-data 形成多个写入方。本轮删除这些并行写入契约，保留只读、安全、证据、渐进披露和运行时只读门禁。其他 Skill 的有效引用在各自 patch 中同步更新，历史 patches 不改写。

## Rationale

用户已明确批准改名、收缩写入能力和三 Skill 集成方案。单一写入方可避免竞争真源；保留阶段名作为路由入口可降低调用迁移成本。契约测试与声明式 eval 可验证新边界。

## Files

- skills/code-explore/ → skills/project-explore/：目录、frontmatter 与 agent 配置改名。
- skills/project-explore/SKILL.md：项目理解定位、Atlas/wiki 读取顺序和只读路由。
- skills/project-explore/references/phases.md：保留 ask/explore，重写 archive/ingest/project 交接。
- skills/project-explore/tests/test_code_explore_contract.py：更新命名、路由和 Brief 契约。
- skills/project-explore/evals/cases.yaml：覆盖只读路由、Atlas 优先和混合归档顺序。
- skills/project-explore/agents/openai.yaml：更新展示名与调用名。

## Validation

- 对临时原文/改后副本机械生成 change.patch，不手写 hunk。
- git apply --check --recount。
- 用户已在会话中批准具体高风险改动，风险门禁已通过。
- git apply --recount 后运行 git diff --check。
- python3 -m pytest skills/project-explore/tests -q。
- 检查 frontmatter、引用路径、隐私及历史 patches 未变更。
