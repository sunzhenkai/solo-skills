# 模式卡：接口访问统计

> 在线服务如何以非阻塞、防基数爆炸、零明文泄漏的方式采集 HTTP 访问明细，提供精确分位聚合与 API Key 专项下钻面板。14 处跨技术栈服务独立落地验证。

## 动机

在线服务上线后常面临四类可观测性与治理盲区：
1. **同步写库拖慢业务**：在请求路径上同步写统计日志会放大尾延迟，DB 抖动时直接拖垮核心接口；
2. **原始路径基数爆炸**：扫描器探测大量随机 404 路径或带动态 ID 的 URL，导致聚合查询与索引失效；
3. **API Key 缺乏专项归因**：无法区分浏览器会话与外部 Key/Token 调用，也无法在 Key 吊销后保留历史用量或追踪无效 Key 的 `401` 暴力试探；
4. **自查统计越权与明文泄漏**：若允许 API Key 查询统计或把原始 query / `Authorization` 落库，会造成凭据自查越权或敏感信息外泄。

## 参与者

| 参与者 | 职责 |
| --- | --- |
| 采集中间件 | 记录起止耗时、状态码、框架归一化路由模板与鉴权归因，清洗脱敏后投递有界队列 |
| 异步有界采集器 | 维护内存有界队列与后台批量写入 worker，满队丢弃降级，并周期性分批清理过期行 |
| 明细表（`api_access_logs`） | 存储结构化访问事实与 Key 快照（无硬外键级联删除），支撑多维筛选与精确分位聚合 |
| 只读统计查询 API | 提供 5 个标准只读端点，执行会话/角色/内网门禁，禁止 API Key 自查 |
| 统计面板（Web / 内嵌页） | 呈现时间范围筛选、KPI、趋势图、路由排行、错误明细及「概览 / API Key 专项」双 Tab 下钻 |

## 落地件（五件套）

1. **统一明细数据模型与无硬外键快照**：
   - 统一表 `api_access_logs`（已有同构审计表的服务可增量补齐列复用）：主键 `id`、`occurred_at`（UTC）、`method`、`route_template`、`status_code`、`duration_ms`（非负整数）、`auth_type`（`session` | `api_key` | `anonymous` | `invalid_key`）、`user_id`（字符串化兼容 UUID/Int）、`api_key_id`、`api_key_prefix`、`api_key_name`、`auth_outcome`（`ok` | `unauthorized_401` | `forbidden_403` | `rate_limited_429` | `error_5xx`）、`client_ip`、`user_agent`（截断 200 字符）、`error_code`（仅 `>=400`）。
   - `api_key_id` **不设硬外键级联删除**，写入时同步保存 `api_key_prefix` 与 `api_key_name` 快照，确保 Key 吊销后历史用量与趋势不丢失；查询 `api-keys` 时再左联或对比活跃列表标出 `active` / `revoked`。
   - 最低索引集合：`(occurred_at DESC)`、`(route_template, occurred_at DESC)`、`(status_code, occurred_at DESC)`；带 Key 服务加 `(api_key_id, occurred_at DESC)`；多用户隔离服务加 `(user_id, occurred_at DESC)`。

2. **有界异步批量采集与降噪 / TTL 治理**：
   - **有界队列**：内存队列容量上限 `2048`，后台 worker 每 `1–2s`（如 `1500ms`）或满 `50–100` 条（如 `64` 条）批量写入（PG 可用 `unnest` 批插，SQLite 启用 WAL 模式事务批插）；优雅停机时排空刷盘。
   - **满队丢弃降级**：队列满时直接丢弃新事件，累加内部 `dropped_count` 指标并输出节流 `warn` 日志，绝不阻塞业务响应。
   - **开关与测试钩子**：提供 `API_STATS_ENABLED`（默认 `true`）一键关闭开关，以及同步直写测试钩子（`syncWrite`）供单测确定性断言。
   - **默认降噪**：跳过静态资源后缀（`.js`/`.css`/`.png`/`.svg`/`.ico`/`.woff2`/`/_next/static/*`/`/assets/*`）、健康探活（`/health`、`/healthz`、`/readyz`、`/livez`）与统计接口自身正常轮询路径（`*/api-stats*`、`/stats/api*`）。
   - **TTL 分批清理**：默认保留 `30` 天（`API_STATS_RETENTION_DAYS=30`），后台每小时按 `LIMIT 5000` 分批删除过期行，避免长事务锁表。

