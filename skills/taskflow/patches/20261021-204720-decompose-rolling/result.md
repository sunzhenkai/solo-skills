# Result

- target: skills/taskflow
- mode: update
- patch: 20261021-204720-decompose-rolling
- risk: high
- status: applied
- applied-at: 2026-10-21T20:50:00+08:00

## Validation

- `git apply --check --recount`: pass。应用前逐文件核对了基线；应用后的结果与候选稿逐文件一致。
- `git diff --check`: pass
- target tests: 全量 `python3 -m pytest skills tests -q` 结果为 470 passed, 3 skipped。本 patch 新增 5 条（`test_rolling_wave_contract.py`）；`test_check_handoff.py` 里逃生口用例的 phase 值改为 design，结果不变。
- `make check-style`: OK，0 条告警
- privacy check: pass
- mode check: pass

## Notes

- 体量：SKILL.md 从 4449 B 增到 4666 B；driver-template.md 从 5497 B 增到 6691 B。
- evals 从 22 条增到 23 条。
- 只应用到工作树，没有暂存，也没有提交。
