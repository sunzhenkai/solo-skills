# 页面类型

业务页路径由 `type` 决定。文件名用标题的短 slug（可含中文），扩展名 `.md`。

| type | 目录 | 用途 | 必需章节 |
|------|------|------|----------|
| entity | `wiki/entities/` | 可唯一指认的对象：人、组织、产品、项目 | 概述、关键事实、相关概念、来源 |
| concept | `wiki/concepts/` | 可复用的术语、方法、框架、机制、理论 | 定义、核心要点、相关实体、来源 |
| source | `wiki/sources/` | 一份 raw 源的摘要，不是原件 | 摘要、关键观点、相关实体/概念 |
| synthesis | `wiki/synthesis/` | 跨源分析 | 问题/目的、分析、引用、后续 |
| experience | `wiki/experiences/` | 可复用的经验结论及其证据、适用边界 | 适用场景、触发信号、经验结论、预防与处理、验证方式、证据、边界与失效条件、来源 |
| ledger | `wiki/ledgers/` | 一个业务对象的当前状态与历史变化 | 当前状态、历史、来源 |
| comparison | `wiki/comparisons/` | 对比 | 对比维度、异同、结论 |
| query | `wiki/queries/` | 值得留下的问答 | 问题、回答、引用 |

关系（某实体采用某概念）用正文和 `[[wikilink]]` 表达，不要做成第三种页面类型，也不要把双方名字拼进概念标题。

## Frontmatter

业务页：

```yaml
---
title: 页面标题
type: entity
date: YYYY-MM-DD
confidence: medium
tags: []
aliases: []
sources: []
related: []
---
```

- 更新时不要轻易改 `type`、`title`、`created`（若已有）。
- `tags` / `aliases` / `sources` / `related` 做并集去重，不覆盖删除旧值。
- `date` 用本次写入日；`created` 只在首次创建时加。
- `description` 是一句话摘要，供索引与候选筛选使用；活跃页应填写，缺失会产生 warning。`aliases` 记录常用别名、缩写和中英变体，可用于链接解析；同名或别名冲突时必须使用路径限定链接。
- 活跃业务页必须有非空 `sources`。每项指向 `wiki/sources/` 页标题、`[[来源页面]]` 或 `raw/sources/` 内的相对文件名；来源必须存在。`origin` 为 `user-input` / `conversation` 的 source 页本身可为空。归档页保留既有来源，不强制补写历史字段。
- 活跃 `source` 页还必须有 `origin` 与 `captured_at: YYYY-MM-DD`；`origin` 使用 raw 相对路径、`user-input` 或 `conversation`，`content_hash` 可选，存在时为源内容的 SHA-256 十六进制摘要。
- `tags` / `aliases` / `sources` / `related` 使用 inline list（如 `[alpha, beta]`）。lint 支持标量、空值和 inline list，不支持的 frontmatter 行会报错，不静默忽略。
- 所有业务页必须有 `confidence: high | medium | low`，只表示证据强度，不表示重要性或真实概率。
- `last_verified: YYYY-MM-DD` 是主张与来源最后核实的日期，不是编辑日期；`high` 必须有此字段。
- `review_after: YYYY-MM-DD` 是下一次复审期限，易变知识必须填写；到期只表示需要复审，不自动降低证据强度或判定内容错误。
- `experience` 必须有 `status: draft | validated | deprecated`；`validated` 页必须同时记录 `last_verified` 和 `review_after`。
- `ledger` 必须有 `status`，取值沿用该业务的既有词表；`date` 表示当前状态最后更新时间。
- `archived_at: YYYY-MM-DD` 存在即表示整页已归档，必须同时填写 `archive_reason`；`superseded_by: "[[替代页面]]"` 可选。三个字段只描述页面生命周期，与 experience 的验证状态、ledger 的业务状态正交。
- 归档页保留原路径、类型、来源与正文历史；重开时移除上述归档字段，并在正文保留归档与重开记录。

### 置信度定级

