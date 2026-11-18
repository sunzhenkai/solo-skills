# 收窄 project-atlas 的持久化路由

- target: skills/project-atlas
- mode: update
- patch: 20261118-235654-scope-atlas-description
- risk: high
- status: proposed

## Intent

把 description 的触发条件限定为建立、更新或复核持久化 Atlas，保留项目知识地图、架构与业务文档、Atlas 静态站点和过期页面修复分支。一次性项目问答仍由 project-explore 承接，普通静态站点仍由 UI 路由承接；本次不改变 Atlas 的执行流程和产物契约。

## Conflict check

与 project-explore 的一次性问答边界及 ui-kit 的静态站点职责保持一致；不修改下游 Skill，不新增跨 Skill 引用。

## Rationale

原触发词「业务逻辑梳理」「静态站点」缺少 Atlas 限定，容易把相邻 Skill 的请求路由到持久化文档流程。收窄后的分支均可通过 frontmatter 文本契约检查。

## Files

- `skills/project-atlas/SKILL.md`：收窄 description 的 WHAT + WHEN。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：守护持久化 Atlas 的触发分支。

## Validation

- `git apply --check --recount` 校验 patch。
- 运行 project-atlas 契约测试。
- 运行 `make check-style`、仓级检查与全量测试。
