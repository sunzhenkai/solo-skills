# Result：ui-kit 默认总入口与双路线分派

## Outcome
`ui-kit` 现为默认 UI 总入口，按既有技术栈与模板使用情况选择唯一主承接方。通用路线交 pretty-ui；React 模板路线保留既有代码、lock、白名单与像素保真合同。风格包、专项 skills、taskrail 和 reviewer 的承接关系均有正文与测试。

## Verification
- 聚焦路由、pretty-ui、taskrail、reviewer 与跨引用测试：95 passed。
- `python3 -m pytest skills tests -q`：620 passed, 3 skipped, 2 subtests passed。
- `make check-names` / `make check-style` / `make check-deps`：通过。
- `git diff --check`：通过。

## Notes
没有新增依赖或多框架组件实现；已有模板 init / customize / verify / update 行为不变。
