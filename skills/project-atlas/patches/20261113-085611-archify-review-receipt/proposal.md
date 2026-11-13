# 明确 Archify review 回执落点

- target: skills/project-atlas
- mode: update
- patch: 20261113-085611-archify-review-receipt
- risk: low
- status: proposed

## Intent

补充真实集成验证发现的契约：Archify 在修复轮使用 `--out-dir` 时，finalize 摘要位于 review 目录。将通过的摘要原样复制为 `diagrams/<slug>.finalize-summary.json`，供 Atlas 持续检查。

## Conflict check

不改变 Archify 的交付过程或 Atlas 校验行为，只明确已有回执检查所需的文件来源。

## Rationale

真实 Archify finalize 已验证该路径行为；文档补充可避免修复后轮误报回执缺失。

## Files

- `skills/project-atlas/references/diagrams.md`：说明 review 摘要的规范落点。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：守卫该约定。

## Validation

- `git apply --check --recount`。
- `python3 -m pytest skills/project-atlas/tests -q`。
