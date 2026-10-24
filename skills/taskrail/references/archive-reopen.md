# archive 与 reopen

原则：不覆盖、保留未结项、整树移动、INDEX 可重建。

## archive

- 完成归档：close 已完成、status done 后同轮把父任务整树移到 `tasks/archive/<yyyy-mm-dd>/<task-id>`；子任务留在 subtasks。
- 未完成关闭：只有用户明确放弃 / 关闭才执行，status archived；不能写成 done 或伪造成成功 SUMMARY。
- 搬之前核对未结子任务、未决、driver / worktree 现状和目标路径冲突。目标已存在则停，不覆盖。
- 步骤：写回热状态与 SUMMARY → 记录 archived 日期 → 原子移动整树 → `task_state.py rebuild-index <workspace>` → 确认新路径可读、旧路径不存在 → 清绑定。
- driver 已在 workspace openspec 中归档不等于任务可归档；仍须 close。

## reopen

用户明确 reopen 才动。先报告归档任务、driver 和 worktree 现状；目标 ongoing 路径冲突则停。

将整树搬回 ongoing，status 回 active，写 reopened 日期和原因，不删旧 SUMMARY / history / decisions；重建 INDEX，绑定后按 reconcile 和 router 从受影响 reference 继续。旧 driver 不自动删除或复用到新任务。
