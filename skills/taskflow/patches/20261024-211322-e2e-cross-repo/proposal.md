# Proposal: 固化跨仓 E2E 回归脚本

## Why

taskrail / taskflow 的跨仓能力已经过两条人工端到端验收（direct 父子任务 + OpenSpec CLI driver 双切片），但验收脚本与夹具散落在任务工作区，改 skill 后无法一键回归。

## What Changes

- 新增 `scripts/e2e_cross_repo.py`：一键在临时目录创建两个 git 夹具仓，复现两条验收路径并逐步断言：
  - direct：父任务 + 两个子任务 + `prepare_worktree.py` + 父级集成 + close 归档；
  - openspec：`check_handoff.py` 门 → driver（skip_specs）→ 两个子 change → `validate --strict` → `archive --yes` → 父级集成 → close 归档。
- 新增 `tests/test_e2e_cross_repo.py`：结构契约（脚本存在、仅标准库导入、--help 可用）+ 活体契约（git 可用跑 direct，openspec CLI 可用跑 openspec，缺依赖自动 skip）。
- 只加仓级脚本与测试，不改任何 skill 正文。

## 影响面

根 `scripts/` 与 `tests/` 各一个新文件；skill 正文零改动。

## 验证

- `python3 scripts/e2e_cross_repo.py --mode all`：direct 11 步 PASS（0.9s）、openspec 14 步 PASS（22.6s，CLI 1.14.1）。
- 根 `tests/`：13 tests OK（含两个活体 E2E）；taskrail 131 tests OK；taskflow 58 tests OK。
- `make check-names` / `make check-style` / `git diff HEAD --check`：全部通过。
