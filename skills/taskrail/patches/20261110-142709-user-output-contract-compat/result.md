# Result

- target: skills/taskrail
- mode: update
- patch: 20261110-142709-user-output-contract-compat
- risk: medium
- status: failed
- applied-at: 2026-11-10T14:28:36+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: taskrail / taskflow 202 passed、2 skipped、2 subtests passed；全仓 562 passed、3 skipped、2 subtests passed、1 failed
- privacy check: pass
- mode check: pass

## Notes

上一组五项兼容失败已修复。全仓剩余失败为 check_output_style 要求 user-report 保留至少三组「前后对比」；check-names / check-style 因命令链在该失败处停止，尚未运行。后续以新 patch 补方法论对照。
