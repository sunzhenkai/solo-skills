---
id: way-to-cr
name: way-to-cr
description: 多引擎 Git diff / MR / PR 代码审查（原 solo-code-review）：先思考审查范围与风险重点，再选择内置审查、Claude Code /code-review、Codex /review 或 OCR 执行并按需记忆模型选择，输出 P0~P3 分级报告，支持可选落盘与 MR/PR 评论。在用户要求 code review、审查 MR/PR、评审未提交改动或提交时使用。
license: MIT
---

# way-to-cr

面向个人与小团队的多引擎 **Git diff 级代码审查**（原 `solo-code-review`）：先厘清范围与风险，再由用户选方案与模型，最后按 `P0~P3` 输出精炼报告并按需落盘或发布评论。

架构评审、岗位视角评审、需求/规格符合性评审交给 `role-review`。默认只审查、不改代码；用户明确要求「顺手修」时再改代码。无 diff 的全仓静态扫描直接用 `ocr scan`。

## 调用

```text
/way-to-cr [repo=<仓库名|仓库路径>] [mode=uncommitted|default-branch|commit] [commit=<hash>] [engine=builtin|claude|codex|ocr] [model=<name>] [provider=<name>] [save=yes|no|plan] [change-name=<slug>]
/way-to-cr <GitLab/GitHub MR 或 PR URL> [engine=...] [model=...]
```

可选：业务背景 `-b <一句话>` / `-B <md路径>`；审查深度 `effort=low|medium|high`；更换已记住的模型时传 `model=` 或说「换模型」。机械步骤统一用 [`scripts/reviewctl.py`](scripts/reviewctl.py)（`--root` 指向工作区根目录）。

## 四步流程

### 1. 思考审查内容与范围（范围确认门）

1. **解析目标**：
   - 给了 **MR/PR URL** → 走 `parse-mr` 与 [references/mr-mode.md](references/mr-mode.md)（只 fetch 到 `refs/code-review/*`，保持工作区干净，不 `checkout`/`stash`/`reset`）。
   - 给了 **仓库名或路径** → `reviewctl inspect --repo <name>`。
   - 都没给 → 当前对话已点名仓库则直接用；否则询问。多命中时列出全部 `candidates` 让用户选。
2. **范围确认门**（`inspect` 的 `recommendation`）：

| recommendation | 含义 | 下一步 |
|---|---|---|
| `uncommitted` | 仅工作区脏 | 建议工作区未提交审查；仍须用户确认 |
| `default-branch` | 干净且相对默认分支有提交 | 建议 `--from <comparison_ref> --to HEAD`；仍须用户确认 |
| `ask` | 既有未提交又有分支提交 | 必须让用户二选一，禁止默默合并两种 diff |
| `nothing` | 干净且无新提交 | 停止，问是否改审 MR/PR、单个 commit 或其他 ref |

   点名**单个 commit** 时设 `mode=commit`（范围 `-c <hash>`）。
3. **预览与思考重点**：跑 `reviewctl preview --repo <name> --mode <mode>`（按需加 `--commit` / `--from` / `--to` / `--exclude`），提取 `reviewable_files`、`excluded_files` 与仓库底线文件（`AGENTS.md` / `CLAUDE.md` 等）。先思考改动意图与高风险点（并发、资源释放、权限安全、边界条件、底线遵循），向用户简述审查范围、排除项与重点清单。

### 2. 选择 Review 方案（方案确认门）

跑 `reviewctl probe` 探测本机可用引擎与已保存偏好，向用户展示可选方案并等待选择（范围清晰无歧义且用户未预选 `engine=` 时，可与第 1 步合并为一次确认）：

| engine | 方案 | 特点与适用场景 |
|---|---|---|
| `builtin` | 内置审查（推荐日常首选） | 零依赖、快；对齐 `AGENTS.md` 与 diff，推荐干净会话或只读 subagent 避开盲区 |
| `claude` | Claude Code `/code-review` | 复用 Claude Code 订阅与插件/无头命令，适合复杂变更 |
| `codex` | Codex `/review` | 复用 Codex CLI 原生审查或只读 `codex exec` |
| `ocr` | Open Code Review (`ocr`) | 支持 `ocr review` 与 `ocr delegate`（复用当前订阅额度） |

若用户已明确传入 `engine=`，核对可用后跳过询问。

