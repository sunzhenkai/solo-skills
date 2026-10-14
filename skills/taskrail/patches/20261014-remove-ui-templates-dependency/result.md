# Result：移除对 ui-templates-* 系列 skill 的依赖（taskrail 侧）

改动已落工作树（`change.patch` 由 `git diff HEAD` 生成）。

## 改动文件

`SKILL.md`�`evals/cases.yaml`�`references/contract.md`�`references/gate-packs.md`�`references/glossary.md`�`references/phase-wizard.md`�`tests/test_confirm_reviewer_binding_contract.py`�`tests/test_deliverable_class_contract.py`

## 测试

- `python3 -m pytest skills tests -q` → 494 passed, 3 skipped（改动前 493 passed, 3 skipped；+1 来自同日 ui-overreach-speed 新增断言）。
- `make check-names` → OK。
