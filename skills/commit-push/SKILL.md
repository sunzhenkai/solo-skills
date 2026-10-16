---
id: commit-push
name: commit-push
description: "提交并推送：分析 git 变更、起草提交说明、commit 并 push 到远程。用户要求提交、commit、push、提交并推送时使用。"
---

# 提交并推送

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文。commit message 跟随仓库已有 log 风格（中英均可）。

只看 diff 或逐文件评审交给 `solo-code-review`；本 skill 负责落 commit 与 push。

默认执行 **commit + push**；若用户只要 commit 或只要 push，按其指示。默认沿用当前分支与 tracking remote；意图不清再问（见「何时问用户」）。

## 收集（按规模分流）

先用通用只读脚本定路：

```bash
scripts/commit_push_context.sh
```

默认输出分支/upstream、ahead/behind、进行中的操作、staged/unstaged/untracked 分类、未合并文件；不执行 add/commit/push。按需加参数：`--push` 补未推送 commits，`--stat` 补 `git diff HEAD --stat`，`--conflicts` 补冲突盘点；`--full` 展开被裁剪的冲突侧，`--help` 看用法。

**仅 push**（工作区干净、HEAD 有未推送 commit）：运行 `scripts/commit_push_context.sh --push`，跳过 diff 收集，核对 `git log @{u}..HEAD --oneline` 后将推送 commits，直接进「提交并推送」的 Push 部分。

**小改动**（≤15 个文件且不含 lockfile/生成物）——脚本默认输出后，一条并行批次收齐，不再单独摸规模：

```bash
git log -3 --oneline
git diff HEAD
```

`git diff HEAD` 一次覆盖已暂存+未暂存，不再分开跑 stat 与两个 diff。untracked 新文件只看路径；核心新文件按需 `Read` 片段即可。

**大改动**（>15 文件，或含 lockfile/生成物/vendor/大 JSON/YAML/资源文件）——先运行 `scripts/commit_push_context.sh --stat`，从统计入手、按路径抽样（整库完整 `git diff` 通读会撑爆上下文）：

1. 批次里把完整 diff 换成 `git diff HEAD --stat`。
2. 按目录与文件类型分组理解意图；只对**核心逻辑文件**抽样 `git diff -- <path>`（每次少量路径）。
3. lockfile、生成物、vendor、大 JSON/YAML、资源文件：**只看路径与是否应纳入提交，不读内容**。
4. 消息依据：**status + stat + 少量代表性 diff + 文件路径模式** 即可，不要求证明读过每一行；单文件 diff 过大时只看局部 hunk。

## 处理冲突

检测到 unmerged paths 或 merge/rebase/cherry-pick 进行中时，先读 [references/conflicts.md](references/conflicts.md)：用 `scripts/commit_push_context.sh --conflicts` 盘点，按**追加型** / **语义型** / **危险型**分流解决，按路径 `git add -- <paths>`（整体 `git add -A` 和盲取一侧都会吞掉另一侧）。
做完的标志：`git ls-files -u` 与 `git diff --check` 均无输出、无冲突标记；冲突处理不会自动获得推送授权。

## 安全默认

安全默认：沿用现有 git config 与 hooks；路径级暂存；每次新建 commit；普通 `git push`；只在确有变更时提交；密钥类文件留在提交之外。

以下情况先确认——用户明确要求才做，并先说明风险：

- **改写或丢弃历史**：`push --force`、hard reset 等破坏性命令；目标是 `main`/`master` 时即便用户要求也先警告。
- **`commit --amend`**：仅当用户明确要求且 HEAD 由你在本会话创建、尚未 push、amend 非因 hook 失败。hook 失败时修好问题后 **新建** commit。
- **跳过 hooks**（`--no-verify` 等）。
- **修改 git config**。
- **提交疑似密钥文件**（`.env`、`credentials.json` 等）：用户点名要提交也先警告。

## 暂存

- 用路径级 `git add -- <paths>`（`git add -A` 容易带入无关或敏感文件）。
- 提交前过一遍 untracked 清单，排除 `.env`、密钥、大产物。
- 排除浏览器调试产物：`page-*.png` / `*screenshot*.png`、`trace.zip`、`playwright-report/`。

## 提交并推送

提交说明：1–2 句，说明 **为什么**，不是文件清单；匹配仓库现有 log 风格。HEREDOC 避免引号问题。

**非共享远程且非默认分支**——一条链式命令跑完（add → commit → push → 收尾 status），不等中间结果：

```bash
git add -- <paths> && git commit -m "$(cat <<'EOF'
消息正文。
EOF
)" && git push -u origin HEAD && git status -sb
```

**默认分支或共享远程**（生产、预发、共享分支）——拆成两步：先 `git add + commit`，推送前单独向用户确认，确认后再 `git push -u origin HEAD && git status -sb`。

若无上游或被拒绝，说明原因并停下，等用户决定（强推属于上方「先确认」）。

## 收尾

链式命令已含确认用 `git status -sb`；简短告知：分支、commit 摘要、是否已 push。

## 何时问用户

- 变更意图不清（多件事混在一起是否拆分）
- 包含可能不该提交的文件
- push 需要选择 remote/分支且无法从 tracking 判断
- 目标是共享远程（生产、预发、共享分支）或默认分支：推送前单独向用户确认，「提交并推送」的授权只覆盖当次点名的目标
