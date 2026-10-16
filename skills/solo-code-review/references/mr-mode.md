# MR/PR 模式细则

入口与门禁在 SKILL.md「流程」；本文件是步骤细则。

1. `reviewctl parse-mr --url ...` → `kind` / `host` / `project` / `iid` / `repo_hint`
2. 用 `repo_hint`（或 URL 里的 project）`inspect`/`resolve-repo` 定位本地仓；找不到则列出候选或请用户给仓库路径。
3. 取源/目标分支：
   - GitLab：`GITLAB_TOKEN="$GITLAB_TOKEN" glab mr view <iid> --repo https://<host>/<project> -F json`
   - GitHub：`gh pr view <iid> --repo <project> --json baseRefName,headRefName,title`
4. **只 fetch，不 checkout、不 stash**：

```bash
git -C <git_root_abs> fetch origin
# GitLab
git -C <git_root_abs> fetch origin "merge-requests/<iid>/head:refs/code-review/mr-<iid>"
# GitHub
git -C <git_root_abs> fetch origin "pull/<iid>/head:refs/code-review/pr-<iid>"
```

5. 审查范围：`--from origin/<target_branch> --to refs/code-review/mr-<iid>`（GitHub 用 `pr-<iid>`）
6. `ocr review --preview` 后确认再跑 LLM。用户指定了 `provider=` / `model=` 时同样透传 `--provider/--model`（见 SKILL.md「调用」与「跑 ocr」）。
