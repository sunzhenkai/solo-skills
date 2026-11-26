# P1 优化：小中大任务尺度适配（合一确认、懒创建、子任务级 HITL/AFK、集成闭环与 OpenSpec 单一归属）

- target: skills/taskrail
- mode: update
- patch: 20261127-004000-p1-scale-adapt-and-integration
- risk: high
- status: proposed

## Intent

优化 taskrail 在小、中、大型任务上的体验与落地闭环：

1. **小型任务提速**：单一明确小改（单仓、无 `design`/`decompose`、改点与验证一步读清）允许在首轮合并呈现意图复述与最小计划，用户一次确认同时落定两项确认；`task_state.py init` 懒创建台账文件（只建 `TASK.md`、`PLAN.md`、`context/current.md`，`decisions.md`/`history.md` 首次有内容时再建）；小任务允许 3 段紧凑版 `SUMMARY.md`。
2. **大型任务子任务级 HITL/AFK**：解除 `task_state.py init --parent` 禁止覆写 `confirm_mode` 的死锁——子任务默认继承父模式，但允许在 `ROADMAP.md` 中按子任务覆写为 `human`（HITL）或 `goal`（AFK）。
3. **父任务同仓多子任务集成闭环**：在 `decompose.md` 与 `contract.md` 明确前置依赖子任务的 `--base` 串联方式，以及父任务进入 `verify` 时通过 `prepare_worktree.py <workspace> <parent>/integration ... --integrate` 在隔离集成 worktree 合并验证子任务分支（冲突即中止并回退），绝不触碰源仓与默认分支。
4. **OpenSpec 与 taskrail 产物单一归属**：选定 `execution: openspec` 后，详细设计与切片清单归 OpenSpec changes，`PLAN.md` 只留指向 driver 的一行指针，消除多套计划/设计文档叠罗汉。

非目标：不引入 Matt 工程方法论（留待 P2）、不合并裁剪 `references/` 数量（留待 P3）、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskflow/patches/20261127-004000-p1-integration-worktree-and-env-bootstrap/`（在 `prepare_worktree.py` 落地 `<parent>/integration` 与 `--integrate` 合并/冲突回退能力，补充 worktree 环境引导与 OpenSpec 归属对齐）。
- 保持 `confirm-protocol.md` 严格 `< 4000 B`（`test_task_family_contract.py` 守卫）、`SKILL.md <= 8192 B`、一层直链与 stdlib-only 约束。

## Rationale

小任务强制两轮停点与 5 文件预建造成过高记账摩擦；大任务一刀切父子 `confirm_mode` 导致无法同时对高危核心走 HITL、对契约锁定子任务走 AFK；同仓多子任务此前缺少父级合并验证物理环境；OpenSpec 下 `PLAN.md` 与 driver/slice 产物易重叠。本轮将四项结构摩擦一次性收口并配套单测与 evals。

## Files

- `skills/taskrail/references/confirm-protocol.md`：在保持 `< 4000 B` 前提下增加单一明确小改首轮合一确认规则与子任务按 ROADMAP 覆写 `human`/`goal` 规则。
- `skills/taskrail/references/intent.md`：补充单一明确小改首轮合并呈现意图与最小计划的规则。
- `skills/taskrail/references/plan.md`：补充首轮合一确认落账、子任务按自身 `confirm_mode` 确认 PLAN 及 OpenSpec 下 `PLAN.md` 仅留 driver 指针的规则。
- `skills/taskrail/references/decompose.md`：ROADMAP 模板增加可选 `模式` 列（HITL/AFK），`init --parent` 支持 `--confirm-mode` 覆写，补充依赖子任务 `--base` 与父任务 `<parent>/integration --integrate` 集成协议。
- `skills/taskrail/references/handoff.md`：明确 `execution: openspec` 后设计与切片归 OpenSpec、`PLAN.md` 仅留 driver 指针。
- `skills/taskrail/references/close.md`：允许单一明确小改使用 3 段紧凑版 `SUMMARY.md`。
- `skills/taskrail/references/templates.md`：注明 `decisions.md`/`history.md` 懒创建与紧凑版 `SUMMARY.md`。
- `skills/taskrail/references/contract.md`：同步懒创建、子任务模式覆写、父级集成 worktree 与 OpenSpec 产物归属契约。
- `skills/taskrail/scripts/task_state.py`：`init_task()` 支持子任务显式覆写 `--confirm-mode`（省略仍继承父任务），且仅懒创建热三件（`TASK.md`/`PLAN.md`/`context/current.md`）。
- `skills/taskrail/evals/cases.yaml`：新增小任务合一确认、子任务 HITL/AFK 覆写与父任务同仓集成 worktree 3 条案例。
- `skills/taskrail/tests/test_task_state.py`、`test_confirm_contract.py`、`test_decompose_contract.py`：同步并新增对应单测与契约守卫。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-004000-p1-scale-adapt-and-integration/change.patch`
- `git diff --check -- skills/taskrail`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `make check-names` 与 `make check-style`
