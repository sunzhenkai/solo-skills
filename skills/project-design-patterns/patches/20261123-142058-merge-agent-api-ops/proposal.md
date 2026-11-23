# 把 agent-api-ops 并入 project-design-patterns 作为引用件

- target: skills/project-design-patterns
- mode: update
- patch: 20261123-142058-merge-agent-api-ops
- risk: medium
- status: proposed

## Intent

把独立 skill `skills/agent-api-ops` 并入 `skills/project-design-patterns`，正文改为 `references/agent-api-ops.md` 引用件，契约测试迁入同 skill 的 `tests/` 并改写断言。安装/升级与版本声明统一走 `project-design-patterns`（1.1.0）：应用话术只装一个 skill，模式库自带可执行规范。

非目标：操作流程、凭证落盘约定、认证与 401/403/429 语义、文档获取优先级、操作纪律不变。

## Conflict check

- 仓内引用：README 清单、模式卡、pattern 契约测试均指向旧独立 skill；本轮同步修改。`archive/README.md` 旧名链 `app-api-ops → agent-api-ops` 改为 `→ project-design-patterns`，否则 `tests/test_cross_skill_refs.py` 的 RegistryTest 会因后继名不在役而失败。
- 仓外引用：hela 的接入话术、`/skill.md`、README 与契约测试，dotfiles 编目；本轮同步（见 result.md）。
- 依赖组：本变更只在 project-design-patterns 内部新增 `references` 链接，不新增跨 skill 相对链接，README「依赖组」无需登记。

## Rationale

`agent-api-ops` 的定位一直是 project-design-patterns 模式卡的操作规范件（description 与 README 均自称内部 reference skill）。合并后安装单元只剩一个，版本线与模式库一致，避免两个 skill 的版本漂移与话术里的两步安装。代价是操作规范的版本粒度变粗（随 skill 版本），由「应用声明最低期望版本」机制覆盖：模式库新增卡片造成的版本增长不会强制应用升级。

## Files

- `skills/agent-api-ops/SKILL.md` → `skills/project-design-patterns/references/agent-api-ops.md`（去 skill frontmatter，版本协议改 skill 级）
- `skills/agent-api-ops/tests/test_agent_api_ops_contract.py` → `skills/project-design-patterns/tests/`（断言改写）
- `skills/project-design-patterns/SKILL.md`（version 1.1.0、description、直链引用件）
- `skills/project-design-patterns/references/agent-api-access.md`（操作规范节、版本化说明、先例行、更正记录）
- `skills/project-design-patterns/tests/test_project_design_patterns_contract.py`（安装命令断言）
- `README.md`、`archive/README.md`（仓库级，按 patch 协议不入 change.patch，记入 result.md）
- 仓外：hela（话术 / `skill.md` / 契约测试 / README）、dotfiles（`skills.yaml`；lock 待重锁）

## Validation

- 应用后：`python3 -m pytest skills tests -q`；`make check-style`；`make check-names`
- 布局：SKILL.md 直链 `references/agent-api-ops.md` 可解析；旧独立 skill 目录不再存在
- hela：`go test ./internal/handler/`；desktop 话术单测
