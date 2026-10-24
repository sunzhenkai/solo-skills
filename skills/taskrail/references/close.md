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
1. 写 `SUMMARY.md`：交付与验证、最终有效机制 / 根因、被推翻假设、关键决定、可复用经验、剩余风险、后续项和长期文档链接。
2. 只有跨任务仍成立的知识才提升到 AGENTS / ADR / glossary / 项目 wiki；任务特例留在 SUMMARY，不自动改 Skill。
3. 完成通知说明各仓库分支 / worktree、验证结果和如何合入；不 push、不自动清理 worktree。
4. 按 [done.md](done.md) 最终核对，使用 `task_state.py update ... --status done --current-ref close`；脚本检查 SUMMARY 和所有直接子任务 done。
5. 按 [archive-reopen.md](archive-reopen.md) 同轮归档整棵任务树并重建 INDEX。未完成关闭不伪写成功总结。

## 产出
SUMMARY.md、长期知识指针（按需）、done 状态和可读的完成通知。

## 完成门
SUMMARY 存在、判据证据有效、子任务全 done、状态与 INDEX 一致，归档路径可读。

## 退出与重入
任务结束。reopen 后 status 回 active，并从受影响 reference 重入；旧 SUMMARY 不覆盖，追加新验证和更正。
