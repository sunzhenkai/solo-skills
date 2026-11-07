# 保留 TASK 模板的 handoff 兼容示例

- target: skills/taskrail
- mode: update
- patch: 20261107-081107-template-compat
- risk: low
- status: proposed

## Intent

修复上一 patch 引入的模板兼容回归。实际新建根任务仍由脚本写 `current_ref: intake`；通用 TASK 模板保留 `current_ref: plan` 作为意图已确认后的示例，供 taskflow 现有模板兼容测试替换为 execute。context 模板继续携带意图确认状态。

## Conflict check

不改变新任务入口、确认规则或 taskflow。模板顶部说明示例所处状态，避免被理解为新建任务直接从 plan 开始。

## Rationale

taskflow 测试从 TASK 模板提取内容并替换 `current_ref: plan`；保持这一既有契约比同步扩大修改面更小。脚本状态测试已机械守卫实际入口为 intake。

## Files

- skills/taskrail/references/templates.md：标明 TASK 示例为意图确认后的状态并恢复 plan 示例。
- skills/taskrail/tests/test_explore_contract.py：恢复模板兼容断言并守卫示例说明。

## Validation

- `git apply --check --recount`。
- `python3 -m pytest skills/taskrail/tests -q`。
- `python3 -m pytest skills -q`。
- `make check-names && make check-style`。
