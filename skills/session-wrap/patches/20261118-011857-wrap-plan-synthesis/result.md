# Result

- target: skills/session-wrap
- mode: update
- patch: 20261118-011857-wrap-plan-synthesis
- risk: medium
- status: applied
- applied-at: 2026-11-18T01:20:00+08:00

## Validation

- `git apply --check --recount --reverse`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/session-wrap/tests tests/test_evals_structure.py -q`，16 passed
- repository checks: `make check-style` 0 条告警；`make check-names` 无命中
- full tests: `python3 -m pytest skills -q`，551 passed、3 skipped、2 subtests passed
- size: `SKILL.md` 7976 字节，低于 8KB 告警线

## Notes

- 输出改成四块加恢复入口；「待你确认」由方案的一次确认取代。
- 三档边界：默认完成的收尾记账、一次确认的方案步骤、逐项授权的风险动作。
- 额外缺口未点名时写入 `context/current.md`「未决问题」，不建任务、不代写 SUMMARY。
- 细则下沉 `references/plan-synthesis.md`，正文保留触发、分档要点与模板。
- 变更坐在 `task/session-wrap` 分支上，尚未提交。
