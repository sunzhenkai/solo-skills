---
id: task-intent
name: task-intent
description: "任务开工前的意图确认：详细只读探索上下文 → 一份简洁清晰的「意图复述」（要干嘛 / 怎么干 / 输出什么 / 上下文 / 不做 / 假设）→ 纠偏到用户说对（goal 模式由异源模型代审）。由 taskrail wizard 第 1 步委派；用户点名 task-intent 或说「先确认你理解对了没」时也可用。一句话能说清的小改、纯问答、已有确认意图的 resume 不要用。"
---

# 任务意图确认

先对齐「要干嘛、怎么干、输出什么」，再动手。探索要详细，输出要简洁。细则、模板与示例见 [references/intent.md](references/intent.md)。

产出：`{taskRoot}/wizard/intent.md`（无任务目录时只在对话里给复述）；探索详情落 `{taskRoot}/evidence/intent/`。确认后的「输出什么 · 做完的样子」是 `criterion` 的起草来源，下游不得无声改写。

## 流程

1. **探索上下文**：读相关代码 / 配置 / 文档、`tasks/` 历史任务与近期提交，必要时查外部参照；面广时可并行派只读 subagent 分头摸，回简短摘要，详情落 `evidence/intent/`。上下文是复述的一部分，不是可省的前置。
2. **复述**：先按覆盖清单（要干嘛 / 怎么干 / 输出什么 / 上下文 / 不做 / 假设 / 决定）想清楚，再用 1–3 句第一人称口语告诉用户：做什么、怎么做、产出落在哪、接下来会怎样。说决定、不提问（含难回头单独说、真阻塞才停），见 [user-report.md](../taskrail/references/user-report.md)；有任务目录时决定追加到 `TASK.md`「已做决定」。不打标题、不加粗标签、不逐项列字段；结构化内容只写进 `wizard/intent.md`。
3. **纠偏**：
   - human：给用户看复述，按指正先回一手资料重查，再说改了什么、出处在哪，直到用户明确说对；用户显出困惑或不满时立刻停止提问，查清后给有出处的结论；多轮仍对不上就把两种理解并排说清、写明我按哪种做。
   - goal：不问人，派异源模型审（`role-based-reviewer roles=intent`），无 P0/P1 即通过，见 references。
4. **落盘**：确认版写 `wizard/intent.md`，`status: confirmed`（goal 审不过时 `assumed` + 显式降级）。

## 不可跳过

- 注意任务边界。细则见 [references/intent.md](references/intent.md) 第 1、4 节。
- 先查后定；说决定、不提问；真阻塞才停：见 [user-report.md](../taskrail/references/user-report.md)「说决定，不提问」。
- 复述必须忠于用户原话：不添目标、不漏约束、不把宽泛目标缩窄；「不做」只写用户原话里的限制，自己想加的写进「我的假设」；不确定处写成假设，不写成事实。
- 涉及线上、不可逆、对外发送的意图，goal 模式也必须停下等人。
- 不写代码；探索只读。
- 用户没回话不算确认。

## 何时跳过

（taskrail 契约引用本节，唯一真源。）simple 档且用户原话已含明确目标与完成标准（一句话能描述改动）：不做大范围探索，直接出简短复述。resume 已有 `wizard/intent.md` 且 `status: confirmed` 或 `assumed` 时不重做；human 模式下 `assumed` 只补说一次「我按这个理解继续」。
