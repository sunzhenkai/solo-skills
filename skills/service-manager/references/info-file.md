# 两层信息、缓存与项目信息文件

## 两层信息

令 `<ph>` = `md5(项目根绝对路径)`。

| 层 | 路径 | 用途 | 是否进仓库 |
|----|------|------|------------|
| 运行时缓存 | `~/.cache/service-manager/<ph>.json` | 服务清单、pgid/pid/容器、日志路径 | 否 |
| 项目信息 | `<项目根>/.service-manager.md` | 启动方式、依赖、端口、踩坑 | 是（随项目走） |

日志目录：`~/.cache/service-manager/logs/<ph>/`（**按项目隔离**）。若仍存在旧路径 `logs/<name>.log`（无 `<ph>`），仅作只读回退，新写入一律进 `logs/<ph>/`。缓存与日志不提交 git。

## 信息缓存（加速再次启动）

- **先读缓存**：缓存存在且关键文件 mtime 未变 → 用缓存清单，跳过探索。
- **缓存失效或不存在**：执行 discover，完成后写入缓存。
- 缓存字段：
  - `services[]`：`name`、`command`、`cwd`、`port`、`source`、可选 `compose_file`、`health`、`recipe`
  - `profiles[]`：可选；`name`、`services`、可选 `prepare`，来源必须是 `.service-manager.md` 已声明内容
  - `discovered_at`、`source_mtimes`
  - `runs`：`name` → 原生：`pgid`、`pid`、`log`、`started_at`；compose：`container`、`compose_file`、`started_at`（不记 pid）

缓存示例：

```json
{
  "project": "/abs/path/to/project",
  "discovered_at": "2026-08-02T12:00:00Z",
  "source_mtimes": {"Makefile": 1722600000, "package.json": 1722600000, "docker-compose.yml": 1722600000},
  "services": [
    {"name": "api", "command": "make run-api", "cwd": ".", "port": 8080, "source": "Makefile"},
    {"name": "web", "command": "npm run dev", "cwd": "frontend", "port": 3000, "source": "package.json"},
    {"name": "db", "command": "docker compose up -d db", "cwd": ".", "port": 5432, "source": "docker-compose", "compose_file": "docker-compose.yml"}
  ],
  "runs": {
    "api": {"pgid": 12340, "pid": 12345, "log": "~/.cache/service-manager/logs/<ph>/api.log", "started_at": "..."},
    "db": {"container": "project-db-1", "compose_file": "docker-compose.yml", "started_at": "..."}
  }
}
```

## 项目信息文件（`.service-manager.md`）

记录**启动相关的稳定知识**：缓存管「这次怎么起」，此文件管「这个项目怎么起、踩过什么坑」。

### 冲突与覆盖

1. **人工标注优先**：条目或 notes 含「人工」「勿改」等明确标记，或用户本会话指定的 command → 不得覆盖。
2. **经验证优先于未验证**：文件中已成功 start 过并写回的 command/port，优先于缓存里未验证的 discover 结果；冲突时以文件为准并在输出说明。
3. **start/restart 成功后的校正**：仅校正**本轮实际生效**且与文件不一致的 `command`/`cwd`/`port`/前置条件；不删 notes、不改踩坑、不改带人工标记的字段。
4. **discover 补全**：只补缺失服务/字段，不覆盖已有内容。

### 何时读写

1. **任何 phase 开始时**：若文件存在则先读；冲突处理见上。
2. **discover 完成后**：不存在则先询问是否创建（含是否随项目入库），同意后才建；已存在则补全缺失项。
3. **start / restart 成功后**：按「冲突与覆盖」写回生效信息。
4. **遇到坑时立刻写入**踩坑节；同一问题更新已有条目，不重复堆砌。

### 文件模板

```markdown
# 服务管理 — <项目名或目录名>

## 概览

- 一句话说明项目如何本地跑起来
- 前置：运行时 / 包管理器 / 必需服务（如 Postgres、Redis）

## 服务

### <name>

- **command**: `...`
- **cwd**: `.` 或子目录
- **port**: 8080（未知则写「待确认」）
- **source**: Makefile / package.json / docker-compose / ...
- **recipe**: 可选；项目根相对路径，如 `.service-manager/recipes/<name>.sh`
- **notes**: 环境变量、需先 `cp .env.example .env` 等；开发/测试服务注明 bind（如 `0.0.0.0`）与是否热更新

## Profiles

### @<profile>

- **services**: `[dependency, app]`
- **prepare**: 可选；项目根相对脚本或 shell 命令，用于 build / preflight

## 踩坑

- YYYY-MM-DD：现象 → 原因 → 解决/绕过
```

### 写入原则

- 只写与**启动/停止/依赖/端口/环境**相关的信息；不写业务逻辑、密钥明文。
- 不要把 pid、pgid、临时日志路径写进此文件。
- 用户若明确要求不提交该文件，提醒可加入 `.gitignore`，但仍在本地维护。

## Project Profiles & Recipes

项目组合和项目特有构建逻辑保存在项目内；Skill 只提供通用执行协议。

### Profile

`Profiles` 是显式声明的服务组合，名字必须带 `@`，例如 `@test` / `@dev`：

1. `services` 必须引用已定义服务，并按依赖顺序书写。
2. `prepare` 可选；在项目根执行一次，退出码非 0 时停止本次启动。
3. 不自动推导 profile；未声明时不得把「测试服务」等语义映射成固定组合。用户明确说「全部 / all」时保留现有全起规则。
4. profile 名与 service 名冲突属于配置错误，fail-closed 并要求用户明确选择。

### Service recipe

服务可声明项目根相对的可执行 `recipe`，例如 `.service-manager/recipes/api.sh`。recipe 只需实现两个前台子命令：

```bash
<recipe> prepare   # 可选前置：构建、迁移检查、workspace 修复；失败必须非 0 退出
<recipe> start     # 在前台启动服务；必须加载自己的环境，但不得自行 daemonize
```

Skill 的统一职责不变：把 `start` 包进新进程组和项目隔离日志，采集 pid/pgid，执行健康验证，写回运行缓存。recipe 不得输出明文 secret；项目可从 `.env` 或其他本地环境来源加载。

### 启动解析

- `start <service>`：保持原行为。
- `start @<profile>`：执行 profile 的 `prepare`，再按声明顺序启动服务。
- 已运行的成员跳过；单个成员失败不回滚已启动成员，但要报告每个成员状态和失败日志。
- `restart @<profile>` 复用同一 profile 解析，对成员逐个 stop 后 start。
- bare 名称同时命中 service 与 profile 时停止并询问；未命中时列出可用 service/profile。
