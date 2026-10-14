# Proposal：执行座位改为默认派出 + 交接 5 项 + Digest ≤10 行

- target: skills/taskrail
- mode: update
- patch: 20261015-default-dispatch
- risk: medium（行为从「推荐」变「默认」）
- status: applied

## Intent

原执行座位写「派出是推荐，不是强制」，simple 的 explore 与 wizard 均在主会话，实际多数活串行堆在主上下文。参照 Anthropic multi-agent research（交接写清目标 / 输出格式 / 工具 / 边界；按复杂度定规模；结果落盘回传引用）改为：

- 默认派出；无能力仍自做不停下；有能力不派须写一句理由。
- 新增 wizard 意图摸底、评审 / 验证复跑两行；simple explore 也派摸底（grill 提问留主会话）。
- 明确「不派」：闸口、提问、<30 行或一句话的活、拆不开的步骤；规模上限 simple 1 / medium 3 / complex 5。
- 交接契约 5 项；Digest ≤10 行（结论 / 路径 / 未决 / 置信度）。

非目标：不改闸口、完成门、taskflow implementer-isolation。
