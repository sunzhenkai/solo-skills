# 明确 Project Atlas 与 wiki-data 的边界和联动

- target: skills/project-atlas
- mode: update
- patch: 20261113-190627-atlas-wiki-boundary
- risk: medium
- status: proposed

## Intent

Atlas 只维护代码核实后的当前系统事实；决策背景、备选方案、经验、台账和跨项目知识归 `wiki-data`。混合任务先完成 Atlas，再列出需要 wiki-data 摄入或复核的主题。Atlas 不自动写 wiki、不复制其正文，页面与静态站点不依赖 wiki 外链。

## Conflict check

保留 `code-explore` 的一次性问答边界、Archify 职责、源码映射和确认门禁。现有链接校验拒绝越出 Atlas 根目录，因此本轮不增加 wiki 外链，也不修改 CLI、frontmatter 或发布格式。

## Rationale

按当前事实与知识上下文拆分正文可消除重复；交付回执中的 wiki 候选提供可执行联动，同时保持 Atlas 静态站点独立。既有契约测试可守卫该行为，无需新增运行时依赖。

## Files

- `skills/project-atlas/SKILL.md`：明确内容归属、联动顺序与站点边界。
- `skills/project-atlas/references/maintenance.md`：规定代码复核时的 wiki 候选与冲突交接。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：守卫分工和只读交接契约。

## Validation

- `git apply --check --recount` 校验补丁。
- 应用后运行 `git diff --check -- skills/project-atlas`。
- 运行 `python3 -m pytest skills/project-atlas/tests -q`。
- 检查 frontmatter、引用路径、公开仓隐私与 mode=update 范围。
