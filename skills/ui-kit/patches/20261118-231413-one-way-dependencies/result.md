# Result：ui-kit 单方持有路由依赖

## Outcome
ui-kit 明确依赖只由上游编排方指向下游能力，独立下游不反向引用 ui-kit。ui-template 仓库已恢复零 diff，pretty-ui 不再感知 ui-kit；既有分派和验收行为保留。

## Verification
- 聚焦测试与跨引用检查：77 passed。
- 全仓：621 passed, 3 skipped, 2 subtests passed。
- check-names / check-style / check-deps 与 diff check：通过。
- ui-template 三个独立 SKILL.md 扫描不到 ui-kit；模板仓 make check 46 tests OK，1 个可选测试跳过，工作树干净。