### 3. 模型选择与记忆复用 + 执行审查

仅 `claude`、`codex`、`ocr`（原生 `review`）需要选定模型；`builtin` 与 `ocr delegate` 直接使用当前会话模型。

**模型记忆复用规则**（配置文件 `~/.config/way-to-cr/prefs.json`，只存引擎与模型名，严禁写入 key/token）：

1. 用户本次显式传了 `model=`（或 `provider=`）→ 采用并执行 `reviewctl prefs set --engine <e> --model <m>` 记住；
2. 用户明确说「换模型」或 `prefs.json` 中该引擎无记录 → 展示 `reviewctl probe --engine <e>` 探测到的可用模型列表（支持直接输入自定义模型 ID）→ 用户选定后 `reviewctl prefs set` 记住；
3. `prefs.json` 已有记录且用户未要求更换 → 自动复用已记住模型，在回复中简短提示当前沿用该模型并直接执行。

**按引擎执行**：

- `builtin` → 按 [references/builtin-review.md](references/builtin-review.md) 执行。
- `claude` / `codex` → 按 [references/external-agents.md](references/external-agents.md) 执行。
- `ocr` → 按 [references/ocr-mode.md](references/ocr-mode.md) 执行；若 `ocr llm test` 失败或用户想复用当前订阅额度，改走 [references/delegate-mode.md](references/delegate-mode.md)。

### 4. 分级出报告、可选落盘与可选发布 MR/PR

1. **统一分级**：将引擎产出整理为统一 JSON（含 `engine`、`llm.{provider,model}`、`summary`、`comments[]`），按 `P0`（阻断/安全/数据损坏）· `P1`（严重缺陷）· `P2`（普通缺陷）· `P3`（低影响仍值得修）分级。`reviewctl` 优先级为：显式 `priority` > `severity` 映射 > 内容启发式；有把握时校准。
2. **对话输出**：仅输出 `reviewctl render` / `write` 返回的 `summary`（按 `P0→P3` 排序，含引擎与模型）及文档路径（若落盘）；无发现时打印 `No findings.`。原始 JSON 与长推理留在产物中，不刷屏对话。
3. **可选落盘**：
   - 用户传 `save=yes` / `save=plan`、上游 flow 要求落盘、或对话确认落盘时：生成 `change-name`（`reviewctl change-name`，`commit` 模式带 `--commit <hash>`），调用：
     ```bash
     python3 <skill-root>/scripts/reviewctl.py --root <workspace-root> write \
       --result-json /tmp/way-to-cr-result.json --meta-json /tmp/way-to-cr-meta.json [--plan-md /tmp/way-to-cr-plan.md]
     ```
     落盘到 `<workspace-root>/docs/reviews/{YYYY-MM-DD}/{change-name}/`（`raw.json`、`review.md`、`summary.md`；提供 `--plan-md` 时附加 `plan.md`）并更新 `docs/reviews/INDEX.md`。
   - 用户选择仅对话查看（`save=no`）时：调用 `reviewctl render --result-json ... --meta-json ... --format summary`，不在工作区写文件。
4. **MR/PR 评论确认门**：仅在 **MR/PR 模式** 下询问用户是否将完整报告发布为 `<MR/PR URL>` 的评论，并说明这是远程写操作。得到用户明确确认并核对目标 URL/IID 后，才调用 `glab mr note` / `gh pr comment` 发布一条评论；仓库模式不询问也不发布。GitLab 自建实例认证仅通过 `GITLAB_TOKEN="$GITLAB_TOKEN" glab ...` 传递，严禁将 token 写入命令行参数、日志或审查产物，严禁编造凭据。
5. **修复提示（可选）**：有 findings 时（优先标出 `P0` / `P1`），在输出总结后提示用户可选进入修复（指定条目、仅修 `P0/P1` 或保持只读结束）；无 findings 时省略。用户明确确认修复范围后再改代码：单点明确缺陷做最小修复并验证，复杂根因排查可衔接 `way-to-fix`。

## 边界与自进化

- 只读边界：默认仅审查不改代码；目标仓不执行 `checkout` / `stash` / `reset`；MR/PR 只用 `refs/code-review/*`。
- 交付前对照 `evals/cases.yaml` 自检；经验沉淀与正文演进走 `skill-upgrader`（单次失败不直接改本文件）。
