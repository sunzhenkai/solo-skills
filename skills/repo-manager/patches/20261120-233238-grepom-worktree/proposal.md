# 记录 grepom 在 git worktree 中的识别限制

- target: skills/repo-manager
- mode: update
- patch: 20261120-233238-grepom-worktree
- risk: low
- status: proposed

## Intent

在 `references/pitfalls.md` 补充一条通用经验：在 git worktree 中运行 `grepom push` / `grepom mr` 时，若报错 `current directory is not a git repository`，优先检查当前目录的 `.git` 是 linked worktree 生成的 `.git` 文件，而不是普通克隆里的 `.git` 目录；处理方式是回到主 checkout 显式指定分支，或先用 `grepom scan -p <worktree>` 完成 secret scan 再走标准 git 流程。只改文档，不改工具行为。

## Conflict check

现有「安全推送」经验仍要求优先 `grepom push`；本补充说明其在 linked worktree 中的已知限制与替代验证方式，不取消 secret scan，也不建议使用 `grepom push -f` 绕过。

## Rationale

该报错措辞具有误导性：`git status` 在 linked worktree 中正常，而 grepom 的仓库识别不接受 `.git` 文件形式。记录后可直接按现象分流，避免把工具限制误判为 cwd 错误或重复重试同一命令。

## Files

- skills/repo-manager/references/pitfalls.md：在安全推送经验旁新增 linked worktree 条目。
- skills/repo-manager/patches/20261120-233238-grepom-worktree/：本次审计记录。

## Validation

- 应用前：`git apply --check --recount`。
- 应用后：`git diff --check`；`make check-names`；`make check-style`；运行 repo-manager 相关测试。
