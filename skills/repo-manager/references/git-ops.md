# Git 远端操作：push、MR/PR、Release、glab 与多实例鉴权

## 安全 push 与 secret scan

```bash
grepom push                     # gitleaks scan → git push；命中则中止
grepom push -f                  # force（会警告）
grepom push -- origin main      # 透传给 git push
grepom scan                     # 扫工作区文件（gitleaks 规则）
grepom scan --history           # 含 git 历史（含已删 commit）
grepom scan --format json -o report.json
grepom scan -p /path/to/repo    # 临时路径，不需要配置
grepom scan --gitleaks-config rules.toml   # 项目级 allowlist
```

`grepom push` **不需要**配置文件，任意 git 仓库都能用。默认：先 scan，干净才 push。

## MR / PR / Pipeline

```bash
# MR/PR — 从 HEAD 自动推断 branch、target、title
grepom mr
grepom mr --from feat-x --to main --title "Add X" --draft
grepom mr --body-file desc.md --web    # 用浏览器打开，不用 CLI
grepom pr                              # `mr` 的别名

# Pipeline
grepom pipeline list                   # 最近的 pipeline
grepom pipeline watch                  # 等待当前 pipeline
grepom watch                           # 从 cwd 自动识别仓
grepom watch web-app --id 1234         # 指定仓 + pipeline
```

`grepom mr` 从 HEAD commit 读 title 和 body。先写好 Conventional Commit 主题。

需要 `--squash-before-merge`、`--label`、`--assignee`、`--reviewer`、`--remove-source-branch`、`--milestone` 时，回退到 `glab mr create`。

## Release tag

```bash
grepom tag                       # v0.1.5 → v0.1.6（lightweight）
grepom tag -m "release notes"    # annotated
grepom tag -p                    # push 到全部 remote
grepom tag -t -p                 # t-prefix（测试 release）
grepom tag -w                    # tag 后 watch pipeline
grepom tag --dry-run             # 只预览
```

## glab：GitLab 专用回退

单仓范围。`grepom` 覆盖不到时再用。

```bash
glab auth login --hostname gitlab.example.com
glab repo clone gitlab.example.com/group/repo
glab mr create --title "..." --description "..." --target-branch main \
  --squash-before-merge --remove-source-branch --label ~"feature" --reviewer alice
glab mr list
glab issue list --assignee @me
glab ci status
glab ci trace                    # 实时 job 日志
glab variable list               # CI/CD variables
glab api projects/:id/variables  # raw API
```

## 多实例鉴权

`glab` 按 hostname 存凭据，没有 `switch` 命令。每个实例登录一次，再按命令或当前 shell 选 host：

```bash
# --stdin 避免 token 进 shell history
glab auth login --hostname gitlab.example.com --stdin
glab auth login --hostname gitlab.other.com --stdin
glab auth status --all

GITLAB_HOST=gitlab.other.com glab mr list   # 单条命令
export GITLAB_HOST=gitlab.example.com       # 当前 shell
glab auth logout --hostname gitlab.other.com
```

host 解析顺序：`GITLAB_HOST` → 当前仓库 Git remote → `~/.config/glab-cli/config.yml`。无图形界面登录用 `--device`（GitLab 17.9+）。凭据默认走 OS keyring；仅必要时才用 `--insecure-storage`。

对 `grepom`：每个 GitLab 实例建模成命名 `resource`，再把 group 绑上去：

```yaml
resources:
  corp:
    provider: gitlab
    url: https://gitlab.example.com
    token: ${CORP_GITLAB_TOKEN}
  oss:
    provider: gitlab
    url: https://gitlab.com
    token: ${OSS_GITLAB_TOKEN}

groups:
  - name: backend
    resource: corp
    path: my-org/backend
    recursive: true
```

按需用 `grepom clone --resource corp`、`grepom status --resource corp` 或 `grepom pull --resource corp`；每个 resource 可覆盖自己的 `token`/`ssh_key`。token 放环境变量，用最小权限 PAT；泄露则立刻 revoke/rotate。
