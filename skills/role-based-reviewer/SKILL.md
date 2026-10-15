---
id: role-based-reviewer
name: role-based-reviewer
description: "可组合的角色化只读评审：engineer、algo、data、sre、ops、biz、product、design（别名 uiux）、qa、skill、intent。仅在用户显式点名（/role-based-reviewer）、指定 roles=、明确要求按岗位/多角色视角，或上游工作流以 mode=review + 完整 roles + 审阅边界结构化调用时使用。普通「看看代码」「帮我 review」不要自动加载。"
---

# 角色化评审

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文，不要逐词硬翻。

`mode=ask`：按岗位回答问题、标明证据与下游建议。  
`mode=review`：真正做多视角审查，输出分级发现；默认目标为当前工作区变更。

本身不改代码、不落盘、不替代实现类 skill。用户要求修复时再动手。

## 三道门禁（防误触、防角色膨胀、防吹毛求疵）

未过门禁不得进入本 skill 的预加载与分角色审查。

1. **门 1 · 收窄触发**：仅下列情况使用；否则当普通问答/常规审查处理，不加载本 skill。
   - 用户点名本 skill，或发出 `{{slash:role-based-reviewer}}`
   - 用户写出 `roles=` / 岗位短名（如「用 algo 看」「engineer+sre review」）
   - 用户明确要求按岗位、多角色、跨职能视角看问题
   **不算触发**：单独的「看看这段」「帮我 review」「有没有 bug」「审查一下 diff」——没有岗位意图时不要自动进来。
   - 上游编排型工作流以结构化参数调用，且 `mode=review` 与完整合法的角色集 `roles=` 齐备；审阅边界输入（完成判据、质量画像 / 角色底线、显式降级清单、命中交付类别门包时的门包与运行态证据、本环节「审」与「不审」的范围）应尽量齐备——边界缺项（含门包缺失、运行态证据缺失）不构成拒审理由，但须按已有边界审查、报告开头写明缺哪一块、对受影响条目标注未验证，不得把缺项当通过。满足上述条件时承认其为正当调用方，按传入角色执行；角色集由调用方按任务适用面给定，数量随任务变，不算角色膨胀。
2. **门 2 · 角色确认**：未指定 `roles` 时默认只开 **engineer**。其它角色必须有**强信号**才加（见下节）；一次推断将超过 2 个角色时，先列出候选问用户，禁止静默堆视角。文件名/目录沾边（有 CSS、有 Dockerfile、有 `model` 字样）不够。
   - 调用方传入完整 `roles=` 属「已指定」而非推断：照单执行，不列候选、不反问，即使角色数超过 2 个。用户当轮显式点名的 `roles` 优先于传入值；两者都不增删。
3. **门 3 · 发现克制**：`mode=review` 默认只报 **Blocker** 与 **Major**。Minor / Suggestion 仅在用户要求「仔细 / 全面 / 含风格」时输出。不确定的不当 Blocker；没有问题就说没有，不为每个角色凑一条。

## 输入

- `roles=<逗号分隔角色>`：可选。合法值：`engineer`、`algo`、`data`、`sre`、`ops`、`biz`、`product`、`design`（别名 `uiux`）、`qa`、`skill`、`intent`（仅调用方显式传入，审意图复述）。
- `mode=<ask|review>`：可选，默认 `ask`。已过门 1 且用户说评审 / review / 审查时视为 `review`。
- `<问题或变更范围>`：可选。`mode=review` 且未给范围时，默认当前工作区 `git diff`（仍受门 2：不要因此自动加角色）。
- `审阅边界输入`：仅工作流调用方需要。随附完成判据原文、质量画像 / 角色底线、显式降级清单、本环节「审」与「不审」的范围。质量目标含审美 / 体验等无法用确定性度量完备验收的项时，角色底线里还须带天花板参照集（把「卓越」落成可数构成件或外部参照）。命中交付类别门包时还须附门包（见 taskrail 门包表）与运行态证据（起服务 + 截图 / 录屏 / 断言输出）。缺项时只按已有判据审查，并在报告开头写明缺哪一块，不擅自扩大到「不审」列里的内容。
- `产物状态`：`mode=review` 时由调用方给出所审产物的状态标识（提交号，或未提交时的 dirty 摘要）；未给时评审自行取自工作区并在报告「依据状态」注明取得方式。报告与 findings 只对该状态有效。
- `model=<模型名>`：可选。subagent 派发时显式指定评审所用模型（异源评审用）；不指定则模型继承调用方。
- `endpoint=<agent-roster 端点>`：可选。经 agent-roster 委派该端点的 agent 执行评审，Handoff / 回收按 agent-roster 契约；与 `model` 同给时，`model` 作建议、端点自行解析时以其为准。

