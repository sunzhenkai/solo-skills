---
id: repo-manager
name: repo-manager
description: 通过 `grepom`（首选，跨平台批量操作工作区多仓）和 `glab`（GitLab 专用回退：issues、variables、snippets、细粒度 MR 参数）管理多个 GitLab / GitHub / 通用 Git 仓库。若已有 `.repo-manager.md` 则维护 cwd 台账（创建前先询问）。在用户要求跨多仓 clone、sync、list、status、pull、search、scan、push、创建 MR/PR、看 CI pipeline、处理 `.grepom.yml`、从远端 group/org 发现新仓、push 前扫密钥、打 release tag、或在工作区仓库间跳转时使用。不要用于单文件 git 操作、特定 diff 的 code review、或与仓库基础设施无关的工作。
---

# 仓库管理

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文，不要逐词硬翻。

两层 CLI：跨仓批量优先用 `grepom`（源码与安装：github.com/sunzhenkai/grepom）；`grepom` 覆盖不到时再用 `glab`。

配置查找：`grepom` 从当前目录或任意父目录读取 `.grepom.yml`。用 `-c <path>` 覆盖。

## 台账（`.repo-manager.md`）

在**当前工作目录**维护 `.repo-manager.md`，记录本工作区的仓库台账与操作手帐，供人与后续 agent 复用。

### 创建门禁（强制）

| 情况 | 行为 |
|------|------|
| `./.repo-manager.md` **不存在** | **禁止自动创建**。向用户提示：「当前目录没有 `.repo-manager.md`，是否创建台账？」仅当用户明确同意（如「创建」「写台账」「初始化 .repo-manager.md」）后再按下方模板新建。 |
| `./.repo-manager.md` **已存在** | **自动更新**：会话开始先读；有实质操作或新踩坑后立刻写回，无需再问。 |
| 用户明确要求创建/初始化台账 | 即使原先不存在，也按模板创建并写入本次信息。 |

路径始终是 **cwd 下的** `./.repo-manager.md`（不要写到 home、cache 或父目录，除非用户另行指定）。

### 何时读写

1. **任何 repo-manager 操作开始时**：若文件存在，先读一遍——优先采用其中的 resource/group 约定、exclude、鉴权环境变量名、已知坑。
2. **文件存在且完成实质操作后**：自动追加/更新手帐与稳定信息（见下）。只读查询（如单纯 `status` / `list` 且无发现）可不写。
3. **遇到坑时立刻写入**：鉴权失败、sync/clone 异常、prune 误伤、secret scan 命中策略、host/protocol 踩坑等——确认原因或绕过后马上记入「踩坑」，同一问题更新已有条目，不重复堆砌。
4. **文件不存在时**：照常执行 grepom/glab；仅提示一次可建台账，**不**因提示未答复而阻断操作。

### 应记录的内容

- **概览**：工作区用途、`.grepom.yml` 位置（相对 cwd）、主要 resource / group / vgroup、本地 base 路径约定。
- **约定**：常用 filter（`--group` / `--resource` / `--vgroup`）、exclude 策略、token 环境变量**名**（不写值）、SSH/HTTP 协议偏好。
- **手帐**：有状态变化的操作——`sync` / `clone` / `pull` / `prune` / `push` / `mr` / `tag` / 批量 discovery 等；一行一条，含日期与结果摘要。
- **踩坑**：本工作区特有问题与绕过方式。

### 文件模板

新建时使用（按实际删减，保持简洁）：

```markdown
# 仓库管理 — <工作区目录名>

## 概览

- 一句话说明本工作区管理哪些仓库
- 配置：`.grepom.yml`（或相对路径）
- base / 主要 group、resource

## 约定

- 常用命令或 filter
- 鉴权：环境变量名（如 `${GITLAB_TOKEN}`），禁止写明文
- exclude / prune 注意点

## 手帐

- YYYY-MM-DD：操作 → 范围 → 结果（如 sync 新增 N 仓；clone 失败的 repo）

## 踩坑

- YYYY-MM-DD：现象 → 原因 → 解决/绕过
```

### 写入原则

- 只写与**多仓管理 / 同步 / 鉴权 / 扫描 / MR·流水线**相关的信息；不写业务代码细节。
- **禁止**写入 token、密码、私钥、内部未公开 URL 中的凭据部分。
- 手帐要可回溯：后人能看出「何时对哪些 group 做了什么」。
- 稳定约定放「概览/约定」，一次性操作放「手帐」；不要把整份 `grepom status` 原文贴进文件。
- 用户若明确要求不提交该文件，提醒可加入 `.gitignore`，但仍在本地维护。

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

## Self-evolution

本 Skill 具备经验积累、评估与持续进化能力。目录（均相对本 Skill 根目录）：

```text
skills/repo-manager/
├── SKILL.md
├── examples/      # 经过验证的优秀执行案例
├── evals/         # 可验证成功标准
└── experience/    # 真实失败 / 成功 / 规律
```

不要为了自进化而破坏上文已规定的目标、流程、工具用法、输出与约束。

### Examples

执行复杂任务前：

1. 检查 `examples/`
2. 找到与当前任务相关的成功案例
3. 优先复用已经验证的方法

没有相关案例时按上文正常执行，不要编造案例。

### Evaluation

任务完成前：

1. 检查相关 `evals/`
2. 验证关键输出
3. 检查是否违反 Skill 约束
4. 尽可能运行相关 Eval Cases（见 `evals/cases.yaml`）

优先确定性 Eval；无法确定性判断时再用 LLM Judge。Eval 失败则先修输出，不要带着失败交卷。

### Experience

任务完成后，出现以下情况才写入 `experience/`：

- 失败
- 用户纠正
- 明显成功
- 新的有效执行方法
- 可复用的经验

不要记录 trivial information。不要伪造条目。密钥、内部 URL、凭据不得写入。

单次失败 → `experience/failures/`。重复出现的规律 → `experience/patterns/`（至少两次同类证据）。

### Evolution

只有当 Experience 暴露出**可复用、稳定的问题或模式**时，才考虑修改本 Skill。

遵循：

```text
Experience
    ↓
Repeated Pattern
    ↓
Improvement Proposal
    ↓
Eval
    ↓
Pass
    ↓
Update Skill
```

禁止：

```text
Single Failure
    ↓
Directly modify SKILL.md
```

进入 Skill 正文的 Experience 必须同时满足：可复用于多个类似任务、有足够证据、能明确改善结果、不破坏已有能力、可通过 Eval 验证。一次性特殊情况只留 Experience，不改 Skill。

实际更新生产 `SKILL.md` 时：

1. 不要直接覆盖原文；记录 version / change / reason / evidence / evaluation。有 Git 则优先靠 Git diff 留历史。
2. 若当前环境有 `skill-evolver`，委托它走候选 patch → 验证 → 晋升，不要本 Skill 自己改生产稿。
3. 未展示 Proposal 并获得用户确认前，不改生产 Skill。
