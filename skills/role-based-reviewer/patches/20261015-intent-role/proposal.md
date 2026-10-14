# Proposal：新增 roles=intent，供 goal 模式审意图复述

- target: skills/role-based-reviewer（连带 taskrail phase-wizard / confirm-protocol 各一句）
- mode: update
- patch: 20261015-intent-role
- risk: low
- status: applied

## Intent

goal 模式开头没人核对「意图是否理解对」。新增 `intent` 角色：只读用户原话、意图复述、摸底 Digest，查添加目标 / 漏约束 / 不可检查 / 假设失当，输出分数 0–1 与通过/不通过（≥0.8 且无 🔴/🟡）。仅调用方显式传入，不参与视角推断（不扩大默认角色）。task-intent goal 模式用 `model=` 指定异源、高一档模型调用；taskrail wizard 第 1 步与确认协议 goal 行同步一句。

## 改动

roles/intent.md（新增）、SKILL.md 合法角色列表、role-vocabulary 一行、constraints redirect 一行（intent ↔ product）、测试 +1 类并把 intent 纳入加厚角色结构检查；taskrail phase-wizard / confirm-protocol / 测试各一句。
