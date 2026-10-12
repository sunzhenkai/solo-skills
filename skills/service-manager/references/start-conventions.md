# 启动约定、discover、身份匹配与运行状态判定

## 开发/测试启动约定

适用于本地 **开发 / 测试** 原生服务。判定信号（任一即可）：`source` 为 Makefile / package.json / 语言入口等；notes 标明 dev/test；服务名或 command 含 `dev` / `develop` / `serve:dev` 等开发语义；用户明确说是开发环境 / 开发栈。**不**强制改写：人工标注或用户本会话指定的 command、生产向无 watch 的 `start`/`serve`（且无热更新候选时）、compose 依赖类服务（db/redis 等）。

### 优先热更新方式

discover 与选定 `command` 时，同一服务有多候选则按优先级：

1. 显式 watch/reload：脚本或 target 名为 `dev`、`watch`、`serve:dev`，或命令含 `--reload` / `nodemon` / `air` / `watchexec` / `cargo watch` 等。
2. 框架默认开发入口：如 `npm run dev`、`vite`、`uvicorn --reload`、带 debug/reload 的语言服务器。
3. 仅当无热更新候选时，才用普通 `start`/`serve`/`preview`，并在输出说明「无热更新入口」。

不要把「先 `build` 再静态 `preview`」当作首选开发启动，除非用户指定或仅此可起。

### 监听地址

start / restart 开发/测试原生服务时，**默认不改监听配置**（工具自身默认多为 `127.0.0.1`，仅本机可达）。宽绑定 `0.0.0.0` 仅用于局域网/真机联调需求，且绑定前 MUST 确认当前网络可信——公共 Wi-Fi 等不可信网络会向同网段暴露本机服务：

1. 先看 command / notes / 环境是否已宽绑定（已含 `0.0.0.0`、`--host 0.0.0.0`、`HOST=0.0.0.0` 等）→ 不再追加。
2. 仅当用户明确需要局域网/真机访问、或台账 notes 已声明宽绑定，且网络可信时，按栈用**可逆、常见**方式补绑定（优先环境变量，其次该工具官方 host 参数），且不得关掉热更新：

| 栈 / 线索 | 优先补法（示例） |
|-----------|------------------|
| Vite / webpack-dev-server | `--host 0.0.0.0` 或 `HOST=0.0.0.0` |
| Next.js | `-H 0.0.0.0` |
| uvicorn / gunicorn | `--host 0.0.0.0` |
| Flask | `--host 0.0.0.0` |
| Django `runserver` | `0.0.0.0:<port>` |
| 读取 `HOST` 的 Node 脚本 | `HOST=0.0.0.0` |

3. 无法安全推断补法 → 仍用原 command 启动，在输出与踩坑注明「可能仅本机可达」，并询问期望的 host 参数；不要臆造少见 flag。
4. 成功后按冲突规则，可将实际生效的 bind（`0.0.0.0`）与「热更新：是/否」写入该服务 notes。

## 探索启动方式（discover）

在项目根及明显子目录（如 `frontend/`、`server/`、各 package）**合并多源**结果，不要因已有 Makefile 就跳过 package.json / compose。

扫描顺序（后源可追加服务；同名服务保留更具体者：子目录 package 脚本 > 根 Makefile 泛化 target，并在输出说明）：

1. **先读** `.service-manager.md`（若存在），并校验其中 `Profiles` 与服务 `recipe` 引用的服务都存在、脚本路径不越出项目根。
2. **Makefile** / **Justfile** / **Taskfile.yml**：关注 `run`、`start`、`dev`、`serve`、`up`、`server`、`watch` 类任务；读内容确认实际命令；同服务多候选时按「优先热更新方式」选取。
3. **package.json**（含 workspace 子包）：`scripts` 中的 `dev`、`watch`、`start`、`serve`、`preview`；注意 pnpm/npm/yarn；同包多脚本时优先 `dev`/`watch` 等热更新入口。
4. **docker-compose.yml / compose.yaml**（及 `-f` 常见覆盖文件）：服务名即单元；记录 `compose_file` 与 compose 所在 `cwd`；区分 `docker compose` 与 `docker-compose`。
5. **其他线索**（补充，非「前几项全空才看」）：`pyproject.toml` / `manage.py` / `app.py`、`go.mod`+`cmd/`、`Cargo.toml`、`Procfile`、`mise.toml` tasks、README 启动段落。
6. 推断端口；推不出留空，start 后从日志或 `ss -tlnp` 补。
7. 结束 → 更新缓存，并同步/创建 `.service-manager.md`。

无法确定任何启动方式时，列出线索并问用户，不要瞎猜命令。

## 身份匹配（原生进程）

判断缓存中的 pid/pgid 是否仍是本服务时，按下列**可执行**规则（任一足够则匹配；均失败则视为不匹配）：

1. pid 仍存在（`kill -0`），且其 **pgid** 等于缓存 `runs.<name>.pgid`（若有）。
2. 否则：`ps -p <pid> -o args=` 的命令行包含 command 中的**关键可执行名或脚本名**（如 `node`、`uvicorn`、`make`、包名），而非要求整串全等。
3. `npm`/`pnpm`/`yarn`/`make` 启动的，允许实际进程为子进程（`node`/`python` 等）；此时以 **pgid 或进程树属于缓存 pgid** 为准。

不匹配 → 不 kill，列出候选并问用户。

## 运行状态判定

优先级（高 → 低）：

1. **compose**：`docker compose ps` 为 running → running。
2. **缓存 pgid/pid 匹配且进程存活** → running（即使端口尚未监听，标 `starting` 若未满健康等待窗）。
3. **端口已被本服务身份占用** → running。
4. **仅端口被未知进程占用** → 标 `port_busy`，不要当成已由本 skill 启动；start 前先问用户。
5. 否则 → stopped。
