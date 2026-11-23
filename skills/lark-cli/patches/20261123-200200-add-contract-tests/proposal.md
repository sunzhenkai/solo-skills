# 补齐 lark-cli 文本契约测试

- target: skills/lark-cli
- mode: update
- patch: 20261123-200200-add-contract-tests
- risk: low
- status: proposed

## Intent

为全仓唯一缺少单测的 lark-cli 补齐 stdlib unittest 契约测试，锁定手动触发、三道防膨胀门禁、禁止全局安装上游 lark-* 与 catalog 存在性。

## Conflict check

none

## Rationale

防止后续编辑意外削弱防上下文膨胀门禁或删除 disable-model-invocation 声明。

## Files

- `skills/lark-cli/tests/test_lark_cli_contract.py`：新增 lark-cli 文本契约测试

## Validation

- `git apply --check --recount skills/lark-cli/patches/20261123-200200-add-contract-tests/change.patch`
- `python3 -m unittest discover -s skills/lark-cli/tests -p 'test_*.py'`
- `make check-style && make check-names`
