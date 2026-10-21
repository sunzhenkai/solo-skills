# 落盘模板

元信息写在开头的 `---` frontmatter，字段与取值只在 [契约](contract.md)。按已知信息填，未知留空，不编造。

## TASK.md

```markdown
---
slug: <slug>
status: ongoing
phase: wizard
confirm_mode: <human | goal>
tier: <skip | full>
criterion: "<完成判据原文；没有就留空>"
driver: null
evidence_root: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Title>

## 目标
- <要达成什么>

## 不做
- <只来自用户原话>

## 方案
<指向 wizard/plan.md 与 design/；上游给了现成方案就登记要点>

## 进展
- YYYY-MM-DD：<本轮结论，一条一事>

## 已做决定

唯一的决定清单：意图、grill、design、闸口和实现中定下的都追加到这里。

| # | 决定 | 理由 | 可逆 | 来源阶段 |
|---|------|------|------|----------|
| D-1 | <定了什么> | <一句为什么> | 是 / 否 | wizard / design / approve / apply |

## 验证
<skip 档与拆成子任务的父任务：验证命令与结果>

## 交接
<handoff 时按 handoff.md 写>
```

子任务在 frontmatter 另加 `parent:`，`criterion` 用父任务路线图那一行的子判据；父任务的子任务清单就是 `wizard/plan.md`「路线图」，不另抄（见 [large-scope.md](large-scope.md)）。

## INDEX.md

```markdown
# Tasks

派生索引；编辑单任务请改对应 `TASK.md`。

## Ongoing

| 任务 | 标题 | 更新 | 一句话 | 路径 |
|------|------|------|--------|------|

## Archived

| 任务 | 归档日 | 标题 | 一句话 | 路径 |
|------|--------|------|--------|------|
```

Ongoing 按更新日新到旧，Archived 按归档日新到旧。没有任务时只留表头。

## design/<topic>.md

```markdown
# <Title>

> 一段话：做什么、为什么、选哪条路。

## 现状
<已知事实与约束，链到代码 / 文档>

## 方案
<按 plan 步骤展开；图用 ASCII / Mermaid>

## 取舍与回退
<推荐 vs 放弃的方案、接受的取舍、选错了怎么撤>

## 未决
- [ ] <仍未定的>
```

按问题裁剪；对比表与设计依据格式见 [design-detail.md](design-detail.md)（可选）。
