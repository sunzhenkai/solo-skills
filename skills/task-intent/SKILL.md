---
id: task-intent
name: task-intent
description: "任务开工前的意图确认：只读探索上下文 → 简洁的「意图复述」（要干嘛 / 怎么干 / 输出什么 / 上下文 / 不做 / 假设）→ 纠偏到用户说对（goal 模式由另一个模型代审）。taskrail wizard 第 1 步调用；用户点名 task-intent 或说「先确认你理解对了没」时使用。"
---

# 任务意图确认

先对齐「要干嘛、怎么干、输出什么」，再动手。探索要详细，输出要简洁。细则、模板与示例见 [references/intent.md](references/intent.md)。

产出：`{taskRoot}/wizard/intent.md`（无任务目录时只在对话里给复述）；探索详情落 `{taskRoot}/evidence/intent/`。确认后的「输出什么 · 做完的样子」是 `criterion` 的起草来源，下游改它只走 taskrail 契约「意图变更」。

## 先定做多少

- 原话已说清改什么、怎么算做完（一句话能描述改动）：只读要改的那处，给一两句复述，照常纠偏。
- resume 时已有 `wizard/intent.md` 且 `status: confirmed` 或 `assumed`：沿用，不重做；human 下 `assumed` 补说一句「我按这个理解继续」。
- 纯问答、不产出改动：直接回答，不走本流程。
- 其余走下面完整流程。

## 流程

1. **探索上下文**：读相关代码 / 配置 / 文档、`tasks/` 历史任务与近期提交，必要时查外部参照；面广时可并行派只读 subagent 分头摸，回简短摘要，详情落 `evidence/intent/`。上下文是复述的一部分。
2. **复述**：先按覆盖清单（要干嘛 / 怎么干 / 输出什么 / 上下文 / 不做 / 假设 / 决定）想清楚，再用 1–3 句第一人称口语告诉用户：做什么、怎么做、产出落在哪、接下来会怎样。说决定、不提问（难回头的单独说、真阻塞才停），见 [user-report.md](../taskrail/references/user-report.md)；有任务目录时决定追加到 `TASK.md`「已做决定」。口语里不打标题、不加粗标签、不逐项列字段；结构化内容只写进 `wizard/intent.md`。由 taskrail wizard 调用时，复述和 plan 要点合成一条消息，在 wizard 定稿那一步发出。
3. **纠偏**：
   - human：停下等用户说对或指出要改的地方；用户没回话不算确认。按指正先回一手资料重查，再说改了什么、出处在哪；用户显出困惑或不满时停止提问，查清后给有出处的结论；多轮仍对不上就把两种理解并排说清、写明我按哪种做。
   - goal：不问人，按 [confirm-protocol.md](../taskrail/references/confirm-protocol.md)「另一个模型审」派审，清单用 references 第 5 节，无 P0 / P1 即通过。
4. **落盘**：确认版写 `wizard/intent.md`，`status: confirmed`（goal 两轮审不过时 `assumed`，剩余发现写进假设）。

## 守住这几条

- 注意任务边界：范围默认目标加它的直接依赖，细则见 [references/intent.md](references/intent.md) 第 1、4 节。
- 复述忠于用户原话：目标照原话、约束一条不少、宽泛目标保持宽泛；「不做」只写原话里的限制，自己想加的写进「我的假设」；不确定处写成假设。
- 本 skill 只读探索；写代码留给后续阶段。
