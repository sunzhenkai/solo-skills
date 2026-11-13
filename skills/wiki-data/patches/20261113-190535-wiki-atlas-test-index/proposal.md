# 修正 Atlas 链接测试的索引步骤

- target: skills/wiki-data
- mode: update
- patch: 20261113-190535-wiki-atlas-test-index
- risk: low
- status: proposed

## Intent

让新增 Atlas 相对链接测试遵循既有索引契约，先生成索引再检查，不改变生产行为。

## Conflict check

仅修正上一补丁测试夹具的步骤；保留链接断言与全部生产规则。

## Rationale

`lint_wiki` 默认检查索引一致性。测试需要先执行 `--write-index`，再以 `--check-index` 验证链接和索引均无错误。

## Files

- `skills/wiki-data/tests/test_lint_wiki.py`：补齐索引生成与检查步骤。

## Validation

- `git apply --check --recount` 校验补丁。
- 应用后运行 `git diff --check -- skills/wiki-data`。
- 运行 `python3 -m pytest skills/wiki-data/tests -q`。
