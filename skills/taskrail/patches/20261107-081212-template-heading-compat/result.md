# Result

- target: skills/taskrail
- mode: update
- patch: 20261107-081212-template-heading-compat
- risk: low
- status: applied
- applied-at: 2026-11-07T08:13:22+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- compatibility test: `python3 -m pytest skills/taskflow/tests/test_check_handoff.py::TestTemplateCompat::test_new_template_can_be_prepared_for_gate -q` — 1 passed
- target tests: `python3 -m pytest skills/taskrail/tests -q` — 139 passed, 2 skipped, 2 subtests passed
- repository tests: `python3 -m pytest skills -q` — 522 passed, 3 skipped, 2 subtests passed
- repository checks: `make check-names` and `make check-style` — pass, 0 warnings
- privacy check: pass
- mode check: pass

## Notes

说明文字位于 TASK 标题前，taskflow 模板提取兼容。实际新建根任务仍为 intake，意图确认状态为 pending。未修改 taskflow、安装镜像，未 commit 或 push。
