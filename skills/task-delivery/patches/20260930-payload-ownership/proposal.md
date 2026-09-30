# Proposal：方案来源与画像归属分列（批 A·task-delivery 侧）

## 背景

`references/loop-protocol.md` 的 Stage 1 与 Stage 3 把两个载荷都挂在 task-wizard 名下：「委托 task-wizard 产方案（含复杂度档位、建议路由，复杂档含质量画像）」「normal 的质量画像由 task-wizard 复杂档产出」。wizard 不产画像。

## 决定

- Stage 1：改为「委托 task-wizard 产方案（含完成判据、复杂度档位与建议路由）」。
- Stage 1 第二点：质量画像来源改为「由 task-goal 复杂档产出（或逐字采用上游快照）」。
- Stage 3 的 driver proposal 清单：两项分别标注来源——完成判据来自 task-wizard，质量画像来自 task-goal 复杂档。

## 理由

不改 Stage 2/3 的流程与门禁，只把两个载荷的产出者写对；`decide` 冻结门与 `pending` 降级规则原样保留。

## 验证

- 族级契约测试 `TestPayloadOwners`。
- 既有 `skills/task-delivery/tests/test_task_delivery_contract.py` 全过。

## 明确不改

Stage 2 探索冻结、Stage 4-12、Stop conditions（失败计数去重见下一批 `family-single-source`）、增量验证协议、benchmark 隔离。
