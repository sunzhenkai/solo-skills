# `resume` 命令

原 SKILL 小节迁移至此。进入本命令后执行。

## `resume`

恢复进行中的探索任务。**任务文档只读**；发现 INDEX 漂移时允许重建 `INDEX.md`，不要改 `TASK.md` / `glossary.md` / `design/`。

1. 未指定名字：用 INDEX 的 Ongoing 表列出请用户选。指定了则用该名字。
2. 任务不在 `ongoing/`：先查 INDEX 的 Archived 表，再扫 `tasks/archive/`。告知已归档路径；**不要自动恢复**，拉回走 `reopen`。找不到则说明，改走 `new`。
3. 读 `TASK.md`、`glossary.md`、`design/`（有则读索引与最新稿）。恢复子任务时先只读父 `TASK.md` 的目标/决策节防方向漂移，再读子任务全套；父文档不被修改。
4. 用短摘要恢复：**目标 / 当前 phase / 进展 / 未决 / 建议下一步**（`explore` / `chat` / `design` / `approve` / `save` / `handoff` / `archive`）。然后等用户。
