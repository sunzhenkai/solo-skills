# Proposal：质量画像归属改为 task-goal（批 A·task-explore 侧）

## 背景

`task-explore` 的三处 references 把质量画像的产出者写成「上游 task-wizard 复杂档」，而 wizard 全文没有「画像」二字——2026-09-29 拆分后画像的产出点实际在 task-goal。这些是消费侧引用，不改会让 `design` / `decide` / `handoff` 三阶段一直指向一个不产画像的源。

## 决定

三处改为「上游 task-goal 复杂档」：

- `references/task-template.md:3`（`new` 时登记画像快照的条件）
- `references/task-template.md:33`（「方案」小节的画像原文快照行）
- `references/phase-decide.md:14`（冻结时画像快照属成功标准输入）
- `references/phase-handoff.md:28`（交接段逐字复制画像快照）

另 `references/task-template.md:55`（交接小节的画像快照行）补「上游 task-goal 复杂档带画像时」的条件。

## 理由

- 只改归属措辞，不改任何机制：快照的逐字复制、`pending` 降级门、`decide` 冻结规则原样保留。
- 保留「输入里没有画像时不编造」的既有纪律——task-goal 在简单/中等档写「无」，与之一致。

## 验证

- 族级契约测试 `TestPayloadOwners::test_no_stale_wizard_profile_attribution`：族内活文本不得出现「上游 task-wizard 复杂档」。
- 既有 `skills/task-explore/tests/test_task_explore_contract.py` 全过（含 `test_profile_snapshot_frozen_verbatim`）。

## 明确不改

阶段门禁、`handoff` 的 `--goal` 组装规则、INDEX 同步纪律、ledger 写入纪律。
