# 落盘模板

新建与状态更新优先使用 `scripts/task_state.py`，不要手工复制整套文件。字段以 [contract.md](contract.md) 为准。

## TASK.md（热状态）

```markdown
---
slug: <task-id>
parent: null
status: active
current_ref: plan
confirm_mode: human
execution: null
criterion: "<完成判据>"
driver: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# <标题>

## 目标
<一句话>

## 完成判据
<criterion 原文>

## 下一动作
<当前可执行动作>

## 涉及仓库
| repo_id | source_repo | worktree | branch | base |
|---|---|---|---|---|

## 产物指针
- PLAN.md
- context/current.md
```

TASK 只保留恢复所需热信息；路由历史、长决定、原始证据分别放 history.md、decisions.md、evidence/。约 6 KB 后压缩下沉，不截断 criterion。

## PLAN.md

```markdown
# 当前计划

## 当前步骤
- [ ] <动作> — 验证：<命令或检查>

## 验证策略
<focused tests、回归、集成与证据落点>

## 约束 / 回滚
<按需>

## 实施确认
- 状态：pending | confirmed | not-required
- 依据：<human 写用户明确确认原话与日期；goal 写简要复述已给出>
- 范围：<覆盖的当前实施步骤与验证策略>
```

human 进入 execute 前必须为 confirmed，goal 记 not-required。实施范围、步骤或验证策略实质变化后回 pending；只更新 checkbox 或证据不改变状态。direct 的 PLAN checkbox 是实施进度；OpenSpec 实施进度只在 change checkbox。父子结构只写 ROADMAP，不在这里复制状态。

## ROADMAP.md

见 [decompose.md](decompose.md)。只在拆分时存在；集成项由父任务验收。

## context/current.md

```markdown
# 当前事实与假设

| 结论 | 状态 confirmed / assumed / refuted / superseded | 证据 | 失效条件 |
|---|---|---|---|
```

约 8 KB 后把旧细节转 history / evidence，只留当前有效结论和指针。

## decisions.md / history.md

decisions 用 `D-n`、理由、来源和 `active / superseded`；被取代项写由哪个决定取代。history 追加日期、reference、enter / skip / exit / reopen、理由和产物路径；默认不加载。

## SUMMARY.md

```markdown
# 交付总结

## 结果与验证
## 最终有效机制 / 根因
## 被推翻的假设与认知更正
## 关键决定
## 可复用经验与长期文档链接
## 剩余风险与后续项
## 分支、worktree 与合入方式
```

## design/<topic>.md

```markdown
# <标题>
> 做什么、为什么、选哪条路。

## 现状与证据
## 契约 / 方案
## 兼容性、取舍与回滚
## 验证策略
## 未决
```
