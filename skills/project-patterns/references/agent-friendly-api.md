# 模式卡：Agent 友好 API 设计

> 应用如何为 Agent 提供高效率、低漂移、可回滚的业务资源接口（与鉴权接入解耦，专攻资源契约、并发控制、批处理、精准检索与多通道对齐）。

## 动机

传统面向人类 UI 的 CRUD 接口在 Agent 场景下存在明显摩擦：

1. **全量读写浪费且易丢数据**：修改几行正文被迫先 GET 全文再 PUT 覆盖，既浪费上下文又容易并发写丢。
2. **目录与结构调整脆弱**：`mkdir` 重复报错、移动目录遇到同名目录直接失败、删目录打平子层级，迫使 Agent 手工循环搬运。
3. **缺少原子批处理与预演**：多页拆合/迁移只能逐个发请求，中途失败留下半成品且产生碎片历史。
4. **检索模糊且降级静默**：缺少子目录/标签/时间/精确短语或正则过滤，向量检索不可用时静默退回关键词却仍回报 `hybrid`，导致 Agent 误判「库里没有」。
5. **HTTP / MCP / Skill 契约漂移**：同一动作在 HTTP 与 MCP 侧副作用（历史记录、引用图重建、目录总览刷新）或权限边界不一致，甚至未登记工具默认放行。

## 参与者

| 参与者 | 职责 |
| --- | --- |
| 业务 API 与共享引擎 | 提供双寻址、纯函数局部补丁、乐观锁、事务批处理（`dry_run`）与多维检索，并统一副作用 |
| MCP / 工具适配层 | 复用同一用例服务层暴露工具，执行 deny-by-default 权限控制 |
| 自描述 Skill 文档 | 与接口同仓演进，准确声明端点、锁字段、批量与检索契约 |
| 调用侧 Agent | 按操作纪律优先局部修改、携带乐观锁、批量前先 `dry_run` |

## 落地件（六件套）

1. **双寻址与富过滤列表**：
   - 资源同时支持 **稳定 ID** 与 **逻辑相对路径** 寻址（如 `GET .../by-path?path=&include_content=false`），减少先 list 再过滤的 N+1 往返。
   - 列表端点返回真实元数据（如 `tags`），支持目录前缀、标签（`any`/`all`）、时间区间与标准分页（`limit`/`offset`/`total`/`has_more`）。
2. **原子局部 Patch 与乐观锁**：
   - 文本类资源提供共享纯函数补丁引擎（如 `replace`、`replace_lines`、`append`、`prepend`、`insert_after`），默认唯一匹配并明确错误分型：`422` 未找到、`409` 多处命中（返回命中次数与行号）、`400` 行号越界。
   - 全部单资源写端点支持可选乐观锁（`expected_version` / `expected_content_hash` / `expected_sha256` 或 `If-Match`），不匹配返回 `409 Conflict` 并回传当前版本与哈希。
3. **幂等与合并式结构操作**：
   - 目录创建支持 `exist_ok: true`，已存在时直接返回 `200` 与现有元信息。
   - 目录移动支持 `on_conflict?: "fail" | "merge"`；`merge` 在事务内预检全部目标路径冲突，有冲突整事务回滚并返回 `409` 与完整 `conflicts[]`。
   - 目录迁移或父级归并保持相对子目录层级，不打平子目录。
4. **原子批处理、批量读与 `dry_run`**：
   - 需要跨资源协同且要求统一回滚的域（如知识页面拆合/重排），提供单事务单 `change_set` 统一批处理（如 `POST /documents/batch`），设单批上限（如 100），合并后置副作用（链接重写、索引与图谱刷新），并支持 `dry_run: true`（事务内完整校验与预演后回滚）。
   - 无跨操作组合需求的二进制/原始文件域，提供语义直白的分端点 `bulk-move` / `bulk-delete` / `bulk-ingest` / `bulk-link`。
   - 配套批量读 `batch-get`（支持按 `ids`/`paths` 一次读取，并按 `fields=meta|content|outline` 裁剪载荷）。
5. **多维精准检索与可观测降级**：
   - 检索支持目录前缀、标签（`any`/`all`）、时间区间与排序，SQL 层先按主实体去重（`ROW_NUMBER() OVER (PARTITION BY id ...)`）再 `LIMIT`，避免长文档多片段挤占配额。
   - 支持 `match=fuzzy|all_terms|phrase|regex` 与 `case_sensitive`；非法正则返回 `400`；`phrase`/`regex` 附带 1-based `matched_lines`。
   - 支持跨层联合检索（如 `?scope=wiki|archives|all`）与统一分页（`total`/`limit`/`offset`/`has_more`）。
   - **严禁在查询热路径同步执行耗时的 backfill/索引修复**（移至启动或后台异步任务）。
   - 混合检索降级时在响应中显式透出 `effective_mode` 与 `degraded_reason`，禁止静默掩盖。
6. **HTTP / MCP / Skill 同源契约与 deny-by-default 安全默认**：
   - HTTP API 与 MCP 工具共用删除、移动、补丁、检索及后置副作用逻辑，消除双链漂移。
   - 工具权限采用 **deny-by-default**：未显式登记进只读或写集合的工具一律拒绝执行；只读模式下拦截全部写工具。
   - 服务端自带的 `/skill.md` 与阶段 skill 文档随接口变更同步更新，避免过时警告误导 Agent。

## 边界

- **与 `agent-api-access` 的职责边界**：本模式卡只管业务资源接口设计，不管 API Key 签发、Bearer 鉴权、接入话术与凭证落盘（见 [agent-api-access.md](agent-api-access.md)）。
- **不强加通用批处理引擎**：简单 CRUD 或无事务历史模型的资源不必硬上通用 `batch` DSL，分端点 `bulk-*` 更清晰。
- **硬上限与防滥用**：批量接口必须限制单批数量与单文件文本大小，正则检索必须限制模式长度并做语法预校验。
- **安全默认不妥协**：只读模式与未授权工具必须在策略层硬拦截，不能依赖提示词约束。

## 先例

| 项目 / 域 | 落地要点 | 复用意图 |
| --- | --- | --- |
| `llmwiki`（Wiki + Archives） | 完整落地六件套：共享 `text_patch` 与 `wiki_batch`、乐观锁、`on_conflict=merge`、联合检索与 `effective_mode` 降级透出、MCP `deny-by-default` 与 `skills/` 同步 | 已完整验证 |
| 通用知识库 / 个人资产 / 文档类应用 | 作为新建或重构 Agent-friendly HTTP API 与 MCP 工具时的标准设计对照清单 | 跨项目复用 |

## 更正记录

- 2026-11-28：初版，从 `llmwiki` 面向 Agent 的 Wiki 与档案 API/MCP 改造交付中提炼沉淀（与 [agent-api-access.md](agent-api-access.md) 解耦）。
