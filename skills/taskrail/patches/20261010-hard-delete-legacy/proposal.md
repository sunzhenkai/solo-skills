# Proposal：硬删除旧 task* 目录

## Intent

删除 `task-wizard` / `task-goal` / `task-delivery` 目录；资产迁入 `task-confirm`。

## 迁移

- `suspension.md` / `state-file.md` / `state-machine.md` / `scripts/goal_transition.py` → `task-confirm`
- 族契约测试 → `taskrail/tests/test_task_family_contract.py`
- 生产稿链接改指 taskrail / task-confirm

## 删除

`skills/task-wizard/`、`skills/task-goal/`、`skills/task-delivery/`（含历史 patches/evolutions；审计痕迹已在本 patch 与重组 patch 记录）。
