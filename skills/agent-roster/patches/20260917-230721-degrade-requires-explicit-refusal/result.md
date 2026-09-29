# Result

- target: skills/agent-roster
- mode: update
- patch: 20260917-230721-degrade-requires-explicit-refusal
- risk: high
- status: applied
- applied-at: 2026-09-17T23:09:54+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: not-available
- privacy check: pass
- mode check: pass

## Notes

门禁改动经使用者确认后应用。应用后核对：`SKILL.md` 委派段为四态（含「还没回答 → 不得改走降级」），不变量含「未获明确拒绝不得降级；上一次用过降级不构成本次豁免」；契约降级段以「进入条件」开头；frontmatter `name` 仍为 `agent-roster`。

上一轮 patch 遗留的缺口（仓库根 `README.md`「执行层」段把降级读成对等路径）已在本轮同时修掉，但该文件不在 skill 目录内，按协议不进 `change.patch`，是 patch 之外的独立编辑。

触发本轮的真实失败：门禁应用后的下一次委派仍直接宣布「沿用既有降级路径」，未提议安装。该失败应在使用者侧数据目录记一条 Trace（使用者纠正了执行器决定），不写入本仓库。
