# 增加 token 与组件统一的 UI 工程化检查

- target: skills/pretty-ui
- mode: update
- patch: 20261031-082315-ui-engineering
- risk: medium
- status: proposed

## Intent

在 system 模式下增加 UI 工程化分支，覆盖项目初建与已有项目架构优化：

- init：沿用现有技术栈与命名，补齐语义 token、当前所需组件契约和证据页，不生成整套组件库。
- audit：默认只读，盘点 token 漂移、重复组件、API/状态分叉与共享组件绕过，输出带文件行号、使用次数和迁移批次的 `UI_AUDIT.md`。
- 用户明确要求实施时，按语义 token → 基础组件 → 代表页面 → 批量迁移 → 清理旧实现收敛；保留刻意差异与一次性结构。
- 验证复用项目原生 typecheck/lint/test/build、现有 contrast/check_page、Storybook 或 preview 与 evidence.md。

非目标：不新增顶层模式，不更换技术栈或视觉方向，不新增依赖，不编写通用 TSX 正则扫描器，不修改 project-init。

## Conflict check

- project-init 负责脚手架、依赖和目录约定，并已将完整色阶与对比度交给 pretty-ui；新增边界句即可，无职责冲突。
- system.md 继续作为 token 刻度真源；组件工程化细则放新 engineering.md，避免膨胀 system.md 与 rules.md。
- 工作区已有 `20261030-183146-evidence-speedup` 审计记录及其生产改动，本轮以当前内容为基线，只覆盖本提案声明的文件。
- SKILL.md 当前接近 8 KB，路由与指针采用合并行并压缩重复表述，保留既有测试预算。

## Rationale

token 与组件统一是 system 的同一设计体系职责；独立 reference 可按需加载。审计与实施分离使“检查”保持只读，代表页切片限制回归面，采用项目原生工具避免引入脆弱的跨框架静态分析。契约测试和声明式 evals 可守卫分支、输出、迁移及例外行为。

## Files

- `skills/pretty-ui/SKILL.md`：description、system 路由、engineering 指针与 project-init 边界。
- `skills/pretty-ui/references/engineering.md`：新增 init/audit、检查项、组件契约、审计输出、迁移与完成门。
- `skills/pretty-ui/references/system.md`：增加工程化细则指针。
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`：新增路由、链接与 engineering 行为契约。
- `skills/pretty-ui/evals/cases.yaml`：新增初建、只读审计、代表页迁移、刻意差异与一次性结构案例。

## Validation

- 应用前：`git apply --check --recount skills/pretty-ui/patches/20261031-082315-ui-engineering/change.patch`。
- 应用后：生产文件 `git diff --check`；`python3 -m pytest skills/pretty-ui/tests -q`；`python3 -m pytest skills -q`；`make check-names`；`make check-style`。
- 核对实际 diff、frontmatter、引用、8 KB 预算与隐私，未改安装镜像、历史 patch 或其他 Skill。
