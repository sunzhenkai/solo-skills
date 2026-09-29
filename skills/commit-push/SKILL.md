---
id: commit-push
name: commit-push
description: "分析当前 git 变更、起草提交说明、创建 commit 并 push 到远程。在用户要求提交、commit、push、提交并推送时使用；仅查看变更/diff 或需要逐文件评审时不用本 skill（那是 review 的活）。按规模分流：仅 push 跳过 diff、小改动一条并行批次收齐、大改动只抽样。"
---

# 提交并推送

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文。commit message 跟随仓库已有 log 风格（中英均可）。

默认执行 **commit + push**；若用户只要 commit 或只要 push，按其指示。默认沿用当前分支与 tracking remote；意图不清再问（见「何时问用户」）。

## 收集（按规模分流）

先用一条 `git status -sb` 定路：变更文件数、ahead/behind、有无未推送 commit 一次看清。

**仅 push**（工作区干净、HEAD 有未推送 commit）：跳过 diff 收集，只跑 `git log @{u}..HEAD --oneline` 核对将推送的 commits，直接进「提交并推送」的 Push 部分。

**小改动**（≤15 个文件且不含 lockfile/生成物）——一条并行批次收齐，不再单独摸规模：

```bash
git status -sb
git log -3 --oneline
git diff HEAD
```

`git diff HEAD` 一次覆盖已暂存+未暂存，不再分开跑 stat 与两个 diff。untracked 新文件只看路径；核心新文件按需 `Read` 片段即可。

**大改动**（>15 文件，或含 lockfile/生成物/vendor/大 JSON/YAML/资源文件）——**禁止**一上来对整库跑完整 `git diff` 并通读：

1. 批次里把完整 diff 换成 `git diff HEAD --stat`。
2. 按目录与文件类型分组理解意图；只对**核心逻辑文件**抽样 `git diff -- <path>`（每次少量路径）。
3. lockfile、生成物、vendor、大 JSON/YAML、资源文件：**只看路径与是否应纳入提交，不读内容**。
4. 消息依据：**status + stat + 少量代表性 diff + 文件路径模式** 即可，不要求证明读过每一行。不要为了写 commit message 而并行打开几十个文件；单文件 diff 过大时不要拉完整 patch 也不要 `Read` 全文。

## 安全协议

- **不要** 修改 git config
- **不要** 用破坏性命令（`push --force`、hard reset 等），除非用户明确要求
- **不要** 跳过 hooks（`--no-verify` 等），除非用户明确要求
- **不要** force push 到 `main`/`master`；若用户要求则警告
- **避免** `commit --amend`，除非用户明确要求且满足：HEAD 由你在本会话创建、尚未 push、amend 非因 hook 失败
- hook 失败：修问题后 **新建** commit，不要 amend
- 没有变更时不要空提交
- 疑似密钥文件（`.env`、`credentials.json` 等）不要提交；若用户点名要提交则警告

## 暂存

- 用路径级 `git add -- <paths>`，避免盲目 `git add -A` 带入无关或敏感文件。
- 提交前过一遍 untracked 清单，排除 `.env`、密钥、大产物。
- 排除浏览器调试产物：`page-*.png` / `*screenshot*.png`、`trace.zip`、`playwright-report/`；勿提交浏览器调试截图。

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

若无上游或被拒绝，说明原因并停下，不要强推。

## 收尾

链式命令已含确认用 `git status -sb`；简短告知：分支、commit 摘要、是否已 push。

## 何时问用户

- 变更意图不清（多件事混在一起是否拆分）
- 包含可能不该提交的文件
- push 需要选择 remote/分支且无法从 tracking 判断
- 目标是共享远程（生产、预发、共享分支）或默认分支：推送前单独向用户确认，「提交并推送」的授权只覆盖当次点名的目标
