---
id: solo-code-review
name: solo-code-review
description: 使用 OCR 兼容的代码审查 CLI，审查指定 Git 仓库的未提交改动、单个 commit、相对默认分支的 diff，或 GitLab/GitHub Merge Request / Pull Request；完整结果写入 review workspace 的 docs/reviews/{日期}/{change-name}，对话只打印按 P0~Pn 排序的总结。在用户要求 code review、审查 MR/PR、评审未提交改动或某个提交时使用。
license: MIT
---

# solo-code-review

用 OCR 兼容的 CLI 做 **Git diff 级代码审查**。机械步骤走 `scripts/reviewctl.py`；审查引擎用 `ocr`：LLM 已配置时跑 `ocr review`；未配置时走 delegate 模式（见「前置」），由 OCR 做文件筛选与规则解析、当前 agent 执行审查。

不替代：架构评审、岗位视角评审、需求/规格符合性评审。默认只审查、不改代码。无 diff 的全仓静态扫描直接用 `ocr scan`，不经本 skill。

## 调用

```text
/solo-code-review repo=<仓库名|仓库路径> [mode=uncommitted|default-branch|commit] [commit=<hash>] [provider=<name>] [model=<name>] [change-name=<slug>]
/solo-code-review <GitLab/GitHub MR 或 PR URL>
```

可选：业务背景 → `-b`（一句话）/ `-B <md路径>`（成篇文档）；审查深度 `effort=low|medium|high`；LLM 后端 `provider=<name>` + `model=<name>`（单次覆盖，不给则用现有 `ocr config`；内置清单 `ocr llm providers`）。

## MUST 先读取并执行

1. 本文件全文。
2. 机械命令用 [`scripts/reviewctl.py`](scripts/reviewctl.py)（子命令 `inspect` / `parse-mr` / `change-name` / `write`），`--root` 指向审查 workspace 根目录，用法见下文各步。

## 前置

```bash
which ocr && ocr --version || echo "NOT INSTALLED"
ocr llm test
```

未安装：按 OCR CLI 的上游文档安装（先征得用户同意）。运行中 `--format` 报 `unknown flag` 说明 CLI 低于 v1.9.0，提示升级：`npm i -g @alibaba-group/open-code-review`。

`ocr llm test` 只验证**默认配置**（无 `--provider/--model` 参数）。用户指定 provider/model 时：先用 `ocr llm providers` 核对名称；凭据须已在 `ocr config` 或环境变量中配好（单次覆盖不传凭据），跑 `ocr review` 报错即停下请用户配置，禁止编造 API key。

`ocr llm test` 失败时停下，让用户在两条路里选一条；禁止编造 API key：

1. 配置 LLM（环境变量或 `ocr config`）后重跑。
2. delegate 模式：读取并按 [references/delegate-mode.md](references/delegate-mode.md) 执行，审查由当前 agent 的 LLM 完成，产物与确认门同主流程。

GitLab 自建实例认证：优先环境变量 `GITLAB_TOKEN`（需 `api` scope），调 `glab` 映射为 `GITLAB_TOKEN="$GITLAB_TOKEN" glab ...`；token 不写入命令行参数、日志或审查产物；未设置且目标需要认证时停止并请用户配置，禁止编造或输出 token。

## 流程

### 1. 解析目标

- 用户给了 **MR/PR URL** → 走「MR 模式」，忽略本地脏工作区。
- 用户给了 **仓库名或路径** → `reviewctl inspect`。
- 都没给：若当前对话已点名仓库则用之；否则询问。多命中时列出 `candidates` 让用户选。

### 2. 确定审查范围（确认门）

**仓库模式**（`inspect` 的 `recommendation`）：

| recommendation | 含义 | 下一步 |
|---|---|---|
| `uncommitted` | 仅工作区脏 | 建议 workspace 审查；**仍须用户确认** |
| `default-branch` | 干净且相对默认分支有提交 | 建议 `--from <comparison_ref> --to HEAD`；**仍须用户确认** |
| `ask` | 既有未提交又有分支提交 | **必须**让用户选其一，禁止默默合并两种 diff |
| `nothing` | 干净且无新提交 | 停止，问是否改用 MR 链接、单个 commit 或其它 ref |

用户点名**单个 commit** → mode=commit，范围 `-c <hash>`（对其父提交），确认与预览同下。用户已显式给 `mode=` 时，不再改推荐，仍要先 `ocr review --preview` 展示文件列表再跑 LLM。

