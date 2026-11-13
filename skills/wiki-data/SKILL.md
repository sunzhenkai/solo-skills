---
id: wiki-data
name: wiki-data
description: 在本地 Markdown 工作区维护可累积、带置信度与时效的知识 wiki：摄入源文档成 typed 页面、按引用回答、总结经验和踩坑、记录业务台账、归档或重开页面、重组结构并做健康检查。用户要求整理知识、维护 wiki、ingest 本地文档、查询或复用已有知识、相似任务前查经验、archive/reopen 页面、lint/重组知识库，或点名 wiki-data 时使用。
---

# Wiki Data（本地文档）

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文。

把本地文档**编译**成可累积的 Markdown wiki：摄入时交叉引用、标出矛盾、写入持久页面。下次提问读 wiki，而不是重新从源材料拼答案。

本 skill 只操作本地文件。不启动 llmwiki 应用，不调用 MCP。不依赖 llmwiki 服务、MCP 或 SQLite。

## 非目标

- 不安装、运行或包装 llmwiki 二进制 / Web / MCP。
- 不写软件项目 spec 镜像（`project-spec-mirror` 已归档在 `archive/skills/`，需要时从那里恢复）。
- 不用 wiki 重建当前项目的架构、业务流程或规则现行说明；这些代码映射文档交给 `project-atlas`，wiki 保存决策背景、经验、台账和其他可累积知识。
- 不探索或修改业务源码（交给 `code-explore`）。
- 不做根因排查；用户明确要求查证原因时交给 `trouble-grill`，本 skill 只维护知识记录。
- 不编辑 `raw/` 中的源材料。
- 不自动 commit / push / sync 安装。
- 工作区只含纯 Markdown 目录（`raw/`、`wiki/` 等），不建 `.llmwiki/`、`.obsidian/` 等应用私有目录。

## 阶段

用户点名 `{{slash:wiki-data}}` 且首词命中下表时走该阶段；否则按意图推断，并用一行说明。写盘阶段在首次绑定前必须先 `guide` 或 `init`。

| 阶段 | 何时 | 写入 | 做完的标志 |
|------|------|------|------------|
| `guide` | 了解工作区目标、结构、覆盖与缺口 | 只读 | 已按真实 `ls` 报出目标、结构、覆盖与缺口 |
| `init` | 尚无 wiki 布局，或要把一堆本地文档收成 wiki | 确认后创建骨架 | 骨架齐全、`WIKI_ROOT` 已绑定、log 已追加 init |
| `ingest` | 把文件、粘贴文本或对话编进 wiki，总结经验或更新台账 | 确认范围后写 `wiki/` | 新写页已回读、`sources` 可追溯、lint 无 error、log 已追加 |
| `query` | 问 wiki 里已有的知识，或相似任务执行前查经验 | 默认只读；归档问答需确认 | 回答逐条带出处、置信度与时效，未覆盖处明说「wiki 尚未覆盖」 |
| `archive` | 整页被替代或不再适用 | 先给计划，确认后原地标记 | 历史与链接保留、索引归入已归档、lint 无 error、log 已追加 |
| `reopen` | 恢复已归档页面 | 核实后解除归档标记 | 当前主张已核实或降级、历史保留、索引与 log 已更新 |
| `organize` | 合并重复、搬页、补交叉引用 | 先给方案，确认后改 | 确认的方案全部落地、lint 无 error、log 已追加 |
| `lint` | 健康检查；可顺带修 error | 修 error 可直接做；warning 需说明 | 脚本 error 为 0（或剩余项已逐条说明） |

## 绑定 `WIKI_ROOT`

会话绑定一个工作区根目录 `{WIKI_ROOT}`。项目内的默认落点是 `{PROJECT_ROOT}/docs/wiki`，其中 `{PROJECT_ROOT}` 是当前项目根；用户显式指定的路径优先。

**既有布局**：`{WIKI_ROOT}/purpose.md` 与 `{WIKI_ROOT}/wiki/` 同时存在。

1. 用户指定了目录 → 绑定该目录。
2. cwd 的 `docs/wiki` 已是既有布局 → 绑定该目录，并报告路径。
3. cwd 本身已是既有布局 → 绑定 cwd，兼容已有工作区。
4. 否则将 `{PROJECT_ROOT}/docs/wiki` 作为拟创建落点，确认研究/知识范围后走 **init**。确认前不写盘。

