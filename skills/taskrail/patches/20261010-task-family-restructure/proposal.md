# Proposal：task* 族重组为 taskrail 轨道

## Intent

按最终整理方案落地：脊柱 `taskrail`、确认 `task-confirm`、收紧 `task-explore`（approve/expand + TASK.md phase）、`taskflow` 衔接；旧入口兼容转发。

## 变更摘要

- 新增 `taskrail`（契约 + wizard 阶段 + 外部参照）
- 新增 `task-confirm`（human/goal 确认与审阅；质量画像）
- `task-explore`：`decide`/`plan-review` → `approve`；`split` → `expand` 别名；目录与 phase 字段
- `task-wizard` / `task-goal` / `task-delivery`：兼容横幅
- README / AGENTS / 族契约测试更新

## Validation

`python3 -m pytest skills/taskrail/tests skills/task-confirm/tests skills/task-explore/tests skills/task-wizard/tests skills/task-goal/tests skills/task-delivery/tests skills/taskflow/tests -q` → 250 passed
