# Result

- target: agents/skills/task-explore（现 `skills/task-explore`）
- mode: update
- patch: 20260925-064334-goal-confirm-via-review
- risk: high
- status: applied
- applied-at: 2026-09-25T06:51+08:00（`dotfiles f873970 fix task-wizard goal`，同批落下 task-explore 与 task-wizard 两侧）
- retargeted-at: 2026-09-29T17:25+08:00（`solo-skills cd1d135 task-goal: 新建承接 goal 执行协议`）
- closure: **retroactive**（补记于 2026-09-29；应用当时未写 result.md）

## Validation

判据以 `git log -S` 为准（文本落地率会误判，见姊妹条目 `task-wizard/20260925-064335` 的教训）：
探针句「冻结未决并交接时，审阅收敛即「按推荐冻结并交接」」在 `f873970` 进入历史，即内容确曾落到生产稿。

辅助核查——取 `change.patch` 全部新增行（≥12 非空字符）比对当前 skill 树：

- 落地 18/22 行。
- 未逐字命中的 4 行已定性，均非"漏应用"：
  1. `description:` 行 —— 该句后被多次改写，现生产稿仍含「处在 goal 里时，向用户确认的决定改走 …审阅，不列选项」。
  2. 「都改为走 **task-wizard** 的『审阅』」 —— 机制保留，委派对象被 `patches/20260929-goal-confirm-via-task-goal` 重定向为 **task-goal**（生产稿 `SKILL.md:19`）。
  3. 派审/收敛那一句 —— 同上，随重定向改写。
  4. `self.assertIn("走 task-wizard 的「审阅」", section)` —— 契约测试断言随第 2 条同步改写。

## Notes

本 patch 引入的规则（goal 里不向用户列选项、改走审阅；审阅收敛即本轮 `decide` 完立刻 `handoff`）已在生产稿生效，
是 `task-goal` 拆分前的第一版实现。审阅的归属后来从 task-wizard 迁到 task-goal，属后续架构决定，不否定本 patch。
