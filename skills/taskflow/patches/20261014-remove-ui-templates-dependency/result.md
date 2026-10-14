# Result：移除对 ui-templates-* 系列 skill 的依赖（taskflow 侧）

改动已落工作树（`change.patch` 由 `git diff HEAD` 生成）。

## 改动文件

`SKILL.md`�`evals/cases.yaml`�`references/acceptance-rubric.md`�`references/delivery-quality-loop.md`�`references/driver-template.md`�`references/execution-discipline.md`�`tests/test_execution_spine_contract.py`

## 测试

- `python3 -m pytest skills tests -q` → 494 passed, 3 skipped（改动前 493 passed, 3 skipped；+1 来自同日 ui-overreach-speed 新增断言）。
- `make check-names` → OK。
