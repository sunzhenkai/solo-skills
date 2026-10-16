# audit-skill.sh 已知误报

`exit 2` 逐条复核时优先对照本表。命中本表也只是「可能误报」的依据：仍要读原文给出判断，由用户针对具体条目豁免后才安装。

| 命中规则 | 典型误报来源 |
|----------|--------------|
| `jailbreak_role` | MIT LICENSE 正文的 `without limitation`。该分支现只放过 `limitation` 后缀，其余 `without … limit` 与 `no restrictions` 仍阻断 |
| `browser_session` | 前端代码里的 `localStorage`、`document.cookie`。文档写「不记录 cookie」应跳过 |
| `credential_paths` | 清单里的 `.env` + `README` 曾因 `README` 命中 `read`；现要求独立单词 `read`/`cat`/`source`。`~/.ssh` 分支现排除 `~/.ssh/config`（非密钥配置）；私钥路径仍由 `/\.ssh/id_` 兜底。个人环境的路径特例不进共享规则集，走被审 skill 的 `.audit-allow` |
| `eval_external` | Markdown 反引号 + 单词 Eval 不是 `eval $(curl …)` |
| `internal_url` | JSON Schema `$id` 的 `https://*.local/schemas/…`、文档里的 `localhost` 开发地址不是内网主机 |
| `binary_in_skill` | 真正的 ELF / Mach-O / PE32 / shared object。带 shebang 的纯文本脚本不再报 |
| `sudo_usage` / `force_push` 等 | 安全规范类 skill 在讲反面例子（脚本已尝试按「禁止/不要/avoid/不记录」跳过，但覆盖不全） |
