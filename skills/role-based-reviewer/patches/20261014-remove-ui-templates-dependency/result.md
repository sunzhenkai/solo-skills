# Result：移除对 ui-templates-* 系列 skill 的依赖（role-based-reviewer 侧）

改动已落工作树（`change.patch` 由 `git diff HEAD` 生成）。

## 改动文件

`references/constraints.md`�`references/roles/design.md`

## 测试

- `python3 -m pytest skills tests -q` → 494 passed, 3 skipped（改动前 493 passed, 3 skipped；+1 来自同日 ui-overreach-speed 新增断言）。
- `make check-names` → OK。
