# MR/PR 模式细则

入口与门禁在 SKILL.md「四步流程」；本文件是步骤细则。

1. `reviewctl parse-mr --url <url>` → `kind` / `host` / `project` / `iid` / `repo_hint`
2. 用 `repo_hint`（或 URL 里的 project）调 `reviewctl resolve-repo` / `inspect` 定位本地仓；找不到则列出候选或请用户给仓库路径。
3. 取源/目标分支（GitLab 凭据仅走环境变量）：
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

5. 审查范围：`--from origin/<target_branch> --to refs/code-review/mr-<iid>`（GitHub 用 `pr-<iid>`）。
6. 预览变更列表：

```bash
python3 <skill-root>/scripts/reviewctl.py --root <workspace-root> preview \
  --repo <git_root_abs> --mode range --from origin/<target_branch> --to refs/code-review/mr-<iid>
```

7. 交由用户选定的引擎执行：
   - `builtin` / `claude` / `ocr`：直接使用上述 `origin/<target_branch>..refs/code-review/*` 范围；
   - `codex`：因不得 checkout，走只读 `codex exec --sandbox read-only` 审查上述范围（详见 `references/external-agents.md`）。
