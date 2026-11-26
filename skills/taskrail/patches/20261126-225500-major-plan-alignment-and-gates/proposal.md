# 重大改动默认人话对齐方案、grill 分层与 anti-lazy 门禁接入

- target: skills/taskrail
- mode: update
- patch: 20261126-225500-major-plan-alignment-and-gates
- risk: high
- status: proposed

## Intent

收口 taskrail 在大型项目、重大改动与架构调整时跳过方案对齐的三处缺口：

1. 将「大型项目 / 重大改动 / 架构调整 / 公共契约变更」升格为一等对齐门禁：默认无论 `human` 还是 `goal`，首次重大方案落定或实质变更前均须用人话与用户对齐并获明确放行（不因在 git 分支内可逆或属于同任务内部切片而跳过；`goal` 放行后后续实施与切片按自动模式推进；仅用户本会话原话明确豁免时改为异源审）。
2. 在 `user-report.md` 补充「重大方案人话对齐」正面标准（现状与目标、整体方案、关键取舍、影响面/节奏与回退），并将该停点前置到 `SKILL.md` 一层可见。
3. 将 `grill.md` 分层：普通局部技术未知仍自问自答；重大架构/契约/价值取舍不再自答闭环，整理成带推荐项的设计树前沿问题与用户拉齐，需要深度拷问用户时可按需启用可选外部 skill `grilling` 或 `grill-with-docs`。
4. 在 `confirm-protocol.md`、`design.md`、`plan.md`、`verify.md` 接入 `anti-lazy` 按名软指针，于方案对齐与交付前核对「哪件事只有用户能定」与目标差距。
5. 在 `scripts/task_state.py` 切到 `execute` 时增加机械检查：存在 `design/*.md` 但缺 `reviews/APPROVED.md`（含父任务批准覆盖）或 `PLAN.md` 的「实施确认」仍为 `pending` 时拒绝进入 `execute`。

非目标：不修改 `taskflow`、不新增固定线性阶段、不改写 `AGENTS.md` / `README.md` / 历史 `patches/`、不同步安装副本。

## Conflict check

- 保持 `confirm-protocol.md` 薄契约（`< 4000 B`）与 `SKILL.md` 8KB 软预算、一层直链和正向表述约束。
- 保留 `grill.md` 对局部技术未知的自问自答约定（不默认委托 `grilling`），仅对重大架构/路线/价值取舍与用户拉齐并按需启用可选外部 skill `grilling` / `grill-with-docs`（均已登记于 `README.md`「外部依赖」）。
- `anti-lazy` 为本仓在役 skill，采用按名软引用，不增加跨 skill 相对路径硬依赖。
- `task_state.py` 的 `execute` 检查兼容不含 `design/` 且未写 `## 实施确认` 的旧任务与仓级 `scripts/e2e_cross_repo.py`。

## Rationale

现有契约只在意图和最小 `PLAN.md` 设停点，`design.md` 落盘即退出、`approve.md` 易将分支内重构判为可逆、`goal` 免除全部人工对齐、`grill.md` 默认自答且无脚本门禁，导致大型架构改动在未和用户人话对齐的情况下直接动工。本轮同步收口入口可见性、路由/审批触发、人话对齐结构、`grill` 分层、`anti-lazy` 核对与脚本机械检查，并配套单测与 evals 守卫。

## Files

- `skills/taskrail/SKILL.md`：入口分诊纳入大型项目/架构调整/跨模块重大重构；在输入与主循环一层显式写明重大方案人话对齐停点。
- `skills/taskrail/references/confirm-protocol.md`：重大改动/架构调整在 `human` 与首次 `goal` 均停等用户人话确认（原话豁免改异源审）；闸口前自查接入 `anti-lazy`。
- `skills/taskrail/references/router.md`：`design` 与 `approve` 明确纳入大型项目/重大改动/架构调整/公共契约变更，明确不因分支内可逆或同任务内部切片跳过。
- `skills/taskrail/references/design.md`：落盘后按 `anti-lazy` 自检并准备人话方案摘要，重大方案必转 `approve` 落 `reviews/APPROVED.md`。
- `skills/taskrail/references/approve.md`：扩大进入条件至重大改动/架构调整，明确首次 `goal` 重大方案停等用户确认及 `reviews/APPROVED.md` 记录依据。
- `skills/taskrail/references/grill.md`：区分局部技术未知（自问自答）与重大架构/契约/价值取舍（前沿问题拉齐，按需启用可选 `grilling` / `grill-with-docs`）。
- `skills/taskrail/references/plan.md`：存在 `design/` 或命中重大方案时，进入 `execute` 前按 `anti-lazy` 核对并确认已有 `reviews/APPROVED.md`。
- `skills/taskrail/references/decompose.md`：澄清同任务内部切片不新增额外拆分停点，但整体命中重大方案仍须先完成整体方案人话对齐。
- `skills/taskrail/references/user-report.md`：新增「重大方案人话对齐」四要素标准与对应「前后对比」。
- `skills/taskrail/references/verify.md`：交付验证对照环节接入 `anti-lazy` 差距核对。
- `skills/taskrail/scripts/task_state.py`：`update --current-ref execute` 增加 `design/*.md` 缺 `APPROVED.md` 与 `PLAN.md` 实施确认仍为 `pending` 的机械阻断。
- `skills/taskrail/tests/test_confirm_contract.py`：新增重大改动默认人话对齐守卫测试。
- `skills/taskrail/tests/test_neighbor_skill_contract.py`：新增 `anti-lazy` 与可选 `grilling` 接线守卫测试。
- `skills/taskrail/tests/test_task_state.py`：新增 `execute` 机械门禁与子任务继承父批准测试。
- `skills/taskrail/tests/test_user_report_contract.py`：新增「重大方案人话对齐」指南守卫测试。
- `skills/taskrail/evals/cases.yaml`：新增重大架构改动人话对齐与重大取舍 grill 分层两条评估案例。

## Validation

- 在仓库根运行 `git apply --check --recount skills/taskrail/patches/20261126-225500-major-plan-alignment-and-gates/change.patch`。
- 高风险门禁：向用户展示风险、变更摘要与 diff，获明确确认后执行 `git apply --recount`。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'` 与 `python3 -m unittest discover -s tests -p 'test_*.py'`。
- 运行 `make check-names` 与 `make check-style`，确认 0 报错 0 告警。
- 核对无隐私泄露、无修改历史 `patches/` 或安装镜像目录。
