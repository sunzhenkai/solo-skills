---
id: task-delivery
name: task-delivery
description: "把一句复杂交付目标编排成自动闭环：探索 → 小切片实现 → 运行证据 → 三角色评审 → 失败归因 → 修复复验，进度只认 taskflow checkbox。仅在用户明确要求自闭环交付、自动探索加自动验证、或短目标端到端实现时使用；简单局部修改、只要方案、或未授权多阶段编排时不进入。支持 `goal:` 模式：本循环内的确认与方案审阅委托 task-goal，不列选项。"
---

# Task Delivery

把用户的短目标变成可验证交付，而不是一次性生成大而全的实现。本 skill 是**薄编排层**：不新建第二份任务账本，不复制 taskflow 的质量规则；进度以 taskflow checkbox 为唯一真相。goal 模式下本 skill 是**执行器**：状态与完成门由 task-goal 持有（见下方「goal 模式的归属」）。

## 输入

```text
task-delivery <一句话目标>
task-delivery goal: <一句话目标>
```

可识别的前缀：

- `normal:` 默认，真实交付。
- `goal:` 显式 goal 模式：本循环内所有要向用户确认的决定、以及方案审阅，一律委托 task-goal 的「审阅」，不列选项。
- `benchmark:` / `盲测:` / `回归复跑:` 只用于评估 skill 或 agent 能力。

未显式标记 benchmark 时一律按 normal 处理。

**goal 自动识别**：处理前缀前先判断——消息里看得到 `/goal`，或当前有进行中的 goal 且本条消息挂了本 skill。命中即按 goal 模式执行，不需要显式 `goal:` 前缀；未命中时按 normal / benchmark 处理。

## 依赖

本轮真正执行前，确认下列 skill 可读；缺任一项停下报告安装选项，不发明等价流程：

- task-wizard
- task-goal（goal 模式必需）
- task-explore
- taskflow
- role-based-reviewer
- skill-upgrader（仅 failure 归因为 skill gap 时需要）

## 主循环

