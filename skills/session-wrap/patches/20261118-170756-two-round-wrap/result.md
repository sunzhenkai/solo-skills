# Result

- target: skills/session-wrap
- mode: update
- patch: 20261118-170756-two-round-wrap
- risk: high
- status: applied
- applied-at: 2026-11-18T17:10:00+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/session-wrap/tests tests/test_evals_structure.py -q`，19 passed
- full tests: `python3 -m pytest skills tests -q`，591 passed、3 skipped、2 subtests passed
- repository checks: `make check-style` 0 条告警；`make check-names` 无命中
- size: `SKILL.md` 8033 字节，低于 8KB 告警线
- privacy check: pass
- mode check: pass

## Notes

- 收尾改为两轮：第一轮收尾清单（将直接执行 / 需你选择 / 缺口及落点），不下结论；确认后执行，第二轮输出结论、收尾结果、缺口列表与恢复入口。
- 缺口落点按执行时的任务状态取，补上已归档任务的落点：SUMMARY「剩余风险与后续项」追加一行。
- 为留在 8KB 内，删去正文中与第 3 步「清理」、第 7 步「缺口」重复的两句，约束本身仍在。
- 仓库 `README.md` 的 skill 一行简介同步更新，属仓级文档，不在本 patch 内。
- 变更在 `task/session-wrap-two-round` 分支的 worktree 上，尚未提交。
