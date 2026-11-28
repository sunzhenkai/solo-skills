---
id: 20261128-181200-worktree-node-deps-guidance
skill: taskflow
mode: update
status: proposed
risk: low
source: user-feedback-retrospective
created_at: 2026-11-28T18:12:00+08:00
---

# Proposal: 补充 taskflow worktree 中 pnpm/Node 依赖符号链接踩坑指引

## Trigger & Evidence
- 在 JS/TS monorepo 中使用 git worktree 运行测试时，若直接软链源仓的 `node_modules`，`pnpm` 的 `.pnpm` 虚拟存储与硬链接解析常在部分测试/构建工具下失效或污染路径。

## Target Files
- `skills/taskflow/references/worktree.md`
- `skills/taskflow/tests/test_taskflow_contract.py`

## Planned Changes
1. 在 `skills/taskflow/references/worktree.md` 的「未跟踪环境与重依赖」条目中补充：对 `pnpm` 等依赖硬链接/虚拟存储的 Node 工作区，优先在 worktree 内执行 `pnpm install --frozen-lockfile`（或项目标准安装命令），避免直接软链源仓 `node_modules` 导致路径解析异常。
2. 在 `skills/taskflow/tests/test_taskflow_contract.py` 新增契约测试，锁定该指引。

## Conflict Check
- 同步发起伴随 patch：`session-wrap`（`20261128-181200-enforce-push-gate-and-mock-boundary`）与 `anti-lazy`（`20261128-181200-mock-only-verification-and-contract-check`），三者修改各自独立目录，无文件冲突。

## Acceptance Criteria
- `python3 -m unittest discover -s skills/taskflow/tests` 通过。
- `make check-names && make check-style` 通过。
