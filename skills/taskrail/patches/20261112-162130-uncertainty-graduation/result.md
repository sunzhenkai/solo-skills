# Result

- target: skills/taskrail
- mode: update
- patch: 20261112-162130-uncertainty-graduation
- risk: medium
- status: failed
- applied-at: 2026-11-12T16:21:30+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/taskrail/tests -q` failed：1 failed, 146 passed, 2 skipped, 2 subtests passed
- privacy check: pass
- mode check: pass

## Notes

`ReferenceContractTest.test_router_uses_evidence_and_prevents_oscillation` 失败：正文第三步把既有锚点“当前最关键不确定性”改成了“当前关键不确定性”。后续修复应在新 patch 中恢复“当前最关键不确定性”原文，不放宽既有测试。

候选稿新增测试先行通过：`test_uncertainty_contract.py` 与 `test_grill_self_answer.py` 共 7 passed。`make check-names` 和 `make check-style` 均通过。完整 `python3 -m pytest skills -q` 在 taskrail 测试失败后未运行。
