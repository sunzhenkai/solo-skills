# taskflow：driver 模板与 propose 产出约定

仅 `execution: openspec` 使用。Driver 协议块逐字写入 proposal；通用 worktree 真源是 [worktree.md](worktree.md)。

## 脚手架细则

`.openspec.yaml` 必须显式写 `skip_specs: true`。脚手架不写满 tasks.md，留给 stock openspec-propose；proposal 的 Driver 协议会进入 apply contextFiles。

## driver proposal 模板

````markdown
## Why
<目标、criterion、方案 / 批准指针>

## What Changes
- 本 change 只编排子 changes，不直接改代码

## Non-goals
- <...>

## 涉及面
| repo_id | source_repo | worktree | 角色 | 说明 |
|---|---|---|---|---|

## 验收标准
- [ ] <criterion 原文>

## Driver 协议
- 本 change 无 spec 增量（`.openspec.yaml` 已设 `skip_specs: true`）
- workspace 是唯一 planning root：`tasks/` 与本 driver / 子 changes 都在这里；所有 `openspec-*` 命令 cwd 都是 workspace，并显式给 change name
- 子 change 命名 `{task}-<slice>`，与 driver 同 workspace；不同项目不是更换 planning root 的理由
- 每个必须修改的 git 仓库先运行 `python3 <taskflow>/scripts/prepare_worktree.py <workspace> <task-id> <repo-id> <source-repo> --json`；代码、测试、项目文档和提交都在返回的 `<workspace>/worktrees/<task-id>/<repo-id>/`，失败时保留现场且不写代码
- 源 checkout 的分支和未提交改动保持原样；不 stash / reset / 自动复制未提交改动，不 push、不合默认分支、不自动清理 worktree
- 实现进度只认子 change 自己的 tasks.md；只有依赖的实施项都已勾的切片才建子 change；driver 实施项只在对应子 change 全勾、validate --strict 通过、这一片已提交到任务分支 `task/<task-id>` 后才勾
- 子 change 按依赖滚动展开，起草时以对应 worktree 当前代码为准；提交由编排者做，每片一次、收尾一次；每片提交后过一次片间检查点，不停人，按新证据补拆、合并或改序，只增删改未勾项并记录 decisions / history；独立交付边界回 taskrail decompose，criterion 变化回 intent / 意图变更
- 同任务同仓写操作串行；不同子任务或不同仓库才可并行。worker 输入只带本人范围、criterion、契约、worktree 绝对路径和证据要求，返回摘要与路径
- 单项做不了保持未勾并在验证记录写原因，继续其他就绪项；真阻塞只停依赖项，不勾假完成
- 子 change 全勾、validate --strict 与评审校核过后才 `openspec archive {task}-<slice> --yes`；未勾齐不归档
- driver 归档后回 taskrail verify / close；driver 归档或 checkbox 全勾不等于任务 done

## 验证记录
````

## propose 的 tasks.md 骨架

```markdown
## 1. 准备
- [ ] 1.1 对涉及面每个必须修改仓运行 prepare_worktree.py，并把 repo / worktree / branch / base 写回 TASK

## 2. 实施（一片一条，依赖写括号）
- [ ] 2.1 完成子 change `{task}-api`：全勾、validate --strict、提交到任务分支
- [ ] 2.2 完成子 change `{task}-ui`（依赖 2.1）：同 2.1

## 3. 收尾
- [ ] 3.1 在当前 worktree 跑回归与静态检查，结果写 proposal 验证记录
- [ ] 3.2 回填验收标准与未勾原因
- [ ] 3.3 提交收尾改动（不 push）
- [ ] 3.4 校核子 changes、评审处置和证据；归档全部子 changes
```

propose 只展开依赖已满足的切片；后续切片按当时 worktree 代码起草。已勾项和已归档 changes 不改写。父任务若有 subtasks，则每个子任务有自己的 driver 或 direct 路径，父任务不再持一个重复进度的 driver。