禁止猜测家目录或机器特例路径。

## 核心不变量

1. **`raw/` 只读。** 源文件修订应作为新来源加入，不改旧文件。
2. **`wiki/` 是 LLM 维护的知识层**，写入必须尊重 `purpose.md` 与 `rules.md`（缺失则明确说缺，不编造规则）。
3. **文件系统是真理源。** 搜索用目录列表与内容检索（`rg` / 读文件）；不要假设有 FTS 索引。
4. **先搜再写，写后回读。** 业务文档默认写入 `{WIKI_ROOT}/wiki/` 下对应 typed 目录；更新已有页必须先读全文，保留旧事实与旧 `sources`。
5. **`wiki/log.md` 仅追加。** 条目格式：`## [YYYY-MM-DD] action | description`。不重排、不删历史。
6. **业务台账与操作日志分离。** 业务对象的当前状态与历史写入 `wiki/ledgers/`，不混入 `wiki/log.md`。
7. **系统页** `wiki/overview.md`、`wiki/index.md`、`wiki/log.md` 不可当业务页删除或移走。
8. **声称必须可追溯** 到存在的 `raw/` 或 `wiki/sources/` 来源；本轮对话与粘贴材料也先建来源页。没有证据就写「wiki 尚未覆盖」，不要编造。
9. **证据与时效分开。** 每页标 `confidence`，用 `last_verified` / `review_after` 记录核实与复审；回答沿用具体主张的等级，draft、deprecated、已归档、冲突与逾期内容不作为当前真理。
10. **摄入前做隐私自查。** 凭据、密钥、个人联系方式、内部主机名不写入 wiki；写成 `<REDACTED>` 并告知用户。
11. **Atlas 联动保持单一正文。** 同时需要更新两者时，先由 `project-atlas` 更新当前系统事实，再由本 skill 按确认范围保存决策、经验或台账；项目实体页可用相对 Markdown 链接指向已有 Atlas，链接不替代 `sources`。摄入与查询细则见对应 reference。

## 加载

进入阶段后 **只读该阶段详情**，其它 reference 等用到时再读。

| 阶段 | 进入时读取 |
|------|------------|
| `guide` / `init` | [references/layout.md](references/layout.md) |
| `ingest` | [references/ingest.md](references/ingest.md)；写页时再读 [references/page-types.md](references/page-types.md) |
| `query` | [references/query.md](references/query.md)；归档到 `wiki/queries/` 时再读 page-types |
| `archive` / `reopen` | [references/archive-reopen.md](references/archive-reopen.md)；改完读 [references/lint.md](references/lint.md) |
| `organize` | [references/organize.md](references/organize.md)；写页时再读 [references/page-types.md](references/page-types.md)；改完读 [references/lint.md](references/lint.md) |
| `lint` | [references/lint.md](references/lint.md) |

确定性检查：

```bash
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}" --check-index
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}" --write-index
```

`<this-skill>` 是本 skill 安装目录。不要手写绝对家目录。

## `guide`

只读了解工作区。进入后读 [references/layout.md](references/layout.md) 的 `guide` 节。

## `init`

没有 `wiki/` 时 **必须先获得确认** 再创建。未确认则停止。确认 `{WIKI_ROOT}` 与研究/知识范围一句话。进入后读 [references/layout.md](references/layout.md)，按其中脚手架创建，再转 `ingest`。

## `ingest`

进入后读 [references/ingest.md](references/ingest.md)。写页时再读 [references/page-types.md](references/page-types.md)。

## `query`

进入后读 [references/query.md](references/query.md)。默认只读；用户要求归档时，先说明将写入 `wiki/queries/`，确认后再写。

## `archive` / `reopen`

进入后读 [references/archive-reopen.md](references/archive-reopen.md)。归档先给计划，确认后原地标记；重开前重新核实当前主张。改完跑 lint。

## `organize`

先给方案，确认前不改。进入后读 [references/organize.md](references/organize.md)；写页时再读 [references/page-types.md](references/page-types.md)。改完跑 lint。

## `lint`

进入后读 [references/lint.md](references/lint.md)。先修 error，warning 说明后处理或有意推迟。