**MR/PR 模式**：按 [references/mr-mode.md](references/mr-mode.md) 执行（parse-mr → 定位本地仓 → glab/gh 取分支 → **只 fetch 到 `refs/code-review/mr-<iid>` / `pr-<iid>`，不 checkout、不 stash** → `--preview` 确认后跑 LLM）。

### 3. 跑 ocr

始终：`ocr review --audience agent --format json --repo <git_root_abs> -o /tmp/ocr.json 2>/tmp/ocr.err`，范围按下表追加；有背景加 `-b`/`-B`；用户指定 LLM 后端加 `--provider <name> --model <name>`（单次覆盖，不给用现有配置）。可选：`--effort low|medium|high`、`--exclude '**/generated/*,**/testdata/*'`、`--max-tokens-budget <n>`（大仓止损）；中断后 `--resume <session-id>` 续跑（`ocr session list` 可查）。

| mode | 追加范围 flag |
|---|---|
| `uncommitted` | （无，默认工作区） |
| `commit` | `-c <hash>` |
| `default-branch` / MR / PR | `--from <from> --to <to>` |

先看 exit code 与 `/tmp/ocr.err`。JSON `status=skipped` 视为无审查对象，不是失败。

### 4. 分级并落盘

读取 ocr JSON 的 `comments[]`，为每条指定 `priority`：`P0`（发布阻断 / 安全 / 数据损坏）· `P1`（应尽快修的缺陷）· `P2`（普通缺陷）· `P3`（低影响仍值得修）。`reviewctl` 自动分级次序：显式 `priority` > `severity` 映射（critical/high/medium/low → P0~P3）> 内容启发式；**有把握时覆盖**。把带 `priority` 的 comments 写回临时 JSON。

`change-name`：用户指定优先；否则 `reviewctl change-name`（mode=commit 时带 `--commit <hash>`）。日期使用运行当天的 `YYYY-MM-DD`。

```bash
python3 <skill-root>/scripts/reviewctl.py --root <workspace-root> write \
  --ocr-json /tmp/ocr.classified.json --meta-json /tmp/meta.json
```

`meta.json` 至少含：`repo`、`mode`、`date`、`change_name`、`branch`、`from`、`to`、`default_branch`；mode=commit 加 `commit`（短 hash）；MR/PR 再加 `mr_url`、`mr_iid`、`title`。LLM 后端无需手填：`reviewctl write` 从 ocr JSON 的 `llm.{provider,model}` 读出写进 `review.md`（以 OCR 实跑值为准）。

产物目录：`<workspace-root>/docs/reviews/{YYYY-MM-DD}/{change-name}/`

| 文件 | 内容 |
|------|------|
| `ocr-raw.json` | ocr 完整 JSON |
| `review.md` | 完整审查（含现有代码 / 建议 / 推理） |
| `summary.md` | 总结版（同对话打印） |

并更新 `docs/reviews/INDEX.md`。

### 5. MR/PR 评论确认门

仅在 **MR/PR 模式** 且 `review.md` 已成功落盘后，询问用户：

> 完整 review 报告已保存到 `<review.md 路径>`。是否将该完整报告作为评论发布到 `<MR/PR URL>`？这会对远程平台产生写操作，请确认目标和内容。

在用户明确确认前，禁止调用 `glab mr note`、`gh pr comment` 或任何等效的远程写接口；确认时再次核对目标 URL/IID 与待发布文件。用户拒绝或未确认 → 只保留本地报告。确认后以 `review.md` 完整内容发布一条评论并报告成败。仓库模式不询问，也不发布评论。

### 6. 对用户只打印总结

对话输出 **仅** `write` 返回的 `summary`（已按 P0→Pn 排序），再给完整文档路径；`thinking`、大段代码、原始 JSON 不进对话。无 findings 时打印 `No findings.` + 文档链接。需要浏览器回放或分享时用 `ocr session export <session-id>` 生成离线 HTML（含源码摘录，按仓库同等保密）。

## 边界

- 默认不改业务代码、不 commit、不 push；MR/PR 远程评论以第 5 节确认门为准。用户明确要求「顺手修」才可改代码。
- 不 `checkout` / `stash` / `reset` 目标仓；MR/PR 只用 fetch 的 `refs/code-review/*`。
- 完整结果只写 `--root` 指定 workspace 的 `docs/reviews/`，不写目标仓的代码目录。
- 架构评审、岗位视角评审、需求/规格符合性评审分别使用适合的专门流程。

## 自进化

执行前可查 `examples/` 复用成功案例，交付前对照 `evals/cases.yaml` 验证；各目录用法见其 README，经验沉淀与正文演进走 `skill-upgrader`（单次失败不直接改本文件）。
