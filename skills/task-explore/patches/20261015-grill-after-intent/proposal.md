# Proposal：grill 收窄到意图确认之后

- target: skills/task-explore（references/explore-design.md、commands.md、tests）+ AGENTS.md 一行
- mode: update
- patch: 20261015-grill-after-intent
- risk: low
- status: applied

## Intent

接入 task-intent 后，simple/medium 的「仅 grill」仍写着「澄清目标/判据/范围」，会把用户刚确认的意图再问一遍。改为：`wizard/intent.md` 确认版的目标 / 做完的样子 / 不做 视为已定，grill 只问细节、边界、术语与约束；发现冲突停下回 task-intent 纠偏，不在 grill 里改写意图。

非目标：不改 grill 委托对象（仍为 `grilling`）、不动 gate_lines 锁定句（原句保留，新增句另起一行）。
