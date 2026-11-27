# 外部 Agent 引擎细则（claude / codex）

本文件说明如何通过本地已安装的 `claude`（Claude Code CLI）或 `codex`（OpenAI Codex CLI）执行非交互式只读代码审查，并将结果统一归一化后回到主流程第 4 步。

## 共用前提

1. **只读与不动工作区**：外部引擎只允许读仓库和执行只读 `git diff` / `git show`，严禁修改业务文件、执行 `git checkout` / `stash` / `reset` 或自动发布远程评论。
2. **模型记忆**：模型确定后执行 `reviewctl prefs set --engine <claude|codex> --model <model>` 保存；下次自动复用，直到用户显式要求「换模型」或传新 `model=`。
3. **未安装或报错处理**：`reviewctl probe` 显示未安装时，说明缺失原因并引导安装或让用户切换 `builtin`；鉴权/额度失败时如实报错并停下，禁止编造 API key 或静默切换引擎。

---

## 一、Claude Code（`engine=claude`）

### 1. 模型候选

- 内置常用别名：`sonnet`（均衡首选）、`opus`（复杂逻辑与深层推理）、`haiku`（轻量快速）。
- `reviewctl probe --engine claude` 还会合并 `~/.claude/settings.json` 中的默认 `model` 与已保存模型；用户也可输入任意自定义模型名。

### 2. 调用方式

在目标仓库 `<git_root_abs>` 下使用非交互参数 `-p`（`--print`）和 `--model <model>`：

- **路径 A：插件模式**（`probe` 显示 `has_code_review_plugin=true` 且审查对象为当前分支/PR 常规场景）：

```bash
claude --model <model> -p "/code-review 仅做只读代码审查，不修改任何文件、不直接发布远程评论。审查范围：<range_desc>。" \
  --allowedTools "Read,Grep,Glob,Bash"
```

- **路径 B：通用无头结构化模式**（未装 `code-review` 插件，或审查特定 `commit` / `uncommitted` / MR `refs/code-review/*`）：

```bash
claude --model <model> -p "<审查 prompt>" \
  --output-format json \
  --allowedTools "Read,Grep,Glob,Bash"
```

`<审查 prompt>` 须明确包含：
1. 精确只读范围命令（`git --no-pager diff <merge_base>..<to>` / `git show <commit>` / `git diff HEAD` + untracked）；
2. 若存在 `AGENTS.md` / `CLAUDE.md` 等底线文件，要求先读取并优先校验；
3. 要求仅做只读审查，输出按 `P0~P3` 分级的 JSON findings（含 `path`、`start_line`、`end_line`、`priority`、`content`、`existing_code`、`suggestion_code`）。

---

## 二、Codex CLI（`engine=codex`）

### 1. 模型候选

- `reviewctl probe --engine codex` 读取 `~/.codex/config.toml`（`model` 与 `[profiles.*]`）及 `codex debug models`（若支持），无结果时给出常见建议值；支持用户输入任意模型 ID。

### 2. 调用方式（严守 fetch-only 不变式）

先区分场景选择子命令：

- **路径 A：本地仓标准范围**（`uncommitted`、`default-branch`、`commit`）：优先使用原生 `codex review`（可通过 `codex review --help` 核对当前版本是否支持 `-c model="<model>"` 或 `-m <model>`）：

```bash
# uncommitted
codex review --uncommitted -c model="<model>"

# default-branch（对比默认分支）
codex review --base <comparison_ref> -c model="<model>"

# commit（单提交）
codex review --commit <hash> -c model="<model>"
```

- **路径 B：MR/PR 模式或任意 `from..to`**（目标不是当前 `HEAD`，例如 `origin/<target>..refs/code-review/mr-<iid>`）：
  禁止为了用 `codex review --base` 而 `checkout` 分支。改用只读沙箱执行 `codex exec`：

```bash
codex exec --sandbox read-only -C <git_root_abs> -m "<model>" \
  "请仅做只读代码审查（不改文件）。先阅读仓库底线文件（如 AGENTS.md），再执行 git --no-pager diff --no-ext-diff --no-textconv --no-color <merge_base>..<to> 审查全部变更，按 P0/P1/P2/P3 输出 JSON findings（path/start_line/end_line/priority/content）。"
```

---

## 三、输出归一化与回到主流程

1. 将 `claude` / `codex` 的输出整理为统一 result JSON 写入 `/tmp/way-to-cr-result.json`：
   - `engine`：`"claude"` 或 `"codex"`
   - `status`：`"complete"`
   - `session_id`：`"<engine>-<YYYYMMDD-HHMMSS>"`
   - `llm`：`{"provider": "<engine>", "model": "<model>"}`
   - `comments[]`：每条含 `path`、`content`、`start_line`、`end_line`、`priority`（或 `severity`）、可选 `existing_code` / `suggestion_code`
   - `warnings[]`：工具跳过或降级说明
2. 回到 `SKILL.md` 第 4 步完成分级、对话总结、可选落盘与 MR/PR 评论确认门。