3. **框架原生路由模板归一化与 `/_unmatched` 折叠**：
   - 必须使用路由匹配后的模板（如 `/api/items/:id`）而非原始 URL 路径；未匹配任何路由的 404 / 405 扫描统一折叠为 `/_unmatched`。
   - **鉴权短路与 SPA fallback 注意点**：中间件在路由前短路返回 401/403 时需确保仍解析路由模板（或由路由后置钩子回填）；带前端 SPA fallback 的服务须对未匹配 `/api/*` 请求显式返回 404，防止 fallback 吞掉 404 导致 `/_unmatched` 失效。

4. **5 端点只读查询契约与精确分位**：
   - 通用筛选参数：`range=1h|24h|7d|30d`（默认 `24h`，可选 `from`/`to`）、`method`、`route`、`status_class=2xx|3xx|4xx|5xx`、`auth_type`、`api_key_id`。
   - 5 个标准端点（挂载前缀按服务风格，如 `/api/v1/api-stats`、`/api/admin/api-stats` 或 `/stats/api`）：
     1. `GET <prefix>/overview`：`capabilities`（`{ has_api_keys, scope: "global"|"user" }`）、`summary`（`total_requests`, `rps`, `success_rate`, `error_4xx_rate`, `error_5xx_rate`, `avg_duration_ms`, `p50_ms`, `p95_ms`, `p99_ms`, `active_routes`）、`series`（分桶请求量、4xx、5xx、p95）、`status_distribution`、`auth_sources`。
     2. `GET <prefix>/routes`：支持 `sort=count|error_rate|p95` 与 `limit`（默认 50），返回归一化路由排行。
     3. `GET <prefix>/errors`：返回最近 50–100 条 `status_code >= 400` 明细（不含请求体与敏感字段）。
     4. `GET <prefix>/api-keys`（仅 `has_api_keys=true`）：返回 `summary`（含 `unauthorized_401_count`、`forbidden_403_count`）与按 `api_key_id` 聚合的 `items`。
     5. `GET <prefix>/api-keys/:keyId`：返回单 Key 趋势 `series`、Top 路由、错误路由与最近错误；`:keyId = "__invalid__"` 时聚合无效/已吊销 Key 的 `401` 试探。
   - **精确分位**：PostgreSQL 使用 `percentile_cont(0.50/0.95/0.99) WITHIN GROUP (ORDER BY duration_ms)`；SQLite / 内存聚合在应用层排序后做线性插值，与 `percentile_cont` 语义一致。

5. **前端双 Tab 面板与单 Key / `__invalid__` 下钻**：
   - 沿用既有 UI 体系（或无构建服务使用 `go:embed` / 单文件只读 HTML + 原生 SVG），不强行引入重型图表库。
   - 必含区块：顶部时间范围与多维筛选条 → KPI 卡片组 → 请求量/错误/延迟趋势图 → 状态码与来源分布 → Top 接口排行（支持排序与点击下钻）→ 最近错误明细表。
   - 带 API Key 服务内置「概览 / API Key 专项」双 Tab：展示 Key 专项 KPI（含 401/403 计数）、Key 用量排行与单 Key / `__invalid__` 下钻抽屉。

## 多栈适配器对照

| 技术栈 | 路由模板提取方式 | 特殊适配注意点 |
| --- | --- | --- |
| Hono | `routePath(c)` / `matchedRoutes(c)` | 挂在 trailing-slash 重写中间件之后 |
| Fastify | `request.routeOptions.url` | 未命中路由时 `url` 为空，折叠为 `/_unmatched` |
| Next.js App Router | Route Handler 包装器 `withApiStats(pattern, handler)` | 补 `[...unmatched]/route.ts` 兜底路由折叠 404 |
| FastAPI | `request.scope["route"].path` | 中间件短路 401/403 时需遍历 router 匹配模板 |
| Django | `request.resolver_match.route` | 补前导 `/` 并转换 `<type:name>`；异常/404 折叠 `/_unmatched` |
| Go Gin | `c.FullPath()` | 空串即未匹配路由，折叠为 `/_unmatched` |
| Go chi | `chi.RouteContext(r.Context()).RoutePattern()` | SPA fallback 须放行 `/api/*` 404 |
| Go `net/http` | `r.Pattern`（Go 1.22+） | `ServeMux` 未命中时 `r.Pattern == ""`，折叠为 `/_unmatched` |

