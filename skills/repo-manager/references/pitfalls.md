## 踩坑（可复用经验）

可复用的踩坑经验。**只记跨实例通用的规律**，具体 host / IP / token / 路径等特例不放这里。

### glab CLI

- **HTTP-only 实例必须显式 `--api-protocol http`**：默认走 https，遇到 TLS 错误优先怀疑这个 flag 没带。
  ```bash
  glab auth login --hostname <host> --api-protocol http --git-protocol ssh --stdin
  ```
- **glab 全局默认 host 是 `gitlab.com`**：所有 `glab api /xxx`、`glab mr list` 等命令不显式 `--hostname` 都会用到默认值。多实例环境永远带 `--hostname <host>` 或 `GITLAB_HOST=<host>`。
- **keyring 不可用时 fallback 到 plaintext**（常见于 Linux server / 无 desktop env）：token 落到 `~/.config/glab-cli/config.yml`（权限 0600）。可手动 `chmod 600` 加固；启用 desktop 后再 `glab auth login` 一次会搬回 keyring。
- **`glab mr list` 在 cwd repo 没匹配 host 时报 "remote not known"**：用 `--hostname <host> -R <group>/<repo>` 解决，或 `cd` 到目标 repo。

### GitLab REST API

- **GitLab 17.9+ transfer API 用 `PUT /projects/:id/transfer`**（不是 `POST`）。参数是 `namespace=<group_path>`，不是 `namespace_id=<id>`。
  ```bash
  glab api --hostname <host> -X PUT projects/<id>/transfer -f namespace=<group_path>
  ```
- **`DELETE /projects/:id` 默认是软删除**：标 `marked_for_deletion_at` + 30 天后悔期。path 自动加 `-deletion_scheduled-<id>` 后缀防冲突。
- **恢复软删除**：`POST /projects/:id/restore`，path 自动回到原值。
- **物理硬删要走 admin 内部接口**：`glab` 不暴露；要在 GitLab 主机上 `gitlab-rails console` 跑 `Project.unscoped.find(<id>).really_destroy!`。
- **搜 namespace 不要只查一处**：自托管 group/user 命名易混，三个 API 并行查：
  ```bash
  glab api --hostname <host> 'groups?search=<kw>'
  glab api --hostname <host> 'users?username=<kw>'
  glab api --hostname <host> 'namespaces?search=<kw>'   # 同时含 group + user
  ```
- **`/api/v4/version` 401 不一定是 TLS 错**：很多自托管实例把 version 也要求认证，反而说明 HTTP/API 路径对，继续带 token 测 `/user` 即可。

### grepom 配置与 GitLab 分组

- **配置作用域要先确认**：grepom 会从当前目录向上查找 `.grepom.yml`。在项目内新增本地配置后，它会遮蔽父目录配置；需要操作另一份配置时显式使用 `grepom -c /path/to/.grepom.yml ...`，避免把仓库克隆到错误的 workspace。
- **最小 GitLab 配置**：`base` 是相对于配置文件目录的克隆根目录；分组的 `local_path` 再相对于该 `base` 计算。例如 `base: ./repos`、`local_path: ./team`、远程路径 `team/service` 最终落在 `repos/team/service`。
  ```yaml
  base: ./repos
  resources:
    gitlab-primary:
      provider: gitlab
      url: https://gitlab.example.com
      token: ${GITLAB_TOKEN}
  groups:
    - name: team
      resource: gitlab-primary
      path: team
      local_path: ./team
      recursive: true
  repos: []
  ```
- **推荐初始化顺序**：先用 `grepom init --base ./repos --provider gitlab --url <host> --token '${TOKEN_ENV}'` 生成配置，再把 resource 名称调整为有意义的实例名（例如 `gh`），最后用 `grepom add group --name <name> --resource <resource> --path <group-path> --local-path ./<local-dir> --recursive` 登记分组。不要把 token 明文写入 YAML。
- **追踪与克隆分两步**：`grepom sync --group <group>` 只向配置追加远程发现的新仓库，不会自动克隆；确认发现结果后运行 `grepom clone --group <group>`。全量场景可使用 `grepom clone --resource <resource>`，单仓库使用 `grepom clone <repo-name>`。
- **同步结果要核对**：sync 后用 `grepom list groups` 检查 group/resource/path/repo 数量，再用 `grepom list --all` 确认仓库状态；clone 后进入目标仓库执行 `git status --short --branch`，或运行 `grepom status`。
- **HTTP-only 或 TLS 异常的自托管 GitLab**：资源 URL 显式写 `http://<host>`，避免 grepom 先尝试 HTTPS 再回退并产生额外延迟。若 `grepom add group` 将 URL 规范化为无 scheme 的 host，可手动恢复 `http://` 后再次用 `grepom list` 校验配置仍可解析。API 查询和 glab 操作同时显式带 `--hostname <host>`。
- **SSH URL 形态要注意**：对带 GitLab resource 的 standalone repo，优先把 `url` 写成远程相对路径（如 `group/repo.git`），让 grepom 组合成 `git@<host>:group/repo.git`；直接填 `ssh://git@<host>/group/repo.git` 可能被重复拼接成错误地址。分组 sync 通常会自动写入可用的 HTTP clone URL，SSH clone 仍会优先尝试本机密钥。
- **新建远程项目后的登记方式**：远程项目已存在于已追踪的 GitLab group 时，重新执行 `grepom sync --group <group>` 即可发现；不在已追踪 group 中时使用 `grepom add repo --name ... --resource ... --url ...`。创建远程项目属于 GitLab API 能力，grepom 未覆盖时用 `glab repo create <host>/<group>/<repo> --skipGitInit`，创建后再回到 sync/clone 流程。
- **克隆基目录应纳入忽略**：如果 `base` 指向项目内的 `repos/`，将 `repos/` 加入项目 `.gitignore`，避免把被管理仓库的工作树误提交到当前配置仓库；配置文件 `.grepom.yml` 是否提交则按项目约定处理。
- **安全推送**：完成仓库内提交后优先用 `grepom push -- origin <branch>`，它会先执行 secret scan；扫描包含大二进制文件时可能较安静且耗时，等待命令返回，不要在未确认结果前重复 push。发现命中时先清理或配置 allowlist，不要默认使用 `-f`。

---

