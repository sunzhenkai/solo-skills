# delegate 模式（OCR 未配置 LLM 时）

OCR 的委托模式：`ocr` 只做确定性工程（文件筛选、打包、规则解析），审查由当前 agent 用自己的 LLM 执行。触发条件：`ocr llm test` 失败且用户选择 delegate。产物落盘、分级、总结打印、MR/PR 评论确认门与主流程完全一致，只有「跑 ocr」这一步被替换。

delegate 模式下 `--provider/--model` 不适用（OCR 侧不调 LLM，审查用当前 agent 的模型）；`review.md` 的 LLM 行留空或标注 `delegate`。

## 步骤

### D1. 预览审查范围

```bash
ocr delegate preview --format json --repo <git_root_abs> [--from <ref> --to <ref>] [-c <hash>] [--exclude <patterns>]
```

输出含 `mode`（workspace / range / commit）、ref 元数据（`from` / `to` / `commit` / `merge_base`）、`reviewable_files[]`（path、status、insertions、deletions）与 `excluded_files[]`（含排除原因）。把 `reviewable_files` 展示给用户确认（等同主流程的 `--preview` 确认门）。

### D2. 取规则

```bash
ocr delegate rule --format json --repo <git_root_abs> <path1> <path2> ...
```

输出按规则内容分组（`groups[]`）：共享同一规则的文件归为一组。大变更可按批取规则。

### D3. 逐文件取 diff 并审查

对 `reviewable_files` 建 checklist，以 `(path, status)` 为身份（workspace 模式下同一路径可能出现两次：staged 删除后 untracked 重建）。Git 命令一律 `--no-pager --no-ext-diff --no-textconv --no-color`：

```bash
# range 模式（用 preview 输出的 merge_base）
git --no-pager diff --no-ext-diff --no-textconv --no-color <merge_base>..<to> -- "<path>"
# commit 模式
git --no-pager show --no-ext-diff --no-textconv --no-color <commit> -- "<path>"
# workspace 模式（tracked）
git --no-pager diff --no-ext-diff --no-textconv --no-color HEAD -- "<path>"
# workspace 模式的 untracked 新文件：整文件都是新代码，直接读
cat "<path>"
```

上下文按需补：`git log --oneline -- <path>`、`git blame -- <path>`、`git show <ref>:<path>`。大 diff 加 `--output=<绝对路径>` 写到仓库外，读完即删。

每个文件按其规则组的 checklist 审查，可用 Read/Grep 等工具取更多上下文；标记 `reviewed`，或 `skipped` 加具体原因。发现一个高严重度问题后继续审完，不提前停。

### D4. 组装 comments JSON

每条 comment 字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `path` | string | 是 | 仓库相对路径 |
| `content` | string | 是 | 问题描述 |
| `start_line` / `end_line` | integer | 否 | 新文件中的行号；都为 0 表示未定位 |
| `category` | enum | 否 | bug / security / performance / maintainability / test / style / documentation / other |
| `severity` | enum | 否 | critical / high / medium / low |

组装成与 `ocr review --format json` 同构的对象写入 `/tmp/ocr.json`：

```json
{
  "status": "complete",
  "session_id": "delegate-<YYYYMMDD-HHMMSS>",
  "message": "delegate review: <n> finding(s) across <m> file(s)",
  "summary": {"files_reviewed": <m>, "comments": <n>},
  "comments": [...]
}
```

`summary.files_reviewed` 用实际 reviewed 数；skipped 文件在 `warnings[]` 里逐条写 `path: reason`。severity 会被 `reviewctl` 自动映射为 P0~P3（critical→P0、high→P1、medium→P2、low→P3），仍可按主流程规则覆盖。

### D5. 回到主流程

从主流程「4. 分级并落盘」继续：`reviewctl write` 落 `docs/reviews/`、MR/PR 评论确认门、对话只打印 summary。边界不变：默认不改代码，不 checkout/stash/reset 目标仓。

## 覆盖与止损

- 每个 previewed 文件必须有归宿：reviewed 或 skipped（带原因），覆盖情况写进总结的 message。
- 疑似误报直接丢弃，不写进 comments。
- `--format json` 报 `unknown flag`（CLI < v1.9.0）：改用 text 输出取文件清单与规则，保留 mode/ref/规则信息继续；其余错误报告后停止，不换路重试。
