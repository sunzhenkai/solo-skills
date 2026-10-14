# Proposal：补齐意图闭环的 10 条缺口（跨 skill）

- target: skills/taskrail、task-intent、task-explore、taskflow、role-based-reviewer
- mode: update
- patch: 20261015-intent-loop-gaps
- risk: medium（完成门新增第 8 条；新增意图变更规则）
- status: applied

## Intent

审计发现：意图只在 wizard 流入 criterion，交付不回看；中途改意图无路径；goal 评审不可用时两份文件矛盾。修复：

1. 评审不可用：由 task-intent 先判断；不可用则不调 rbr、登记降级后自审；rbr「禁止同源自审」注明该例外。
2. contract 新增「意图变更」：重跑 task-intent → version+1 → 确认协议显式改 criterion → phase 回退 / 已交接走 taskflow 修订子 change；explore-design 冲突处指向它。
3. 完成门第 8 条对照 intent.md；验收 rubric 随附 intent.md。
4. wizard 定稿核对 criterion 与「做完的样子」一致。
5. taskflow 并行条款指向执行座位（交接 5 项、Digest）。
6. 目录树补 `wizard/intent.md`、`evidence/intent/`。
7. resume 时 `assumed` 也不重做（human 补问一次）。
8. 确认协议 goal 行的意图通过线指向 goal-review。
9. simple 跳过摸底条件单一真源（task-intent「何时跳过」）。
10. taskrail evals 加 `intent-closed-loop`、`intent-change-mid-task`。

另：intent.md 模板加 `version` 与「历史版本」；rbr「严重级别」原句下沉到 `references/severity.md` 以保持 SKILL.md ≤8192 B。
