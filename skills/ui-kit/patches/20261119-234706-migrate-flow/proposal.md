# 已有项目迁入模板的流程

- target: skills/ui-kit
- mode: update
- patch: 20261119-234706-migrate-flow
- risk: medium
- status: proposed

## Intent

补上「已有 React 项目接入模板路线」这条缺失的流程：盘点现状、非 `--init` 安装、骨架替换、逐页替换并删旧件、落差适配、按 verify.md 验收、逐页提交回滚。

同时删掉 SKILL.md 里「已有项目迁入模板尚未支持」这句已失效的说明，改为指向本页；测试从「不许声称已支持」正过来，守卫新页面存在且不含与流程矛盾的做法。

非目标：不改模板仓的安装脚本与组件，不改新项目 init 与升级流程，不引入后端或数据层契约。

## Conflict check

与 init.md 的 `--init` 路径按「新项目 / 已有项目」分工，本页显式要求已有项目不用 `--init`。与 update.md 不重叠：升级管锁与三方合并，本页管首次接入。与 verify.md 的完成条件一致，本页只追加迁移专属确认项。

## Rationale

流程来自一个真实迁移（React 19 + Tailwind 4 + 三个页面的项目）：dev server 把 API 前缀整体代理导致深链接 404、一次改多个 URL 参数被覆盖、页脚每页选择器窄屏折行、单 tab 折叠区没有信息量。这些都不是模板新项目会遇到的问题，写进新页面最省事。

## Files

- skills/ui-kit/references/migrate.md：新增迁移流程与落差处理
- skills/ui-kit/SKILL.md：路由表加迁移一行，删掉「尚未支持」，完成句覆盖
- skills/ui-kit/tests/test_ui_kit_contract.py：`test_migration_not_claimed` 改为 `test_migration_route`，新增 `test_migrate`，引用清单加 migrate.md

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 skills/ui-kit/tests/test_ui_kit_contract.py`；`make check-style`；`make check-names`；`python3 -m pytest tests -q`
