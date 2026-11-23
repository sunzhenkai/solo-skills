# 解除 taskrail 对 ui-kit 与 pretty-ui 的相对路径硬依赖

- target: skills/taskrail
- mode: update
- patch: 20261123-202000-decouple-ui-hard-links
- risk: medium
- status: proposed

## Intent

将 `confirm-protocol.md`、`done.md`、`ui-delivery.md` 中指向 `ui-kit`/`pretty-ui` 的相对链接改为反引号可选文件锚点 + 未安装降级说明，使纯后端/通用用户可只装 taskrail + taskflow。

## Conflict check

配套修改：README「依赖组」、tests/test_cross_skill_refs.py（可选文件锚点静态校验）、role-based-reviewer（同步解耦）。

## Rationale

Web UI 是可选交付类别，不应通过 Markdown 相对链接强制所有 taskrail 用户捆绑安装整套 UI 引擎；同时通过源仓文件锚点测试保住静态防漂移保护。

## Files

- `skills/taskrail/references/confirm-protocol.md`：pretty-ui critique 相对链接改为可选锚点与降级说明
- `skills/taskrail/references/done.md`：pretty-ui 相对链接改为可选锚点与降级说明
- `skills/taskrail/references/ui-delivery.md`：ui-kit/pretty-ui 相对链接改为可选锚点与降级说明
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`：更新断言为可选跨 skill 锚点存在性并禁止相对硬链接

## Validation

- `git apply --check --recount skills/taskrail/patches/20261123-202000-decouple-ui-hard-links/change.patch`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `make check-style && make check-names`