1. **接收目标**：逐字保留目标原文，记录模式、预算、工作区和验证产物位置。
2. **移交方案决策**：委托 task-wizard 产方案（含复杂度档位与建议路由）。方案原文原样带入本循环，不自产方案、不改写。用户点名 `task-delivery` 已表示接受自动编排；这不授权危险操作、线上动作、提交或部署。goal 模式下，方案的外部参照与审阅由 task-goal 接管，**本循环是执行器，不写 goal 状态**：见下方「goal 模式的归属」。
3. **复杂门**：读方案的复杂度档位。非复杂（简单 / 中等）退出本 skill，说明按方案的建议路由执行即可，不硬套闭环；复杂才继续。不自建第二套复杂度判据。
4. **预算**：用户未给预算时，不虚构时间或 token 限额，按 Stage 9 的默认节奏执行；用户另给时间 / 轮次 / 资源预算时以用户值为上限。
5. **探索冻结**：按方案路由进入 task-explore，完成 explore → design → decide。
6. **taskflow 交接**：交给 taskflow 建 driver 与子 change；后续进度只认 driver / 子 change checkbox。**回归门**：driver 收口（含交接后中途长出的任何派生 driver / 子循环）时，MUST 回到本循环 Stage 7–12 继续执行，不得以子循环自定验收替代主循环的收口门；子循环自定 rubric 与 acceptance-rubric 口径冲突时，冲突项 MUST 停下报使用者裁决。
7. **首轮窄切片**：只选 1-3 个能从入口走到结束状态的核心闭环，先实现、测试、留证据。
8. **实现派发**：normal 必须给实现者质量画像或保留语义的子范围裁剪；benchmark 只给目标原文与运行约束。
9. **三角色评审**：调用 `role-based-reviewer mode=review roles=product,design,engineer`，先证据后评分。**异源门**：评审 MUST 与实现异源，按序降级——(a) 经 agent-roster 委派 reviewer / designer 到其他 Endpoint 的其他 coding agent；(b) 本机 subagent 显式指定与实现不同的模型跑本评审；(c) 两者皆不可用则停下问使用者，禁止静默同源自审交卷。同源评审输出只作线索、不作通过线。
10. **失败归因**：每条 Blocker / Major 只归因为 skill gap、implementation bug 或 acceptance gap；不许笼统“再改改”。归因前按 [归因自检](references/loop-protocol.md#stage-8--failure-triage)确认同一 finding 没有第二种解释、且修复层次已分清。
11. **修复复验**：skill gap 走 skill-upgrader patch；implementation bug 修交付仓；acceptance gap 补验收标准。修复后按 [增量验证协议](references/loop-protocol.md#增量验证协议)只重跑受影响门禁，Stage 10 再跑全链路。
12. **收口报告**：输出证据、分数、剩余限制和后续动作。它是交给 task-goal 判完成门的输入，本身不是完成门（goal 模式下的 owner 见「goal 模式的归属」）。

详细阶段、停止条件和修复轮次读 [references/loop-protocol.md](references/loop-protocol.md)。  
benchmark 输入隔离读 [references/benchmark-isolation.md](references/benchmark-isolation.md)。  
证据清单与最终报告读 [references/evidence-report.md](references/evidence-report.md)。

## goal 模式的归属

goal 模式（显式 `goal:` 前缀，或自动识别命中）下，同一个 task 的生命周期只有一个 owner：

- **task-goal 持有**：四状态（`执行中` / `已停` / `已交接` / `已完成`）、state-file、退出点与授权、完成门（完成判据成立 + 交付标准全过）。state-file 路径由本 skill 在建任务时写入 `goal-state-file:` 交给 task-goal（默认 `<evidence_root>/goal-state.yaml`）。
- **本 skill 持有**：Stage 1–12 的执行循环（探索冻结、窄切片、实现派发、证据、三角色评审、失败归因、修复复验）。
- **每轮收口回报**：一轮结束时把「本轮勾掉哪些 checkbox / 是否成立完成判据」回报给 task-goal（带 `goal-event:` 戳优先，无戳则按 task-goal 的事件推断顺序）。**本 skill 不写 `已完成`**——终态由 task-goal 在完成判据成立且交付标准全过时写入。
- **本 skill 的「收口报告」不是完成门**：它是交给 task-goal 判定用的证据与分数（见 Stage 12）。
- 停机口径不来自本 skill：命中 task-goal 的退出点（A 类降级未确认、失败计数上限、危险操作、线上动作、泄密）时按 task-goal 的规则停与呈现；本 skill 的 Stop conditions 只列执行器特有的停机项。

## 观感类质量目标

质量目标含审美 / 体验等**无法用确定性度量完备验收**的项时（典型：UI 观感、文案气质、交互手感），追加三条约束：

1. **天花板前置**：进入实现前 MUST 先定「卓越」的可数构成件或外部参照集；缺失则停下找使用者补，禁止以「无缺陷」默认收工。
2. **度量只声明地板**：收口报告 MUST NOT 用度量全绿支持「美观 / 优雅达标」类表述。
3. **中途真人门**（也是复杂档 B 类降级的唯一集中追认点）：每个修复轮后 MUST 给使用者看最小一批实物并收一句反馈再继续；使用者未看过实物的视觉交付不得进入收口。真人门同时是 B 类降级的集中追认点：逐条呈现 `provisional` 项（含回滚说明），追认改 `confirmed`，否决按回滚说明处理后回到降级确认门。等待使用者反馈期间按挂起五元组呈现（见 [../task-goal/references/suspension.md](../task-goal/references/suspension.md)），非依赖工作继续。

## 硬边界

- 不自动 commit、push、部署、改线上数据。
- 降级定级与确认门、失败计数（验证连败与假设封顶、审阅 P0/P1 连败与恶化闸）的唯一真源是 task-goal：A/B 定级与确认见 [../task-goal/references/quality-profile.md](../task-goal/references/quality-profile.md)「显式降级」节，失败计数见 [../task-goal/SKILL.md](../task-goal/SKILL.md) 退出点「同一验证连败两次」与「审阅不通过」。本 skill 只保留 hooks：A 类 pending 停机、B 类不停机、命中计数上限即停并输出诚实报告。
- 等用户类停机只冻结依赖面，按挂起五元组呈现，不全局停摆。
- 不把 benchmark 的隐藏期望带给实现者。
- 不把具体项目名、机器路径、凭据写进共享 skill。