## 边界

- **API Key 禁止自查统计**：所有携带 API Key / Agent Key / Service Token 的请求访问统计 API 或面板，一律返回 `403`。
- **多用户隔离**：有用户体系的服务，管理员看全局（`scope="global"`），普通用户仅看本人（`user_id = current_user.id`）与本人名下 Key（`scope="user"`）。
- **公网无会话服务 `LANOnly` 门禁**：暴露公网且无独立用户会话的服务，统计页面与 `/stats/api*` 强制走 `LANOnly`（校验 `RemoteAddr` + `X-Real-IP` + `X-Forwarded-For` 全链路为私网/回环 IP，并校验 `Host` / `X-Forwarded-Host` 允许名单，fail-closed，公网一律 403）。
- **零明文脱敏**：绝不记录或回显完整 API Key、`Authorization` 头、query 中的 `token`/`key`/`secret`/`password` 参数值、请求体或响应体；预置静态 Token 服务仅记 `sha256(token)[:8]`（如 `tok_<hash8>`）与角色标签；`client_ip` 与 `user_agent` 须清洗换行与控制字符。
- **可开关与安全回滚**：支持 `API_STATS_ENABLED=false` 关闭采集；迁移仅新增表或可空列，可无损回滚。

## 先例

| 应用形态 | 技术栈与存储 | Key 专项与门禁策略 | 面板落点 |
| --- | --- | --- | --- |
| 个人笔记知识库 | Hono + React / PG | `api_keys` 专项；会话/可信网可用，Key 403 | Web 设置页双 Tab + SVG 趋势图 |
| 个人助手服务端 | Gin + 内嵌页 + 桌面端 / PG | `api_keys` 专项；`/api/v1` 按 `user_id` 隔离，`/status` 走 `LANOnly` | 内嵌状态页 + 桌面端设置页 |
| 个人投资工作台 | FastAPI + React / SQLite & PG | `agent_api_key` 专项；开放/认证双模式隔离，Key 403 | 设置页双 Tab + 抽屉下钻 |
| 商贸办公应用 | Hono + React / PG | `api_key` 专项；admin 全局 / member 本人，Key 403 | 设置侧栏「访问统计」 |
| 视觉创作工作台 | Hono + React / PG | `api_key` 专项；super_admin 全局 / 普通用户本人，Key 403 | 设置页「访问统计」 |
| 知识库全栈应用 | Hono + React / PG | MCP Key 专项；仅 admin 会话，MCP Key 403 | 管理设置页双 Tab |
| 个人博客系统 | Next.js + Drizzle / PG | API Token 专项；仅 admin 会话，Token 403 | `/admin` 子页（`withApiStats` + `[...unmatched]`） |
| 局域网个人工具集 | Hono + React / PG | 通用 3 端点（无 API Key）；登录会话 | 设置页「接口统计」 |
| 数据门户 | Django + SPA / PG & SQLite | 通用 3 端点（无 API Key）；内网门禁 | 门户统计 Tab |
| 通用 Agent 平台 | Fastify + React / PG | 预置 Service Token（`sha256[:8]`）专项；控制台会话，Token 403 | 设置页运行态面板 |
| 待办效率应用 | Django + React / PG & SQLite | 通用 3 端点（无 API Key）；admin 全局 / 普通用户本人 | 设置页「接口统计」 |
| 文件中转服务 | FastAPI / 本地 SQLite WAL | 预置读写 Token（`sha256[:8]`）专项；`LANOnly` fail-closed + Token 403 | 零构建单文件 HTML `/stats` |
| 简易制品服务 | Go chi + React / SQLite | 通用 3 端点（无 API Key）；内网边界 | Web 内嵌 SPA「访问统计」Tab |
| 配置同步服务 | Go `net/http` / PG 扩展 `access_log` | client/token 专项；`LANOnly` fail-closed + Token 403 | `go:embed` 内嵌 HTML `/stats` |

## 更正记录

- 2026-11-28：初版，从 14 个在线服务统一落地「接口访问统计面板（含 API Key 专项统计）」任务收口提炼。
