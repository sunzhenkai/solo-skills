# 切分支改成 worktree

用户规则：worktree 默认放到当前目录的 `worktrees/` 下，除非其他规则另有指定；随后要求把 Driver 协议的切分支方案改成 worktree。

改动：
- Driver 协议：必须修改仓（仍可选）从默认分支最新代码 `git worktree add worktrees/{task} -b {task}`，`worktrees/` 写进 `.git/info/exclude`，实施、回归、提交都在 worktree 里做；主工作树与用户未提交改动不碰，原来 dirty 时带改动 `git switch -c` 的分支逻辑随之删除；git 拒绝才停；收尾保留 worktree，清理留给用户。
- tasks.md 骨架 1.1、execution-discipline、multi-worker 的「切分支」同步为「建 worktree」，multi-worker 的独立工作树指向 Driver 协议。
- evals fail-closed-must-repos 按新规则重写。
