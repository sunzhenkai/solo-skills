---
id: task-intent
name: task-intent
description: "任务开工前的意图确认：并行只读摸底 → 一张不超过 8 行的大白话「意图复述」→ 纠偏循环直到用户说对（goal 模式由异源强模型代审）。由 taskrail wizard 第 1 步委派；用户点名 task-intent 或说「先确认你理解对了没」时也可用。一句话能说清的小改、纯问答、已有冻结方案的 resume 不要用。"
---

# 任务意图确认

先确认「人要什么」，再谈「怎么做」。细节、边界与术语留给 task-explore 的 grill。

产出：`{taskRoot}/wizard/intent.md`（无任务目录时只在对话里给复述）。确认后的「做完的样子」作为 `criterion` 的起草来源，下游不得无声改写。

## 流程

1. **摸底**（只读，按 [references/probe.md](references/probe.md)）：按档位并行派 subagent——simple 1 个、medium 2–3 个、complex 3–4 个；每个回 Digest ≤10 行，详情落 `evidence/intent/`。宿主无 subagent 时主会话按同一分工自做。
2. **复述**（按 [references/statement-template.md](references/statement-template.md)）：≤8 行、6 个字段、大白话；假设标「把握高/低」；最多 1 个要拍板的问题且附推荐答案。
3. **纠偏**：
   - human：给用户看复述，按 [references/correction-loop.md](references/correction-loop.md) 循环到确认。
   - goal：不问人，按 [references/goal-review.md](references/goal-review.md) 派异源强模型审（`role-based-reviewer roles=intent`）。
4. **落盘**：确认版写 `wizard/intent.md`，含轮次与最终状态（`confirmed` / `assumed`）。

## 不可跳过

- 先查后问：能从仓库、历史任务、对话推出的不问；问必带推荐答案。
- 只在歧义会改变做法或范围时提问；否则写成「我的假设」继续。
- 复述必须忠于用户原话：不添目标、不漏约束；不确定处写成假设，不写成事实。
- 面向人的输出不用内部术语（phase、gate、Digest 等）；必须用时括号白话释义。
- 涉及线上、不可逆、对外发送的意图，goal 模式也必须停下等人。
- 不写实现方案、不写代码；摸底 subagent 只读。

## 何时跳过

（taskrail 契约执行座位引用本节，唯一真源。）

simple 档且用户原话已含明确目标与完成标准（一句话能描述改动）：直接出复述并请确认，不派摸底。resume 已有 `wizard/intent.md` 且 `status: confirmed` 或 `assumed` 时不重做；human 模式下 `assumed` 只补问一次「对吗」。
