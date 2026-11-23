# 打通前端脚手架与 ui-kit 默认 UI 总入口的路由衔接

- target: skills/project-init
- mode: update
- patch: 20261123-201200-connect-ui-kit-frontend
- risk: low
- status: proposed

## Intent

在 `references/frontend.md` 明确 React 模板路线交由 `ui-kit`，后续 UI 路线分派也经 `ui-kit`（通用路线仍由 `pretty-ui` 承接）。

## Conflict check

none（ui-kit 已声明与 project-init 的分工，本 patch 补齐反向指针）。

## Rationale

解决新建 React 前端项目时 project-init 绕过 ui-kit 总入口与模板路线的双入口分叉。

## Files

- `skills/project-init/references/frontend.md`：补充 React 模板路线与后续 UI 设计语言对 ui-kit 的路由指针
- `skills/project-init/tests/test_project_init_contract.py`：新增 frontend.md 含 ui-kit 与 ui-template.lock.json 的守卫断言

## Validation

- `git apply --check --recount skills/project-init/patches/20261123-201200-connect-ui-kit-frontend/change.patch`
- `python3 -m unittest discover -s skills/project-init/tests -p 'test_*.py'`
- `make check-style && make check-names`
