# Proposal：审美 / 体验类目标的天花板参照集，落进质量画像并接入 design 审阅

## Intent

「观感类质量目标」（task-delivery SKILL.md）原有三条约束：天花板前置、度量只声明地板、中途真人门。前两条在改正文里**没有任何落点**——天花板前置要求「先定『卓越』的可数构成件或外部参照集」，但没说这个定义写在哪个字段、谁审；度量只声明地板是收口侧措辞约束，不影响采集。

实测缺口：天花板因此只由中途真人门兜底，而真人门在最后一环才发生；评审侧完全没有主体——`role-based-reviewer` 的 design 角色以「Blocker 门槛 = quality floor」为界，「不算问题」节还明确不报「像素与间距口味」「设计趋势追逐」，任何美学比较在没有可落条目时**不许报**。

本 patch 把天花板定义**落进质量画像的 design 底线**（那里本就允许「不适用」，纯后端任务不受影响），再让参照集沿既有快照链进到 Stage 7 审阅边界，由 design 角色按它出意见。据此，三条约束各自的归属是：

| 约束 | 归属 | 本 patch 的处理 |
|---|---|---|
| 天花板前置（定义「卓越」） | 质量画像 design 底线 | 画像字段 + 判据 + 去向一节；缺 → P0，走「理解不够」 |
| 度量只声明地板（措辞） | task-delivery 收口侧 | 不动 |
| 中途真人门 + B 类追认点（时机 / 停机） | 循环侧 | 不动（reviewer 只读单次、不持状态，结构上做不了） |

## 领域依据

参照集是通用的工程机制而非本项目特例：设计系统与无障碍标准都以「外部参照 + 可指认条目」表述验收（WCAG 的成功标准、各家的 design token 基线），而审美主张一旦落到「哪一件参照、差在哪一点」就可判定——这正是它能把 reviewer 的「不许报」翻成「可以报」的原因。

## Files

- `skills/task-goal/references/quality-profile.md`：字段模板的 `design` 行加「天花板参照集」；字段规则新增一条（含「写不出走『理解不够』，不以『无缺陷』默认收工」）；新增「## 天花板参照集的去向」（随快照进审阅边界；不引入新审阅对象；缺失按 P0）
- `skills/task-goal/SKILL.md`：审阅边界的画像检查项并列「审美 / 体验类目标的天花板参照集」
- `skills/task-goal/evals/cases.yaml`：新增 `aesthetics-ceiling-reference-set`
- `skills/task-goal/tests/test_task_goal_contract.py`：`TestQualityProfileContract` 增一条断言（`天花板参照集` + `## 天花板参照集的去向`）
- `skills/task-delivery/SKILL.md`：第 1 条约束从「MUST 先定」改为指向画像字段，并写明参照集进 Stage 7 审阅边界、本循环不另立评审主体
- `skills/task-delivery/references/loop-protocol.md`：Stage 7「观感类目标」段补参照集来源与「design 未生效或模板未给参照集时不补审天花板，按缺字段报」
- `skills/task-delivery/evals/cases.yaml`：新增 `aesthetics-ceiling-comes-from-profile`

分三个 patch 目录（各自 skill 侧）：

- `skills/task-goal/patches/20260930-173857-aesthetics-ceiling-refset/`
- `skills/task-delivery/patches/20260930-173857-aesthetics-ceiling-refset/`
- `skills/role-based-reviewer/patches/20260930-173857-ceiling-refset-boundary/`

## Conflict check

- **不新增审阅对象**：画像明文「架构、接口、schema、代码骨架仍在『不审』列」，新节重申一次。「参照集」是评审的度量物，不是被审对象。
- **不动 role-based-reviewer 的三道门禁、角色推断与「不算问题」既有条目**：该 skill 侧的改动只有两处——`SKILL.md` 的 `审阅边界输入` 条目补一句「含审美项时角色底线须带参照集」，以及**改净本轮引入的失效措辞**：门 1 第 4 条原文「这类流程固定 3 个角色属预期」是本地固定三角色的产物（已由 `20260930-171920-roles-on-demand` 作废，未改净），改为「角色集由调用方按任务适用面给定，数量随任务变」。此处与 20260930-171920 属同一根因，故由本 patch 一并收口，并在 result 里交叉注明。
- **design 角色的「不算问题」节保持原样**：新节用「不受……两条的免报保护」限定其范围（那两条针对无可落条目的审美主张），而非改动或删除原条目。
- **taskflow / task-explore 与验收 rubric 不改**：参照集随画像原文快照走既有通道（taskflow 已明文「质量画像原文逐字保留，不摘要」），不需要新的传递条款；rubric 的五维与 UI/UX 六子项口径亦未触及。

## Risks

- 中：design 角色第一次获得带主观项的评审面。约束是「每条意见必须指到参照集里的具体件并写清差在哪」，无可对照即降 Suggestion 并注明；误报压力落在参照集质量上，而参照集质量本身已由画像字段判据与审阅 P0 把关。
- 低：参照集缺失时按缺字段判 P0，可能让原本能交付的观感类任务多一次回头补定义——这是有意换取「不以无缺陷默认收工」。

## Validation

- 三个 `change.patch` 分别 `git apply --check --recount` 通过；三者连续应用后 `git diff --check` 无空白问题
- `python3 -m pytest skills -q`：428 passed, 1 skipped
