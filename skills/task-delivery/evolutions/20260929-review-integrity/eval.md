# Evaluate — 20260929-review-integrity

## 回归（现有成功路径）

对照 evals/cases.yaml 五个既有 case 逐条过：

- `explicit-loop-orchestrates-existing-skills`：主循环链路（task-wizard → task-explore → taskflow → checkbox 真相源）未改，step 6/9 为追加约束，无打断。pass
- `ordinary-request-does-not-activate`：description 未动，复杂门不变。pass
- `benchmark-input-isolation`：patch 不涉及 benchmark 路径，隔离规则原样。pass
- `normal-delivery-context`：质量画像/裁剪要求未动。pass
- `failure-three-way-triage`：归因三分类与 Stage 8 自检未动。pass

## 模式（原失败是否被新指令避免）

- 「主循环 Stage 7 被子循环自定验收静默替代」→ 回归门（SKILL step 6 + protocol Stage 7）要求 driver（含派生）收口 MUST 回 Stage 7–12，冲突 MUST 报使用者：该类失败会被显式拦截，不再依赖有人记得。避免成立。
- 「同源自审高分自证」→ 异源门三级降级 + 同源只作线索：默认路径不再是同源自审。避免成立。
- 「无天花板定义以无缺陷收工」→ 观感类三分支：前置定义 + 度量只声明地板 + 中途真人门。避免成立。
- 「真人首次反馈在收口才到」→ 中途真人门把使用者介入提前到每个修复轮。避免成立。

## 契约

cases.yaml 的 expect 均为指令级判据（deterministic judge），无脚本可跑；按指令级对照，新增规则不与任何 must/must_not 冲突。pass

## 副作用

- 触发范围：description 与「输入」「复杂门」未动，激活条件不变。
- 破坏性/权限：无放宽；新增三条 MUST-stop（异源不可用、天花板缺失、rubric 冲突），全部 fail-safe 方向。
- 节奏风险：异源门 (c) 与真人门可能拖慢闭环——已用降级顺序与「最小一批 + 一句话」限定成本；残余风险在 proposal.risk 声明为 medium。

## 结论

pass
