# task 系列深度复审落地（taskflow，本批增量）

在 20261020-231800-worktree-instead-of-branch 之上，change.patch 只含本批增量（相对改前快照）。

- Driver 协议补「两个根」：planning root（tasks/、openspec/changes/）留主工作树，openspec-* 在这里跑；代码根 `worktrees/{task}`，改代码、测试、提交在这里，实现者工作目录写它的绝对路径。
- 必须修改仓一律建 worktree（去掉「可选」，例外：非 git 仓或用户要求就地改）；基线默认 origin/默认分支，当前分支领先时用 HEAD；修正「分支已存在去掉 -b」会建出 detached HEAD 的命令，改为 `git worktree add worktrees/{task} {task}`。位置仍按用户规则放修改仓根 `worktrees/{task}` 并写 `.git/info/exclude`。
- 同一任务的 worker 共用这个 worktree；提交只落任务分支，不 push、不合进默认分支（与 taskrail 边界对齐，解除 3.3 勾不上的冲突）。
- gate_bypass：用户原话要求跳过时由 agent 照录原话写入，没有 TASK.md 先按模板建最小一份；taskflow-new 有 TASK.md 时 `{task}` = slug，`--goal` 与 handoff 一致。
- check_handoff.py 兼容 `- key:` 列表行；去掉已删除的「未覆盖即降级」说法。
- description 去掉反向句；evals 同步；新增行为测试 test_template_task_md_passes、test_bullet_meta_compat、test_worktree_protocol。
