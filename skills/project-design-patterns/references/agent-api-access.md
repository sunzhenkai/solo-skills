# 模式卡：agent 数据接入

> 应用如何让外部 agent 安全地管理自己的数据；agent 侧如何接入与操作。三处独立落地验证。

## 动机

外部 agent（个人助手、脚本、自动化流程）需要管理应用数据（日程、笔记、配置、消息等），但不应依赖应用的图形界面或人工会话：GUI 自动化脆弱，桌面会话凭证（OAuth 换发的 JWT / cookie）不适合长期第三方持有。应用需要一个面向 agent 的稳定凭证与操作契约。

## 参与者

| 参与者 | 职责 |
| --- | --- |
| 应用服务端 | API Key 签发与鉴权（全部业务接口可达，凭证管理除外） |
| 应用设置页 | Key 管理（创建时明文只显一次）+ 一键复制「agent 接入话术」 |
| 通用操作规范 | agent 侧规范：凭证落盘、认证方式、API 详情获取、操作纪律（本 skill 的 [agent-api-ops.md](agent-api-ops.md)） |
| agent | 收到话术 → 装 skill → 存 Key → 经 HTTP API 完成业务操作 |

## 落地件（应用侧四件套）

1. **API Key 模型**：独立表（`user_id` + `name` + `key_hash` + `prefix` + `last_used_at`）；只存 SHA-256 哈希，明文仅创建响应返回一次；每用户限量；删除即吊销。
2. **全接口授权**：鉴权中间件按 Bearer 前缀自识别凭证类型（`hela_sk_…` / `hela_pt_…` / 会话 token 同族前缀区分）；Key 放行全部业务接口；**Key 不能管理凭证与登出**（403，需应用端会话）。
3. **设置页分区**：创建（弹窗展示明文 + 复制）/ 列表（前缀 + 最近使用）/ 删除；一键复制接入话术。
4. **接入话术**：一次性给全 agent 所需——base_url、Key、通用 skill 安装命令、应用 skill 接口地址（无 skill 接口的应用以内嵌端点概览兜底）、认证约定、401 处理与凭证边界。话术只带指针，端点细节由应用 skill 接口权威发布，避免双处漂移。

（agent 侧落地件即通用操作规范，见下节。）

## 通用操作规范（本 skill 引用件）

- 操作规范见同 skill 的 [agent-api-ops.md](agent-api-ops.md)（原独立 skill `agent-api-ops`，原 `app-api-ops`），不绑定具体应用；应用话术安装整个 `project-design-patterns`：`npx skills add sunzhenkai/solo-skills -s project-design-patterns -g -y`。
- 内容：解析话术 → 凭证落盘（`~/.agent-state/app-keys/<app>.env`，600）→ Bearer 认证 → API 详情获取策略 → 操作纪律（先读后写、删改确认、401/403/429 语义）。
- **版本化**：`project-design-patterns` 的 SKILL.md frontmatter 带 `version`（规范或契约变化即 bump）；应用 skill 接口头部声明 `skill: project-design-patterns@X.Y.Z`，agent 会话首次操作前比对，本地低于声明版本则用安装命令覆盖升级（检查与升级尽量交给 subagent，主会话只收结论）。应用版本与模式库解耦演进，安装单元只有一个。
- 应用话术直接引用安装；应用自身可另备专属 skill（端点细节、字段说明），两者并行。

## 变体：API 详情的获取通道

话术必须让 agent 拿到「调什么端点」，两条通道按应用能力选：

- **应用侧 skill 接口**（推荐）：应用提供 `GET /skill.md`（或 `/api/v1/skills` 列表）自描述发布，永远与应用版本一致。先例：llmwiki（`go:embed` + `/skill.md` + `/api/v1/skills`）、另一条个人产品线（`/skill.md` 免鉴权）。通用操作规范约定「有则先 fetch」。
- **话术内嵌端点概览**：应用暂无 skill 接口时的兜底，话术直接携带端点表。缺点：接口演进要同步改话术文案，且与实现存在漂移风险。

## 边界

- Key 明文只出现一次（创建响应 / 弹窗）；服务端与列表永不回显，只存哈希与前缀。
- Key 权限 = 业务全接口 − 凭证管理 − 会话操作；管理类动作一律回应用端。
- 话术含密钥，属敏感内容：提示用户保管，agent 输出只显前缀。
- Key 泄露 / 换设备：删除重建，更新 agent 侧保存的配置。

## 先例

| 应用 | Key 形态 | 存储要点 | API 详情通道 |
| --- | --- | --- | --- |
| 个人办公产品线 A | `sk_<app>_…` | hash + AES-GCM 密文；鉴权先 Key 后 cookie 会话 | 应用 `/skill.md` |
| hela | `hela_sk_…`（与推送 token `hela_pt_` 同族） | SHA-256 哈希；Key 覆盖业务接口、管凭证 403 | 应用 `/skill.md`（go:embed 随版本发布，头部声明 `skill: project-design-patterns@1.1.0`）+ 话术指针 |
| llmwiki | （会话之外无独立 Key，API 面向本机 / 可信网） | — | `/skill.md` + `/api/v1/skills` 自描述 |

## 更正记录

- 2026-11-22：初版，从 hela-agent-api 任务收口提炼（通用操作 skill 的更名史见上文与 archive 登记）。
- 2026-11-22：hela 补上自身 `/skill.md` 端点，落地件 4 与变体通道更新——话术统一改为指针，内嵌概览降为无 skill 接口应用的兜底；API 详情获取策略定为「应用 skill 接口优先」。
- 2026-11-22：通用操作 skill 引入版本化与升级通道（skill `version` + 应用声明期望版本 + 会话首用比对，尽量 subagent）。
- 2026-11-23：`agent-api-ops` 并入本 skill，成为 [agent-api-ops.md](agent-api-ops.md) 引用件（不再独立安装）；安装/升级命令与版本声明统一走 `project-design-patterns`（本版 1.1.0），应用话术同步。
