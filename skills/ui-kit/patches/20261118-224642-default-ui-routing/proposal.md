# Proposal：ui-kit 默认总入口与双路线分派

## Intent
把 ui-kit 从 React 模板专用说明调整为默认 UI 总入口。既有/非 React 项目沿用原技术栈并交 pretty-ui；React 模板项目保留固定版本复制、lock、白名单与像素保真。衔接模板风格包、可选专项 skills、taskrail 与 role-based-reviewer。

## Files
- `skills/ui-kit/SKILL.md`
- `skills/ui-kit/tests/test_ui_kit_contract.py`
- `README.md`（界面定位、安装示例与跨 skill 依赖组）

## Tests
- ui-kit 契约测试覆盖默认入口、点名优先级、非 React、模板风格包、专项与编排分派。
- 跨 skill 相对链接在 README 依赖组登记且可解析。

## Non-goals
不新增多框架组件库，不改变模板代码和既有 init/customize/verify/update 合同。
