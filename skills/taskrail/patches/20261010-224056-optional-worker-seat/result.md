# Result

- patch: 20261010-224056-optional-worker-seat
- status: applied
- risk: medium

## What changed

- `references/contract.md`：新增精简「执行座位」（约 15 行）：推荐派出表仅 explore/design/apply；宿主 subagent 抽象；非强制；Digest 回收；grill/闸口留主会话；checkbox 归属写清。
- `SKILL.md`：主循环一句接入；硬边界非强制。
- `tests` / `evals`：最小守卫。

## Review incorporation（claude-opus-5-5-medium）

已按评审删减 / 修正：

- 删除独立 `worker-brief.md`、CONTEXT 术语、YAML Brief、reviewer 座位、过宽推荐表。
- 未改动 `explore 关键` 闸口措辞。
- 补：grill 提问留主会话；`write_paths` 含 apply 业务代码；checkbox 与 `TASK.md` 回写分工。

## Validation

- `git apply --check`：通过（应用前）。
- `python3 -m pytest skills/taskrail/tests -q`：27 passed。
- `git diff --check`（生产文件）：通过。

## Notes

- 未改 task-explore / taskflow；契约为真源。
- 未 commit / sync。
