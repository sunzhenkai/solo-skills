# 完成 project-explore 目录迁移

- target: skills/project-explore
- mode: update
- patch: 20261113-215125-complete-project-explore-rename
- risk: high
- status: proposed

## Intent

将首个内容 patch 未覆盖的未修改配套、测试门禁和历史 patches 从 skills/code-explore 移到 skills/project-explore，完成用户已批准的目录改名；文件内容保持不变。

## Conflict check

首个 patch 由 no-index 内容 diff 生成，只移动了有内容变化的文件。该补充 patch 只修正迁移完整性，不改变行为，不改写历史 patch 内容。

## Rationale

目标 Skill 必须自包含，examples、experience、evals 说明、测试门禁与审计历史应随目录一起迁移。使用临时 Git 仓机械生成 rename diff，可校验且不手写 hunk。

## Files

- skills/code-explore/ 下剩余文件 → skills/project-explore/ 对应路径，仅改名。

## Validation

- 在临时 Git 仓执行 git mv 并生成 rename diff。
- git apply --check --recount。
- 用户已批准整体改名，风险门禁已通过。
- 应用后运行 git diff --check 和 project-explore 测试。
- 确认旧目录消失、配套齐全、历史 patch 内容未改。
