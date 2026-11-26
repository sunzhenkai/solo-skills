# P0 修复：对齐 direct/approve 契约、子任务继承父批准与 worktree 子任务路径隔离

- target: skills/taskflow
- mode: update
- patch: 20261127-002600-p0-handoff-worktree-and-direct-alignment
- risk: high
- status: proposed

## Intent

收口 taskflow 审阅中发现的三处跨 skill 契约冲突与脚本盲区：

1. 消除 `SKILL.md` 中 `direct`“不需要 approve”与 `taskrail` 正交审批门禁的直接矛盾：明确 `direct` 不走 handoff、不建 driver，但重大方案仍按 `taskrail approve` 放行。
2. 补齐 `scripts/check_handoff.py` 的父任务批准继承校验，使其与 `taskrail/scripts/task_state.py` 的 `has_approval()` 保持一致，同时拒绝空白 `APPROVED.md`。
3. 扩展 `scripts/prepare_worktree.py` 与 `references/worktree.md`，支持子任务路径 `<parent>/subtasks/<child>`，映射为扁平目录 `worktrees/<parent>--<child>/<repo-id>/` 与分支 `task/<parent>--<child>`，避免不同父任务下同名子任务撞车以及与 `task/<parent>` 发生 git 分支前缀冲突。

非目标：不改变 OpenSpec driver 协议结构、不引入父任务集成分支机制（留待 P1）、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskrail/patches/20261127-002600-p0-contract-and-gates/`（统一 `intent` / `RF-n` 并补齐 `task_state.py` 机械门禁）。
- 仓级配套改动（非本 patch 范围）：同步 `docs/task-flow/README.md`、`AGENTS.md`、`scripts/check_output_style.py`、`scripts/e2e_cross_repo.py`、`tests/test_output_style.py`。
- 保持 `prepare_worktree.py` 对单段 `<task-id>` 的现有目录、分支与 JSON 输出完全向后兼容，保持 stdlib-only 与 `SKILL.md` 8KB 约束。

## Rationale

`taskflow/SKILL.md` 原文写明 `direct` 不需要 `approve`，会误导执行者在重大重构时绕过 `taskrail` 门禁；`check_handoff.py` 原本不向上检查父任务 `APPROVED.md`，导致继承父批准的 OpenSpec 子任务误报失败；`prepare_worktree.py` 原本只接受单段 ID，跨父任务同名子任务（如 `api` / `web`）直接冲突。三处均属边界不闭合，按最小改动闭环并补单测守卫。

## Files

- `skills/taskflow/SKILL.md`：修正 `direct` 与 `approve` 的正交表述，补充 `prepare_worktree.py` 对子任务路径的说明。
- `skills/taskflow/references/worktree.md`：记录 `<parent>/subtasks/<child>` 到 `worktrees/<parent>--<child>/<repo-id>/` 与 `task/<parent>--<child>` 的映射规则。
- `skills/taskflow/scripts/check_handoff.py`：支持子任务继承父任务非空 `reviews/APPROVED.md`（兼容旧 `approve/APPROVED.md`），并拒绝空批准文件。
- `skills/taskflow/scripts/prepare_worktree.py`：支持 `<parent>/subtasks/<child>` 子任务路径解析与扁平目录/分支映射。
- `skills/taskflow/tests/test_taskflow_contract.py`：更新 `direct` 契约守卫，防止再次写回跳过 `approve` 的矛盾条款。
- `skills/taskflow/tests/test_check_handoff.py`：新增子任务继承父批准与空白 `APPROVED.md` 拦截单测。
- `skills/taskflow/tests/test_prepare_worktree.py`：新增跨父任务同名子任务隔离及与父分支共存单测。

## Validation

- 在工作树根运行 `git apply --check --recount skills/taskflow/patches/20261127-002600-p0-handoff-worktree-and-direct-alignment/change.patch`。
- 应用后运行 `git diff --check -- skills/taskflow`。
- 运行 `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`、`python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'` 与 `python3 -m unittest discover -s tests -p 'test_*.py'`。
- 运行 `make check-names` 与 `make check-style`，确认 0 报错 0 告警。
