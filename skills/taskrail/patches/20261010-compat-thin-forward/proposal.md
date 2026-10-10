# Proposal：旧 skill 轻清理（兼容转发）

## Intent

第二刀轻清理：旧入口只留转发，协议单真源。

## 变更

- `task-wizard` / `task-goal` / `task-delivery`：`SKILL.md` 收成兼容转发
- `task-wizard/references/external-precedent.md` → 薄引用 taskrail
- `task-goal/references/quality-profile.md` → 薄引用 task-confirm
- `task-delivery/references/loop-protocol.md` 标历史归档；链接改指 task-confirm
- 契约测试改写为转发断言；taskflow 同步锁改核 task-confirm / approve

## 保留

- `task-goal`：`suspension.md`、state 脚本（兼容资产）
- 目录不删（留给以后硬删除刀）

## Validation

task* 族 pytest 全绿；全仓 `skills` pytest 绿。
