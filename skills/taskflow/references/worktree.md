# workspace 多仓 worktree 协议

所有 direct / OpenSpec 代码路径共用。worktree 指 git worktree，不是普通目录复制。

## 根与身份

```text
workspace/
├── tasks/
├── openspec/
└── worktrees/<task-id>/<repo-id>/
```

source checkout 可在 workspace 内外；workspace 本身也可以是项目仓库。分支统一为 `task/<task-id>`，每个修改仓一个 worktree。repo_id 只在一个任务内唯一，task_id 在历史任务间也要避免误撞。

## 唯一准备入口

```bash
python3 <taskflow>/scripts/prepare_worktree.py <workspace> <task-id> <repo-id> <source-repo> [--base <ref>] [--json]
```

脚本行为：

- 校验 task / repo id，解析 source git root，默认基线为有效 origin/HEAD，否则 HEAD；不自动联网 fetch。
- 新建幂等；已存在且干净的 worktree 核对 source、branch、common git dir 后恢复。
- 未登记分支已存在、repo_id 指向其他 source、branch 不匹配时拒绝，不静默复用旧任务。
- 脏 worktree 返回非 0 并保留现场；不得 stash / reset / 覆盖用户改动。
- 注册表写 `worktrees/<task-id>/registry.json`，含 source、worktree、branch、base，供 resume 和崩溃恢复核对。
- worktree 位于 source 内部时才把对应顶层目录写 `.git/info/exclude`。

把脚本返回信息写 TASK「涉及仓库」。实现者只拿对应 worktree 绝对路径；OpenSpec 命令仍在 workspace 运行。

## 修改、提交与恢复

- 代码、项目文档、测试和提交都在 worktree；任务台账和 OpenSpec 在 workspace。
- 源 checkout 当前分支与用户已有改动保持原样。需要以未提交改动为输入时先显式记录并获用户认可，不自动复制。
- 编排者按连贯增量提交到 `task/<task-id>`；不 push、不合默认分支、不自动删除 worktree。
- resume 重跑脚本；若脚本在 worktree 新建后、注册前中断，路径 + source + branch 可安全证明身份时恢复注册，否则停。
- 非 git 目录或用户明确要求就地修改才可例外，写 decisions 和证据；不能据此把例外扩散到其他修改仓。
