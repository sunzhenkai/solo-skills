# P1 优化：父任务集成 worktree（--integrate）、环境引导与 OpenSpec 归属对齐

- target: skills/taskflow
- mode: update
- patch: 20261127-004000-p1-integration-worktree-and-env-bootstrap
- risk: high
- status: proposed

## Intent

补齐 taskflow 在大型多子任务集成验证与真实项目 worktree 冷启动上的两项物理缺口，并对齐 OpenSpec 产物归属：

1. **父任务同仓集成 worktree**：`scripts/prepare_worktree.py` 支持 `<parent>/integration` 路径（映射为 `worktrees/<parent>--integration/<repo-id>/` 与分支 `task/<parent>--integration`）及可重复参数 `--integrate <ref>`，在隔离工作树内按序 `git merge --no-ff --no-edit` 合并多个子任务分支（幂等跳过已合入祖先）；遇合并冲突时自动 `git merge --abort` 保持现场干净并以退出码 `5` 返回结构化 `conflict_branch` 与 `conflict_files`。
2. **worktree 环境与未跟踪依赖引导**：在 `references/worktree.md` 明确新建 worktree 不含源仓 gitignored 的 `.env` / `node_modules` / `.venv` 时的检查与引导原则，不静默复制未提交改动或污染源仓。
3. **OpenSpec 产物单一归属**：在 `SKILL.md` 明确选定 `execution: openspec` 后，详细设计与切片清单由 OpenSpec changes 维护，`PLAN.md` 仅留指向 driver 的一行指针。

非目标：不引入 TDD 编码纪律（留待 P2）、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskrail/patches/20261127-004000-p1-scale-adapt-and-integration/`（在 `decompose.md`、`contract.md`、`plan.md`、`handoff.md` 中接入 `<parent>/integration --integrate` 与 OpenSpec 单一归属）。
- 保持 `prepare_worktree.py` 既有参数与 JSON 输出 100% 向后兼容，保持 stdlib-only 与 `SKILL.md <= 8192 B` 约束。

## Rationale

同一仓库拆出多个子任务并各自在独立分支交付后，父任务 `verify` 此前缺少不触碰源仓/默认分支的物理合并验证手段；新建 worktree 缺少本地 `.env` / 依赖缓存也是高频冷启动卡点。本轮用确定性脚本加明确约定闭环，并附真 git 仓库集成单测（含无冲突幂等合并与冲突中止回退）。

## Files

- `skills/taskflow/scripts/prepare_worktree.py`：支持 `<parent>/integration` 与 repeatable `--integrate <ref>`，实现幂等合并与冲突自动 `merge --abort` + 结构化报错。
- `skills/taskflow/references/worktree.md`：记录 `<parent>/integration --integrate` 集成协议、依赖子任务 `--base` 串联与 gitignored 环境/依赖引导规则。
- `skills/taskflow/SKILL.md`：同步 `--integrate` 入口提示与 OpenSpec 单一产物归属说明。
- `skills/taskflow/evals/cases.yaml`：新增父任务集成 worktree 合并与冲突中止评估案例。
- `skills/taskflow/tests/test_prepare_worktree.py`：新增多子任务同仓幂等合并与冲突中止回退两个真实 git 单测。

## Validation

- `git apply --check --recount skills/taskflow/patches/20261127-004000-p1-integration-worktree-and-env-bootstrap/change.patch`
- `git diff --check -- skills/taskflow`
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`
- `make check-names` 与 `make check-style`
