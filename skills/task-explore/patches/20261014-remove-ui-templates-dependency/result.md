# Result：移除对 ui-templates-* 系列 skill 的依赖（task-explore 侧）

改动已落工作树（`change.patch` 由 `git diff HEAD` 生成）。

## 改动文件

`references/approve.md`�`references/commands.md`�`references/explore-design.md`�`tests/gate_lines.txt`�`tests/test_design_contract_and_handoff_gate.py`

## 测试

- `python3 -m pytest skills tests -q` → 494 passed, 3 skipped（改动前 493 passed, 3 skipped；+1 来自同日 ui-overreach-speed 新增断言）。
- `make check-names` → OK。
