# 阶段（命令）详情

> 文中引用的「启动解析」「Profiles & Recipes」见 [info-file.md](info-file.md)，「开发/测试启动约定」「运行状态判定」「身份匹配」见 [start-conventions.md](start-conventions.md)。

## 阶段

用户消息中的第一个词（或语义）决定 phase；缺省为 `list`。

### list

- 读 `.service-manager.md`（若有）与缓存，或 discover；表格：name、source、command、port、运行状态。
- 缓存命中时说明「来自缓存」；源文件 mtime 变了则先重新 discover。

做完的标志：表格每行都有 name、source、command、port、运行状态（未知写「待确认」）。

### start `<name>` 或 `@<profile>`

**缺 name 时**：

- 仅 **1** 个已知服务 → 可直接起该服务并说明。
- 多个服务 → **默认询问**要起哪些；仅当用户明确说「全部 / all」时才全起。
- 全起时按依赖常识排序（db/redis 等先于 app）；无依据则按 list 顺序并声明。

步骤：

1. 查 `.service-manager.md` / 缓存；没有则先 discover。按「启动解析」识别单个 service 或 `@<profile>`。
2. 单个 service 已在运行（见「运行状态判定」）→ 告知并跳过；profile 已运行的成员跳过。
3. **环境**：若 notes/文档要求 `.env`，检查 `<cwd>/.env`（或项目根）；缺且存在 `.env.example` → 先告知并询问是否 `cp`，未经同意不擅自复制；缺依赖运行时则写入踩坑并停下。
4. **准备**：先执行 profile `prepare`；原生 service 有 `recipe` 时执行其 `prepare`，再用 `<recipe> start` 替换裸 command 进入下一步。开发/测试原生服务仍按「开发/测试启动约定」确认热更新入口与 `0.0.0.0` 绑定；得到实际执行用的 command 或 recipe 动作（可与缓存原文不同，成功后按冲突规则写回）。
5. 后台启动（原生）——**新进程组**，便于整组停止：
   ```bash
   mkdir -p ~/.cache/service-manager/logs/<ph>
   cd <cwd> && setsid nohup <command> >> ~/.cache/service-manager/logs/<ph>/<name>.log 2>&1 & echo $!
   ```
   记录 `pid`、`pgid`（`ps -p <pid> -o pgid=`）、`log`、`started_at`。
   compose：在 compose 文件所在目录执行 `docker compose -f <compose_file> up -d <name>`（必要时加 project 名）；记 `container` 与 `compose_file`，不记 pid。
6. 写回缓存 `runs`。
7. **就绪验证**（单个 service 默认 2–5s，慢服务可延长到 ~30s；profile 用总窗口 ~30s，或看 `.service-manager.md` 的 health/notes）：
   - 进程/容器仍在；
   - 有端口则已监听（开发服务期望绑在 `0.0.0.0` 或全网卡；若实际仅 `127.0.0.1` 且本应宽绑定，记入踩坑）；
   - 若配置了 HTTP health / 日志就绪关键字，一并满足。
   失败 → tail 项目隔离日志，写踩坑；profile 输出成员汇总，不隐藏已成功成员。
8. 成功 → 按冲突规则同步 `.service-manager.md`（含实际 bind / 是否热更新 / recipe 生效结果，若适用）。

做完的标志：第 7 步就绪验证全部满足并已写回 `runs`；或失败已附日志尾、踩坑已写。

### stop `<name>`

1. **compose**：在对应 cwd 用同一 `compose_file` 执行 `docker compose stop <name>`，清理 `runs`。
2. **原生优先整组停**：有 `runs.<name>.pgid` 且身份匹配 → `kill -- -<pgid>`（向进程组发信号）；5s 未退再对**同组** `kill -9 -- -<pgid>`。
3. 仅有 pid、无 pgid：身份匹配后 `kill <pid>`，再查是否仍有子进程占端口；有则列出候选问用户，**不要**直接 `fuser -k`。
4. **禁止默认** `fuser -k <port>/tcp` / 无差别 `lsof ... | xargs kill`。仅当用户明确授权「按端口杀」且已展示将杀进程的 pid/命令行后才可执行。
5. pid/pgid/容器都对不上 → 不猜杀，列候选请用户确认。
6. 新坑立刻写入 `.service-manager.md`。

做完的标志：目标进程组 / 容器已退出、端口已释放、`runs` 已清理；对不上的已列候选交用户。

### restart `<name>` 或 `@<profile>`

`stop` 后 `start`；复用已有命令，不重新 discover（除非 start 失败需再探索）。缺 name 时规则同 start；`@<profile>` 对成员逐个 stop 后 start。

做完的标志：stop 与 start 各自的标志都满足。

### status `[name]`

按「运行状态判定」输出：running / starting / stopped / port_busy，以及 pid/pgid 或 container、端口、启动时长。

做完的标志：每个目标服务都给出四态之一及其证据（pid/pgid 或 container、端口）。

### logs `<name>` `[行数]`

- 原生：`tail -n <行数, 默认 50> ~/.cache/service-manager/logs/<ph>/<name>.log`（旧路径仅回退）。
- compose：`docker compose -f <compose_file> logs --tail <行数> <name>`。

做完的标志：输出了指定行数的日志尾，并注明日志路径。