示例与工作流 / 异源调用样例见 [references/inference-and-speed.md](references/inference-and-speed.md)。

## MUST 先读取

[references/protocol.md](references/protocol.md)（约束、预加载、输出骨架、角色边界）。

## 视角推断与耗时优化

- 用户或调用方给定的 `roles` 不增删；仅二者皆无时推断：**默认只 engineer**，额外角色要主体强信号，推断超过 2 个只留信号最强的 2 个并在报告开头说明。
- 大目标先摸规模、按模块抽样；支持 subagent 时可按角色并行派发（见「流程」第 4 步）。
- 信号表与细则见 [references/inference-and-speed.md](references/inference-and-speed.md)。

## 流程

1. 过三道门禁。未过门 1 则不要按本 skill 执行。解析 `mode`、`roles` 与可选的 `model` / `endpoint`；未指定角色时按上节推断，受门 2 约束。
2. 对每个生效角色，按 [protocol 预加载节](references/protocol.md) 加载上下文（含生效角色的 `references/roles/<role>.md`，计入文件预算）。跨角色复用同一文件，合计宜控制在约 6 个文件（建议，非硬线）。`mode=review` 另遵循耗时优化。
3. `mode=ask`：按角色输出独立结论、证据、边界与下游建议。
4. `mode=review`：按角色输出独立 findings，标注严重级别与 `path:line`；共享对象上标主责 / 协作 / 冲突。**派发策略**：`model` / `endpoint` 都不给时，本 skill 自己完成审查；给了任一参数则按参数派发——`endpoint` 经 agent-roster 委派该端点的 agent（选人、Handoff、回收按 agent-roster 契约），仅 `model` 时本机 subagent 按角色并行派发并显式指定该模型；派发结果仍按 protocol 输出骨架汇总去重。两者皆不可用（无 subagent 能力 / 名册无端点）时 MUST 停下报告调用方，禁止静默降级为同源自审（例外：调用方已判定不可用、未调用本 skill 并自行登记降级，如 task-intent goal 自审）。
5. 合并时只去重「同一证据支持的同一风险」；不得把不同角色的结论混写成无归属意见。
6. 下一步默认只推荐一个主责动作；确需并行时写明独立任务与先后关系。

## 严重级别（`mode=review`）

Blocker / Major 默认报，Minor / Suggestion 仅在要求仔细审查时给（门 3）；定义见 [references/severity.md](references/severity.md)。

## 输出

骨架见 [protocol 输出骨架节](references/protocol.md)。多角色 review 至少包含：

- 依据状态：所审产物的状态标识（提交号 / dirty 摘要）与审阅边界齐备性（缺项逐条写明）
- 生效角色及选择依据
- 每个角色独立的 findings / 证据 / 下游建议；Blocker / Major 带稳定编号（供调用方处置台账引用）
- 共享风险的主责与协作角色
- 未覆盖项与降级建议（含未覆盖原因、建议处置与工具不可用时的替代方法与能力边界）
- 未知项、角色间分歧（如有）
- 统一的下一步与总结置信度

报告只对「依据状态」所标识的产物有效；产物变更后受影响的 findings 作废重审。findings 的处置（`fixed` / `accepted-recorded`）由调用方记录，本 skill 不代替调用方判收敛。
