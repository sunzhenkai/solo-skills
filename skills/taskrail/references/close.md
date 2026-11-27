# close：总结知识并完成归档

## 目的
把验证过的交付变成可恢复结果和可复用知识，再安全关闭任务。

## 进入条件
verify 全过；或用户明确放弃 / 关闭未完成任务（此时 status 为 archived，不是 done）。

## 跳过条件
无。driver 已归档、criterion checkbox 已勾都不能替代本环节。

## 所需输入
criterion、验证证据、decisions、context/current、ROADMAP / 子任务状态。

## 执行方法
1. 写 `SUMMARY.md`：交付与验证、最终有效机制 / 根因、被推翻假设、关键决定、可复用经验、剩余风险、后续项和长期文档链接；未阻塞交付的 `F-n` 写入剩余风险或后续项。单一明确小改可用 3 段紧凑版（结果与验证、分支与合入方式、剩余风险），不硬凑空节。
2. 只有跨任务仍成立的知识才提升到 AGENTS / ADR / glossary / 项目 wiki；任务特例留在 SUMMARY，不自动改 Skill。落点按内容分：
   - 项目有 Atlas 时运行其 `status`，`stale_pages` 非空就把复核交给 `project-atlas`，或在 SUMMARY 后续项列出过期页。
   - 可复用经验、踩坑和操作台账交给 `wiki-data`，保留来源、置信度与时效。
   - 跨项目验证的通用方案模式可交 `project-design-patterns` 沉淀为模式卡（未安装则留在 SUMMARY）。
   - 跨任务的 skill 改进交给 `skill-upgrader`，单次经验只留在 SUMMARY。
3. 完成通知按 [user-report.md](user-report.md) 突出交付结果、验证结论与落地方式；若改动仍在 worktree 或非默认分支、尚未推送或未合入默认分支，完成通知必须明说分支名与未合入状态，并主动提示转入 `session-wrap` 处理推送、提 MR/PR、清理 worktree 或弯路复盘，需要 diff / MR 级代码审查时可另行运行 `solo-code-review`（本环节不 push、不自动清理 worktree、不自动调用 `solo-code-review`）。
4. 按 [done.md](done.md) 最终核对，使用 `task_state.py update ... --status done --current-ref close`；脚本检查 SUMMARY 和所有直接子任务 done。
5. 按下文「归档与重开」同轮归档整棵任务树并重建 INDEX。未完成关闭不伪写成功总结。

## 产出
SUMMARY.md、长期知识指针（按需）、done 状态和可读的完成通知。

## 完成门
SUMMARY 存在、判据证据有效、子任务全 done、状态与 INDEX 一致，归档路径可读。

## 退出与重入
任务结束。reopen 后 status 回 active，并从受影响 reference 重入；旧 SUMMARY 不覆盖，追加新验证和更正。

## 归档与重开

原则：不覆盖、保留未结项、整树移动、INDEX 可重建。

- **完成归档**：close 完成且 status done 后同轮把父任务整树移到 `tasks/archive/<yyyy-mm-dd>/<task-id>`（子任务留在 subtasks）；搬前核对未结子任务、未决、driver / worktree 现状与目标路径冲突（冲突则停）；写回热状态与 SUMMARY → 记 archived 日期 → 原子移动整树 → `task_state.py rebuild-index <workspace>` → 核对新路径可读、旧路径不存在 → 清绑定。driver 已在 workspace openspec 中归档不等于任务可归档。
- **未完成关闭**：仅用户明确放弃 / 关闭时置 status archived，不伪写成 done 或成功 SUMMARY。
- **reopen**：仅用户明确要求时执行。先报告归档任务、driver 与 worktree 现状（目标 ongoing 路径冲突则停），将整树搬回 ongoing，status 回 active，记 reopened 日期与原因，保留旧 SUMMARY / history / decisions，重建 INDEX 后按 `reconcile` 与 router 从受影响 reference 继续；旧 driver 不自动删除或复用。
