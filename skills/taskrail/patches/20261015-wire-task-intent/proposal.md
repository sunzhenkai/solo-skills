# Proposal：wizard 第 1 步接入 task-intent（human）

- target: skills/taskrail
- mode: update
- patch: 20261015-wire-task-intent
- risk: low
- status: applied

## Intent

phase-wizard 步骤 1 原为一行「澄清意图」。改为委托 `task-intent`：并行摸底 → 意图复述 → human 纠偏到确认，落 `wizard/intent.md`；确认版「做完的样子」作为 `criterion` 起草来源。契约「进入 explore / design 必须已有」加 `wizard/intent.md`（旧任务不回溯）。

非目标：本步不改 goal 模式（见下一 patch）。

## 改动

SKILL.md 依赖与 wizard 行、phase-wizard 步骤 1、contract 阶段载荷表、1 条测试、1 条 eval。
