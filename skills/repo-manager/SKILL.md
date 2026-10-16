---
id: repo-manager
name: repo-manager
description: 用 `grepom`（首选）与 `glab`（GitLab 回退）批量管理工作区多个 Git 仓库。用于跨多仓 clone / sync / status / pull / push（含 push 前扫密钥）；创建 MR/PR、看 CI pipeline、打 release tag；从远端 group/org 发现新仓或在工作区仓库间跳转。
---

# 仓库管理

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文，不要逐词硬翻。

两层 CLI：跨仓批量优先用 `grepom`（源码与安装：github.com/sunzhenkai/grepom）；`grepom` 覆盖不到时再用 `glab`。

单仓的提交 / 推送走 `commit-push`，具体 diff 的评审走 `solo-code-review`；本 skill 管的是多仓与仓库基础设施。

配置查找：`grepom` 从当前目录或任意父目录读取 `.grepom.yml`。用 `-c <path>` 覆盖。

## 台账（`.repo-manager.md`）

**创建门禁（强制）** 与模板：读写 `.repo-manager.md` 前先读 [references/ledger.md](references/ledger.md)。

## 工具选择

| 需求 | 工具 |
|------|------|
| 跨多仓批量 clone / pull / status | `grepom` |
| 从远端 group/org 发现新仓 | `grepom sync` + `grepom clone` |
| 跨平台（GitLab + GitHub + 通用 Git） | `grepom` |
| 带 secret scan 的安全 push | `grepom push` |
| 仅 GitLab：issues、variables、snippets、raw API | `glab` |
| 细粒度 MR 参数（`--squash-before-merge`、`--label`、`--reviewer`、`--remove-source-branch`） | `glab mr create` |

`glab` 可选。安装：`brew install glab` / `apt install glab` / `scoop install glab`。多数 MR/PR 用 `grepom mr` 即可。

## 初始化（每个工作区一次）

```bash
# 交互式 — 写入 ./.grepom.yml
grepom init

# 非交互
grepom init --base ~/projects --provider gitlab \
  --url https://gitlab.example.com --token '${GITLAB_TOKEN}'

# 之后追加 resource / group / 独立仓库
grepom add resource --name work-gl --provider gitlab \
  --url https://gitlab.example.com --token '${GITLAB_TOKEN}'

grepom add group --name frontend --resource work-gl \
  --path my-org/frontend --recursive

grepom add repo --name dotfiles --resource github \
  --url https://github.com/me/dotfiles.git

# 重新生成一份干净的 example 配置
grepom example
```

token 值用 `${ENV_VAR}` 替换。密钥放在 shell 环境（1Password CLI / direnv / vault），禁止写进 YAML 明文。

## 发现与克隆

```bash
grepom sync                     # 从远端 group 填充配置（不 clone）
grepom clone                    # 全量克隆，4 worker 并行
grepom clone --group frontend   # 单个 group
grepom clone --resource work-gl # 某个 resource 下全部仓
grepom clone --concurrency 1    # 串行（compat）
grepom clone web-app            # 按名称克隆单仓
grepom clone --vgroup work      # 虚拟 group
```

`sync` 只追加新仓，从不删除。在 YAML 里改完 `exclude_repos` 后，用 `grepom prune --apply` 从磁盘去掉已排除的克隆。

## 工作区卫生

```bash
grepom status                   # 各仓 dirty / ahead 摘要
grepom list                     # 仅需关注的仓（默认 filter）
grepom list --all               # 全部仓，含干净的
grepom list --no-push           # 仅未 push
grepom list --no-commit         # 仅 dirty
grepom list groups              # 列出已配置 group
grepom list --remote            # 查 provider API，不用本地配置
grepom search web --group fe    # 大小写不敏感子串搜索
grepom pull                     # 更新干净且在默认分支的仓（并行）
grepom pull --force             # 不论状态都更新
grepom dedup                    # 查 group 内/跨 group 重复
grepom prune                    # dry-run：磁盘上仍在的已排除仓
grepom prune --apply            # 真正删除
```

## 安全 push 与 secret scan

push 前必须按 [references/git-ops.md](references/git-ops.md)「安全 push 与 secret scan」执行；MR / PR / Pipeline、Release tag 同见该文件。

## 跳转

在 `~/.zshrc`（或 `~/.bashrc`）加一次：

```bash
eval "$(grepom dir --shell)"
```

然后：

```bash
gcd web-app                      # 精确匹配 → cd
gcd web                          # 子串；唯一则 cd，多个则列出
grepom dir web-app               # 可脚本化：cd "$(grepom dir web-app)"
```

## glab：GitLab 专用回退

glab 回退与多实例鉴权见 [references/git-ops.md](references/git-ops.md)。

## 维护

```bash
grepom update                    # 自更新到最新 release
grepom completion zsh > ~/.zsh/completions/_grepom   # shell 补全
grepom version                   # 已安装版本
```

## 约定

- **token 来源**：YAML 里一律 `${ENV_VAR}` 占位；密钥经 1Password CLI / direnv / vault 导出，禁止明文。
- **先 commit 再 MR**：`grepom mr` 读 HEAD 消息，先写好 Conventional Commit 主题。
- **未经用户确认，禁止 `--force` push**。
- **过期配置**：`sync` 只追加；上游仓改名/删除时手动改配置，或用 `grepom init` + `grepom add group` 重建。
- **verbose**：命令异常时加 `-v` 看调试输出。
- **台账**：遵守 `.repo-manager.md` 创建门禁——禁止自动创建；仅文件已存在时自动更新（见「台账」节）。

## 不确定时

```bash
grepom --help
grepom <command> --help
glab --help
```

优先跑真实 `--help`，不要猜参数——两个工具迭代快，flag 会变。

## 踩坑（可复用经验）

可复用的踩坑经验（glab CLI、GitLab REST API、grepom 配置与 GitLab 分组）下沉在 [references/pitfalls.md](references/pitfalls.md)，排查时按需加载。**只记跨实例通用的规律**，具体 host / IP / token / 路径等特例不放。参数不确定先跑真实 `--help`（见上「不确定时」），再对照 pitfalls。

## 自进化

经验沉淀（`examples/` / `evals/cases.yaml` / `experience/`）与正文演进走 `skill-upgrader`，单次失败不直接改本文件。
