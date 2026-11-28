---
id: project-patterns
name: project-patterns
description: 个人项目的可复用设计模式库（原 project-design-patterns）：把跨项目重复验证的方案固化为模式卡（动机、参与者、落地件、边界、先例），当前收录 agent 数据接入（含 agent-api-ops 操作规范）、模型供应商管理（含 models.dev 加载与模型联动实现 prompt）与接口访问统计。设计新应用或新功能、讨论接入/集成方案、评审方案完整性，或想把某次交付沉淀为模式时使用。
version: 1.4.0
---

# 项目设计模式（project-patterns）

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文。

把跨项目重复出现的方案固化为**模式卡**：设计或评审时先查这里，按卡上的落地件清单对照现状，不从零推导；任务收口时把新验证的方案沉淀成新卡登记进来。模式卡只描述「什么方案、由什么组成、边界在哪」；可执行的操作规范放本 skill 的 `references/`，卡里按名指向。

## 使用方式

- **设计 / 评审**：按模式索引选卡，读对应 `references/<pattern>.md`，对照落地件清单检查方案完整性，缺件按卡上的边界说明处理。
- **接入实施**：应用已采用 agent 数据接入模式时，按 [references/agent-api-ops.md](references/agent-api-ops.md) 的凭证、认证与操作纪律执行；新建或重构模型供应商配置时，可直接使用 [references/model-provider-impl-prompt.md](references/model-provider-impl-prompt.md) 中的实现 Prompt。
- **沉淀新卡**：相关任务 close 后，从 SUMMARY 提炼动机 / 参与者 / 落地件 / 边界 / 先例，写成 `references/<pattern>.md` 并登记进下方索引；一处先例不足以成卡，至少两处独立落地或一次落地 + 一次明确复用意图。
- **改卡**：新先例推翻卡内结论时更新对应卡，并在卡内记录更正；模式卡不保存任务过程细节，过程看任务 SUMMARY。

## 模式索引

| 模式 | 一句话 | 模式卡 | 先例 |
| --- | --- | --- | --- |
| agent 数据接入 | 应用提供 API Key + 全接口授权 + 设置页话术，agent 经通用操作规范管理应用数据 | [references/agent-api-access.md](references/agent-api-access.md) | 3 处独立落地，详见模式卡 |
| 模型供应商管理 | 从 models.dev 加载并多选实例模型，消费端（默认/任务/会话）两级联动选择 | [references/model-provider-management.md](references/model-provider-management.md) | 2 处独立落地，详见模式卡 |
| 接口访问统计 | 异步有界采集 + 路由归一化 + 5 端点只读统计 + API Key 专项与零明文门禁 | [references/api-access-stats.md](references/api-access-stats.md) | 14 处独立落地，详见模式卡 |
