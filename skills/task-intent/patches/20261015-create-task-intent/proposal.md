# Proposal：新建 task-intent（开工前意图确认）

- target: skills/task-intent
- mode: create
- patch: 20261015-create-task-intent
- risk: low（本步不接入任何流程）
- status: applied

## Intent

taskrail wizard 的意图澄清只有一行（phase-wizard 步骤 1），没有「复述给人看」和纠偏循环。新建独立 skill：并行只读摸底 → ≤8 行大白话复述 → human 纠偏循环 / goal 异源强模型代审。

依据：Kiro requirements-first（先出草稿再逐轮确认）、Claude Code AskUserQuestion / plan mode、Anthropic multi-agent research（交接契约、按复杂度定规模）、Clarify When Necessary / EVPI 选题研究（只在影响走向时问）、MT-Bench LLM-as-judge 偏差（异源 + 评分规则）。

非目标：本步不改 taskrail / task-explore / role-based-reviewer。

## 内容

SKILL.md + references（probe / statement-template / correction-loop / goal-review）+ tests（8 条契约）+ evals（21 条）+ examples + experience；README 技能表加一行。
