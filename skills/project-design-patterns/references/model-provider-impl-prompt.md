# 实现 Prompt：模型供应商配置（models.dev + 两级联动）

> 本文件是 `project-design-patterns`「[模型供应商管理](model-provider-management.md)」模式卡的可复用实现 Prompt。在新项目或现有项目中接入供应商管理时，替换下方参数表后直接发给实现 agent。

## 使用参数（使用前按项目替换）

| 占位符 | 说明 | 示例 |
| --- | --- | --- |
| `{{技术栈}}` | 后端语言/框架、数据库、前端框架/组件库 | `TypeScript + Hono + PostgreSQL + React + shadcn/ui` |
| `{{支持协议清单}}` | 需支持的模型调用协议 | `openai / anthropic / ollama` |
| `{{网络策略}}` | `公网严格 HTTPS（禁内网 IP）` 或 `个人/局域网应用（允许 http:// 与本地服务）` | `个人/局域网应用（允许 http:// 与本地服务）` |
| `{{模型消费场景清单}}` | 需要选择模型的功能入口 | `默认对话模型、后台任务模型（支持沿用默认）、会话内临时模型切换` |

---

## 可复用 Prompt 正文

```text
请在本项目中实现一套完整的「模型供应商管理与两级联动」能力，技术栈为 {{技术栈}}，支持协议 {{支持协议清单}}，网络校验策略采用「{{网络策略}}」，模型消费场景包括：{{模型消费场景清单}}。

### 一、核心设计约束
1. **目录驱动 + 手动兜底**：
   - 接入 `https://models.dev/api.json` 作为供应商与模型元数据目录，同时保留离线兜底快照与手动配置模式（`catalog_id = "custom"`）。
   - 启动时若目录缓存为空则加载内置快照；后台异步检查上次同步时间，超过 24 小时自动同步；提供手动触发同步与目录状态查询接口（使用单飞锁防并发重复同步）。
2. **在供应商实例中确定可用模型**：
   - 供应商实例数据模型必须包含：`id`、`name`、`catalog_id`、`api_format`、`base_url`、`api_key`（服务端保存，接口只返回脱敏掩码）、`models`（已选模型 ID 列表，至少 1 个，首项为首选模型）。
   - 编辑实例时，若 `api_key` 留空则保留原密钥不变。
3. **消费端两级联动（禁止跨实例错配与盲输）**：
   - 所有消费场景（{{模型消费场景清单}}）的模型选择器必须与 Provider 实例选择器两级联动。
   - 模型下拉选项**严格来自当前选中实例的 `models` 列表**，不展示未在该实例中选中的目录模型。
   - 切换 Provider 实例时，若新实例也包含当前模型则保留，否则自动切换为新实例的首选模型（`models[0]`），并原子保存 `(instance_id, model)`。
   - 若存在支持「沿用默认」的场景（如后台任务模型），选择「沿用默认」时清空该场景的实例与模型覆盖并禁用模型下拉。

### 二、后端要求
1. **数据存储与迁移**：
   - 目录缓存表：`provider_info_cache`（含 `id`、`name`、`api_base`、`api_format`、`npm` 等）与 `provider_models_cache`。
   - 实例表：`provider_instances` 持久化 `api_format` 与 `models`（JSON 数组），更新接口支持按字段部分更新。
   - 确认全局设置允许保存各消费场景的 `*_instance_id` 与 `*_model` 键（检查白名单，勿静默丢弃）。
2. **HTTP API（注意静态子路径必须在 `:id` 动态路由之前注册）**：
   - `GET /api/v1/providers`（支持 `?q=` 搜索与可选 `?limit=`）与 `GET /api/v1/providers/:id/models`
   - `GET /api/v1/providers/catalog-status`（返回 `availability: available | fallback | empty`、数量、上次同步时间与错误）
   - `POST /api/v1/providers/sync`（单飞同步 `models.dev` 并返回最新状态）
   - `GET/POST/PUT/DELETE /api/v1/provider-instances`（创建/更新时校验 `models` 非空数组、去重、单条 ≤256 字符、上限 64；`api_format` 合法；`base_url` 符合 {{网络策略}}）
   - `POST /api/v1/provider-instances/models`（接收 `instance_id` 或草稿 `{ api_format, base_url, api_key }`，由服务端请求上游 `/models` 或 Ollama `/api/tags` 返回实时模型 ID 列表；Anthropic 若 base URL 未带版本号则自动补 `/v1/models`）
   - `POST /api/v1/provider-instances/test`（接收 `instance_id` 或草稿参数探测连通性，返回 `ok` / `unauthorized` / `error`）

### 三、前端弹窗与设置页要求
1. **添加 / 编辑 / 复制 Provider 实例弹窗**：
   - 顶部提供「来自 models.dev」与「手动配置」两个 Tab；目录未就绪时给出提示与一键同步按钮。
   - 「来自 models.dev」Tab 使用可搜索 Combobox 选择供应商（展示名称、ID、无默认端点标记），选中后按 `npm`/ID 自动推断 `api_format` 与 `base_url`；使用 `touched` 状态保护用户手改过的名称与 Base URL 不被覆盖，并支持「使用目录默认值」一键重置。
   - 切换协议格式时，若用户未手改 Base URL，自动在已知双协议端点间切换或做 `.../anthropic[/v1]` ↔ `.../v1` 路径投影。
   - **使用的模型**区块：
     - 候选列表 = `models.dev` 该供应商模型 ∪ 端点实时 `/models` 拉取结果（防抖 400–500ms；编辑态未改地址和密钥时自动传 `instance_id` 复用已存凭据）。
     - 提供可搜索多选 Combobox，支持勾选/取消多个模型；当搜索词不在候选中时提供「添加自定义模型」选项。
     - 下方展示已选模型列表，首项标注「首选」，其余项支持「设为首选」与「移除」；至少选 1 个模型才允许提交。
   - 弹窗内提供「测试连接」按钮并内联展示探测结果。
2. **实例列表与消费端设置页**：
   - 实例列表展示已选模型摘要（首模型 + `另 N 个`）、协议、Base URL、脱敏 Key，以及「检查 / 编辑 / 复制 / 删除」操作和目录同步状态栏。
   - 按「核心设计约束 3」实现所有消费场景（{{模型消费场景清单}}）的两级联动选择器，后台执行逻辑也要与所选实例+模型保持一致（不把 A 实例的模型配给 B 实例）。

### 四、验收清单
1. 后端：`models.dev` 转换与同步、实例 CRUD（含 `custom` 模式、留空保留密钥、`models` 校验）、实时 `/models` 发现、草稿/已存连接测活、设置白名单持久化均通过单元测试。
2. 前端：自动填充与双协议路径投影、候选合并去重、切换实例时模型联动解析均通过单元测试；前后端 `typecheck` 与 `build` 零错误通过。
3. 手工/端到端：从 `models.dev` 选一个供应商并勾选 2 个模型保存 → 默认模型与任务模型下拉只出现这 2 个模型 → 切换实例时模型自动切换为新实例首选模型 → 刷新页面后配置保持不变。
```
