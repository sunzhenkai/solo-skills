# Proposal：task-wizard 收窄为纯方案层，加决策收敛

与 task-goal 的 `patches/20260929-decouple-goal-protocol/proposal.md` 同一次改造，本文件只记 task-wizard 侧。

## 改动

- 删：「先分流」、Goal 方案整节（不套模板/正文/外部参照/审阅/旧方案/写完之后/退出点/授权/执行中改步骤/做完）、CONTEXT.md 中 14 条 Goal 专属术语。
- 加：「决策收敛」节——方案落稿前把所有要人拍板的歧义（带推荐答案）、假设、阻塞点、执行中须授权的动作写进方案；下游只做「按此执行 / 调整哪步 / 改路由」三选一，方案外缺口不允许在执行期冒出来向人要答案。
- references：quality-profile.md、legacy-plans.md 迁往 task-goal；external-precedent.md 保留（方案定稿前的动作归方案层），删掉其中 Goal 方案小节。
- 复杂度路由：删 Goal 专属注记，补「方案由 goal 里的执行方接收时，确认与审阅走 task-goal，本 skill 不参与」。
- frontmatter description 去掉 goal 分支表述。
- 契约测试重写：Goal 节与术语不存在、决策收敛存在、references 迁移检查。

## 验证

`python3 -m pytest skills/task-wizard/tests -q` 全过；全仓 282 passed。
