# Patch Proposal: ruling-format

- patch_id: 20260929-192715-ruling-format
- target: skills/task-delivery
- mode: update
- risk: medium

## 问题

回归门里「冲突项 MUST 停下报使用者裁决」没有定义报的形状。同一真实执行中，执行者把它当成需要等待的「审阅收口授权」登记进任务清单，阻塞闭环。

## 改动

`skills/task-delivery/references/loop-protocol.md` Stage 7 回归门尾部追加一句：报使用者裁决的形状是写明冲突项、双方口径原文、推荐裁决与需要的一句话决定；一次性说明，不列选项，不把等待裁决登记为任务。

## 理由

task-delivery 的回归门与 task-goal「授权」节（本批次另一 patch：20260929-192710-goal-wait-protocol）呼应：goal 模式下裁决请求走 task-goal 审阅呈现，本句只规定非 goal 路径与回归门自身的最小呈现，避免两处口径冲突。复用既有术语（裁决、口径、冲突项），不新增概念。

## 可验证点

- Stage 7 回归门文本含「写明冲突项」与「推荐裁决」。
- 含「不列选项」或同等「一次性说明」表述。
- 含「不把等待裁决登记为任务」。

## 验证

- `git apply --check --recount`
- `python3 -m pytest skills -q`（task-delivery 无 tests 目录，跑全量确认无连带失败）
- 人工核对 diff 与本 proposal 一致、无隐私内容。

## 风险与回滚

medium：改交付闭环协议的输出契约。回滚 = `git apply -R` 本 patch。