| confidence | 证据标准 | 复用方式 |
|------------|----------|----------|
| `high` | 当前一手来源已被直接核实，或有可复查的复现/验证证据；多个来源须能独立佐证 | 可按适用范围作为现行结论，并附核实日期 |
| `medium` | 单一可靠来源尚未独立复核，或有依据但未直接验证的推断 | 可作为参考，说明证据缺口与适用边界 |
| `low` | 未验证说法、转述、开放假设或尚未裁决的冲突 | 只作线索，先验证再执行 |

页面 `confidence` 是未单独标注主张的默认值。同页主张证据强度不同或适用范围不同时，在主张后标 `（置信度：低；核实：YYYY-MM-DD；来源：[[来源页面]]）`；回答以具体主张的标注为准。用户决策可以高置信度地证明「做过该决策」，不能由此推高决策结果的置信度。

纠正事实时保留旧主张，标明「已更正」、日期、新来源与替代结论。冲突主张并列保存并保持 `low`，有裁决证据后再更新等级；经验整页失效用 `deprecated`，其他页面用主张级状态保留历史。

系统页可不设业务 `type`。模板页只存在于 `wiki/templates/`。

## 实体 vs 概念

写页前问三句：

1. 这是可指认的具体对象，还是可复用的抽象？
2. 标题是否嵌了已有实体名？
3. 若两者同时出现，是否应拆成两页再用 wikilink 连起来？

**默认**：概念标题保持中性，不把实体名嵌进去。

| 不要 | 要 |
|------|------|
| 概念页 `青禾实验室渐进披露` | 实体 `青禾实验室` + 概念 `渐进披露`，正文互链 |
| 把某组织的工具栈写成概念标题 | 中性概念 + 实体页记录其采用情况 |
| 关系页 `Foo 采用 Bar` | 在 Foo / Bar 正文中写关系 |

**例外**：来源把整句当作专有名词。保留组合标题，并在正文写明命名依据与出处。

虚构示例：实体 `青禾实验室` 是具体组织；概念 `渐进披露` 是可被多个实体引用的方法。

## 项目 Atlas 入口

当前项目实体已有 `project-atlas` 时，可在正文增加「项目 Atlas」一节，用相对 Markdown 链接指向 Atlas `index.md`。只链接入口，不把 Atlas 的架构、流程或规则复制到实体页；链接仅作导航，不替代 `sources`。

## 模板（init 时写入 `wiki/templates/`）

创建业务页时按对应模板补齐章节，不要把「（待填写）」留在成品里。

### entity

```markdown
---
title: 示例实体
type: entity
date: YYYY-MM-DD
confidence: medium
tags: []
---

# 概述

## 关键事实

-

## 相关概念

- [[相关概念]]

## 来源

- [[来源页面]]
```

### concept

```markdown
---
title: 示例概念
type: concept
date: YYYY-MM-DD
confidence: medium
tags: []
---

# 定义

## 核心要点

-

## 相关实体

- [[相关实体]]

## 来源

- [[来源页面]]
```

### source

```markdown
---
title: 示例来源
type: source
date: YYYY-MM-DD
confidence: medium
description: 一句话来源摘要
origin: raw/sources/example.txt
captured_at: YYYY-MM-DD
sources: [example.txt]
tags: []
---

# 摘要

## 关键观点

-

## 相关实体/概念

- [[相关页面]]
```

### experience

```markdown
---
title: 示例经验
type: experience
date: YYYY-MM-DD
confidence: low
status: draft
tags: []
sources: []
---

# 适用场景

## 触发信号

## 经验结论

## 预防与处理

## 验证方式

## 证据

## 边界与失效条件

## 来源

- [[来源页面]]
```

### ledger

```markdown
---
title: 示例业务对象
type: ledger
date: YYYY-MM-DD
confidence: medium
status: active
tags: []
sources: []
---

# 当前状态

## 历史

### [YYYY-MM-DD] 初始记录

- 状态：active
- 依据：[[来源页面]]

## 来源

- [[来源页面]]
```

### synthesis / comparison / query

- synthesis：问题/目的、分析、引用、后续
- comparison：对比维度、异同、结论
- query：问题、回答、引用

## 链接

- 内部用 `[[标题]]` 或 `[[entities/slug|标题]]`。
- 写 A 提到 B 时，尽量在 B 补反向链接（至少从 overview / 相关实体或概念链入）。
- 不要用纯文本名字代替已有 wiki 页。
