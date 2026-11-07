# Lint

确定性检查由 `scripts/lint_wiki.py` 执行。LLM 负责解释、排序和修复，不要只看一遍报告就算完成。

```bash
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}"
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}" --check-index
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}" --write-index
python3 <this-skill>/scripts/lint_wiki.py "{WIKI_ROOT}" --json
```

默认及 `--check-index` 均只读并校验索引一致性；`--write-index` 重建 `wiki/index.md`，不改其它文件。活跃页保留在对应类型表，带 `archived_at` 的页面列入末尾「已归档」表。`--json` 的 `stats` 包含 active / archived / draft / validated / deprecated / review_overdue 数量，供 guide 使用。

## 检查码

| 码 | 级别 | 含义 |
|----|------|------|
| `frontmatter_invalid` | error | frontmatter 含不支持行、重复字段或非法 inline list |
| `missing_frontmatter` | error | 业务页缺 title / type / date / confidence，活跃页缺 sources（user-input / conversation 来源页除外）；experience / ledger 缺 status，活跃 source 缺 origin / captured_at |
| `source_invalid` | error | sources / origin 不存在或越界，来源类型错误，content_hash 非法或与真实 raw 内容不匹配 |
| `dead_link` | error | `[[link]]` 或 `[text](path)` 目标不存在 |
| `ambiguous_link` | error | 未限定标题、slug 或别名命中多页；改用路径限定链接 |
| `index_stale` | error | index 缺失或与当前页面元数据不一致；用 `--write-index` 重建 |
| `confidence_invalid` | error | confidence 不是 high / medium / low |
| `verification_missing` | error | high 缺 last_verified，或 validated 经验缺 last_verified / review_after |
| `date_invalid` | error | date / created / last_verified / review_after / archived_at / captured_at 不是有效的 YYYY-MM-DD |
| `archive_metadata_invalid` | error | 已归档页缺 archive_reason，或 archive_reason / superseded_by 在没有 archived_at 时单独出现 |
| `review_overdue` | warning | 活跃页已到复审日；归档页不产生此项 |
| `description_missing` | warning | 活跃业务页缺少索引摘要 |
| `log_format_invalid` | error | `log.md` 条目前缀不符合 `## [YYYY-MM-DD] action \| description` |
| `log_date_decreasing` | error | 日志日期递减（违反仅追加） |
| `type_dir_mismatch` | warning | `type` 与所在 typed 目录不一致 |
| `misplaced_wiki_page` | warning | 业务页不在 typed 子目录 |
| `duplicate_page` | warning | 同目录下文件名归一化后重复 |
| `entity_concept_coupling` | warning | 概念标题把实体名绑到抽象概念上 |
| `archived_reference` | warning | 活跃业务页链接归档页；需明确历史语义或改指现行页面 |
| `orphan_page` | warning | 活跃业务页无活跃入链；系统页、sources 与归档页不计入，归档页出链不使活跃页摆脱孤立 |

## 修复顺序

先 error，后 warning。一页多问题一次改完。改前先读全文，避免为消警告丢掉信息。

**Frontmatter**：按 page-types 的受限格式修正。活跃页补充真实来源；归档页保留历史。source 的 hash 来自实际文件，不编造。

**链接与来源**：先确认目标是否改名或存在同名。歧义链接改成路径限定形式；来源指向真实来源页或 raw 相对路径，不随便建空页。

**索引**：页面增删、归档、重开或索引字段变化后运行 `--write-index`；query 只读时使用文件系统回退。

**日志**：只改格式与日期顺序问题；不删条目、不改历史含义。

**归档引用**：历史链接保留并说明；当前依据改指替代页或补充现行来源。脚本不能判断正文语境。

**孤立页**：活跃页从相关页面补入链；归档页无需为消除孤立警告补链。

**错位 / 重复 / 耦合**：保留独有事实与历史，按既有 organize 契约处理。

## 脚本做不到的（需 LLM）

- 页面间事实矛盾与过时主张
- 归档引用的历史语境
- 正文提到但尚未建页的概念
- 缺失的交叉引用（入链检查只覆盖已有链接）

`organize` 与 `lint` 可建议这些项，但不要假装脚本已经查过。

## 完成标准

- [ ] lint 报告 0 error，索引一致
- [ ] 来源、死链与歧义链接已解析
- [ ] 业务页 frontmatter 合法，归档元数据成组且完整
- [ ] `wiki/log.md` 格式合法且日期非递减
- [ ] warning 已修或有意推迟并说明
- [ ] 关键修复页已回读
