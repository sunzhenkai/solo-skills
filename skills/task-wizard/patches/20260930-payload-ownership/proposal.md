# Proposal：完成判据加回模板（批 A·task-wizard 侧）

## 背景

2026-09-29 拆分把 Goal 方案层整体搬进 task-goal 时，连同「## 完成判据」小节一起删了。结果是链上**没有任何一环产完成判据**，而四个下游都要求它逐字传递（task-goal 起手节、delivery Stage 3 的 driver proposal、task-explore 的 `TASK.md`「方案」小节、taskflow 的验收标准）。

## 决定

模板在「## 目标」后加回「## 完成判据」小节，并把「## 目标」收窄为「任务名 + 一句话背景」——原写法 `<一句话说清完成标准>` 与判据语义重叠，不收窄会出现两个互相矛盾的可检查字段。

配套五处措辞：「交付级但克制」原则写明判据是整条链的载荷；「简洁」原则写明判据不可省；工作流第 2、5 步要求摸底后写出判据候选、写不出就不交出方案；复杂度路由表与两条路由说明把判据列入逐字携带的正文清单。

本 patch 同时改 `README.md` 的 wizard 行（「复杂档含质量画像」→「不产质量画像」）与 task-goal 行（补「复杂档产质量画像与显式降级」）。

## 理由

- 判据在人工链路（wizard → 人确认 → 实现）本来就该存在，不是 goal 专属概念；放回 wizard 不引入 goal 语义。
- 不写入质量画像，保持 wizard 不感知 goal（与 `test_goal_terms_gone` 的既有约束一致）。

## 验证

- 族级契约测试 `TestPayloadOwners`：wizard 含 `## 完成判据`、不含「质量画像」；族内无残留的 wizard 画像归属。
- 既有 `skills/task-wizard/tests/test_task_wizard_contract.py` 全过（本改动不触及被其断言的小节）。

## 明确不改

复杂度路由判据、外部参照触发范围、「决策收敛」的①/②授权清单（上一批 `cut-interruptions` 已改）、边界节。
