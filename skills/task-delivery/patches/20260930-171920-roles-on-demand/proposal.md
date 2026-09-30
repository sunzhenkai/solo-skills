# Proposal：评审角色改为按任务涉及面推断

## Intent

`task-delivery` 与 `task-goal` 把评审角色集写死为 `roles=product,design,engineer`（两处调用口径 + 一处「不强制三角色」措辞 + 两处 evals）。写死的三角色对不含界面的交付会派出空转的 design，也表达不了涉及部署 / 模型 / 数据 / 运营配置 / 对外对接的交付；评审角色本应随任务涉及面变化。

本 patch 改变的模型行为：

1. `task-delivery` Stage 7（loop-protocol.md 与 SKILL.md 主循环第 9 步）：`roles` 由固定清单改为按任务实际涉及面推断——基线取质量画像 `角色底线` 里写成可检查要求的那几条（写「不适用」的不取），任务确实触及部署 / 模型 / 数据 / 运营配置 / 对外对接时，再按 role-based-reviewer 的角色表补 `sre` / `algo` / `data` / `ops` / `biz`；推断结果与依据写进 evidence manifest 的 `role_review`，使「为什么没派 design」可复核。
2. `task-goal` 审阅人选表 role-based-reviewer 行：固定项同样改为 `mode=review` + 按适用面推断的 `roles`，推断依据连同角色集写进回复记录（该表本就要求记录评审者）；「简单和中等不强制三角色」改为「角色集不预置，按任务适用面推断；简单和中等不强制角色化评审」。
3. 两处 evals 期望同步为「按任务适用面推断，不预置固定清单」。
4. `task-delivery` 新增契约测试 `TestRoleReviewOnDemand`：正文与 loop-protocol 不含 `roles=product,design,engineer`，且保留「按本任务实际涉及面推断」「不预置固定清单」「role_review」三个锚点。

非目标：不新增角色；不改 role-based-reviewer 的门禁、推断规则与「默认只 engineer」；不改 acceptance-rubric 的五维与 UI/UX 六子项口径；不改 taskflow 侧的评分主体分工措辞（见「Conflict check」）。

## Conflict check

- **role-based-reviewer 门 1 第 4 条**（结构化调用需 `mode=review` + 完整合法 `roles=` + 审阅边界）：本 patch 仍传入推断后的 `roles`，三项齐备不破；配合门 2「调用方传入完整 `roles=` 属已指定，照单执行、不列候选、不反问」，推断结果不会被 reviewer 二次追问。
- **role-based-reviewer「默认只 engineer」**：那是它在本方**不给** `roles` 时的兜底；本条要求给出推断结果，属于「已指定」，不与其冲突。若本方推断不出可信角色集，退化到不给 `roles` 亦可接受（reviewer 兜底 engineer），故本条不构成新的停机点。
- **quality-profile「角色底线」三条都要写**（product / design / engineer，不适用写「不适用」加原因）：本条的基线正取自该字段，方向一致；纯后端任务的 design 底线本就写「不适用」，据此不派 design 与画像规则自洽，无需改画像。
- **acceptance-rubric「UI/UX 由 design 评」**：无界面交付时该维度无人打分，属既有现象（画像允许 design 写「不适用」），本 patch 不扩大也不消除，故不动 rubric —— 见「已知遗留」。
- **task-goal「简单和中等不强制三角色」**：原文措辞绑定「三角色」这一固定集，推断制下该措辞失去所指，改写为「角色集不预置……不强制角色化评审」，语义只做等价迁移，不放松复杂档的固定项。
- **taskflow「评分主体按 product / design / engineer 分工」**（evals/cases.yaml）：属评分主体，不属角色集清单；本项目未纳入本轮范围，保持在 taskflow 侧不动。

## Risks

- 中：评审角色集从确定值变为推断值，评审报告的角色组成不再可预测；用 manifest / 回复记录中的 `role_review`（角色集 + 依据）作为事后审计点，取代原先的固定清单。
- 低：若推断漏派了 role-based-reviewer 角色表中本应涉及的角色，finding 覆盖会变窄；推断依据可复核即为纠偏入口。

## Files

- `skills/task-delivery/SKILL.md`：description 的「三角色评审」→「角色化评审」；主循环第 9 步改推断规则；「goal 模式的归属」中「三角色评审」→「角色化评审」
- `skills/task-delivery/references/loop-protocol.md`：Stage 7 调用示例、推断段、findings 要求
- `skills/task-delivery/evals/cases.yaml`：`evidence-before-score` 期望行
- `skills/task-delivery/tests/test_task_delivery_contract.py`：新增 `TestRoleReviewOnDemand`
- `skills/task-goal/SKILL.md`：审阅人选表 role-based-reviewer 行、其下方「不强制三角色」条
- `skills/task-goal/evals/cases.yaml`：`complex-tier-fixed-role-reviewer` 的 description 与期望行

## Known leftovers（本 patch 未处理）

- acceptance-rubric 未定义「某评分维度不适用时如何记分」，无界面交付的 UI/UX 维度仍无明确处置（本轮范围经确认不含 rubric）。

## Validation

- `git apply --check --recount` 通过
- `python3 -m pytest skills -q`：426 passed, 1 skipped
