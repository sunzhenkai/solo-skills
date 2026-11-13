# 集成 Archify 交互图

- target: skills/project-atlas
- mode: update
- patch: 20261113-084454-archify-diagrams
- risk: medium
- status: proposed

## Intent

把 Archify 作为可选绘图后端：Atlas 维护 `diagrams/<slug>.json` 图源与交互 HTML 的关联，构建时只发布 HTML，并在页面复核前检查 Archify 交付回执、pending/lock 状态和源/产物摘要。普通 Markdown 文档与现有静态资源流程保持不变。

## Conflict check

Archify 负责图生成和质量检查，Atlas 负责金字塔导航与源码新鲜度，职责无重叠。现有 `assets/` 静态 HTML 继续兼容；不新增强制 Node.js 依赖，不包装 Archify CLI 或复制其 schema。

## Rationale

同名 JSON/HTML 提供可增量维护的图源；delivery 与 finalize 回执中的 specification/artifact SHA-256 可确定性发现绕过 `finalize` 的修改。页面链接作为页面到图的关联，避免第二份映射台账。该行为可由临时 Atlas 端到端测试验证。

## Files

- `skills/project-atlas/SKILL.md`：声明可选依赖、目录和绘图入口。
- `skills/project-atlas/references/diagrams.md`：新增 Archify 类型路由、生成和修复契约。
- `skills/project-atlas/references/layout.md`：补充图链接约定。
- `skills/project-atlas/references/maintenance.md`：接入源码变化后的图复核。
- `skills/project-atlas/scripts/atlasctl.py`：发布图 HTML，校验回执与摘要，输出受影响图并守住页面复核。
- `skills/project-atlas/tests/test_atlasctl.py`：覆盖图构建、回执、篡改和未完成交付。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：守卫 Archify 文档契约。
- `skills/project-atlas/evals/cases.yaml`：增加源码变化触发的图修复案例。

## Validation

- `git apply --check --recount` 通过后再应用。
- `python3 -m pytest skills/project-atlas/tests -q`。
- `python3 -m pytest skills -q`、`make check-names`、`make check-style`。
- 真实 CLI 冒烟：Archify 图只发布 HTML，篡改 JSON 后 `verify` 与 `check` 失败，重新生成匹配回执后恢复。
