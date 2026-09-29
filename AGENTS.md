# AGENTS.md

本文件为 AI agent 提供本仓库的快速上下文与工作约定。

## 这是什么

sunzhenkai 的第一方 Agent Skills 集合（公开仓，MIT）：任务流编排、交付闭环、角色评审、跨 agent 委派、代码/仓库/知识工具链。**无业务代码、无构建**——git 真相只有 `skills/<id>/`。skill 清单与用途见 `README.md`。

- 根目录 `.claude/skills -> ../skills` 是整目录单软链，仅为本仓开发时在 Claude Code 里即时生效，不是安装路径。
- 安装方式见 README「安装」一节（npx skills / dotf 编目 / Makefile）；`skills-lock.json`、`.agents/` 已 gitignore。

## 常用命令

无构建、无 lint 配置；自动化门禁只有 pytest 契约测试。

```bash
python3 -m pytest skills -q               # 全部测试（秒级）
python3 -m pytest skills/<id>/tests -q    # 单个 skill 的测试

make check-deps     # 检查外部依赖 skill 是否就绪（缺项非零退出）
make install-deps   # 安装外部依赖（openspec-* 四件套 + grilling 系列），结尾跑 check-deps
make install-acpx   # acpx 缺失提示（二进制，需按上游方式手动装）
```

`SKILLS_DIR=` 可覆盖安装目标（默认 `~/.agents/skills`）。已用 `dotf agents -c` 的环境不需要本 Makefile。

## 结构约定

每个 skill 自包含，目录相对各自根：

- `SKILL.md`：正文，YAML frontmatter（`id` / `name` / `description`）。description 决定触发时机，要写清「何时使用 / 何时不用」。
- `references/`：按需加载的细则。`scripts/`：**只依赖 Python 3 标准库**，不引第三方包。
- `agents/`：部分 skill 携带的第三方 agent 配置（如 `openai.yaml`），可选。
- `tests/`：stdlib unittest 写的**文本契约测试**——校验 SKILL.md 与 references 里的阶段门禁、落点、禁令等文本约束，不模拟执行。改正文后必须过测试。
- `evals/`：声明式案例（`cases.yaml`），无自动 runner，供人工 / agent 评审。
- `examples/` `experience/` `patches/` `evolutions/`：示例、经验、变更审计。

## 改 skill 正文的流程

- 结构缺失（无 `examples/` / `evals/` / `experience/`）先走 **skill-upgrader** 一次性升级结构。
- 基于真实执行经验改正文走 **skill-evolver**：仅显式触发，**禁止自动进化**（一次失败 / 一次用户纠正都不足以改 skill）；先展示 Evolution Proposal，用户确认后才写 `evolutions/<date-slug>/`（proposal.yaml + decision.md + eval.md + 候选稿）。
- 变更留审计痕迹：`patches/`（proposal + change.patch + result）或 `evolutions/`，不要直接编辑正文绕过。

## 外部依赖（不在本仓）

skill 之间的互引已在仓内解决；仍依赖下列仓外内容（详见 README「外部依赖」）：

| 依赖 | 来源 | 被谁依赖 |
| --- | --- | --- |
| `openspec-explore` / `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` | `@fission-ai/openspec` CLI 生成 | taskflow、task-explore、task-wizard、agent-roster-flow |
| `grilling` | `mattpocock/skills` | task-explore（explore 阶段唯一委托） |
| `grill-with-docs` / `domain-modeling` | `mattpocock/skills` | task-wizard、agent-roster-flow（grill-with-docs 含两跳到 `grilling` + `domain-modeling`） |
| `acpx`（二进制，非 skill） | https://acpx.sh | agent-roster 的委派执行 |

- `task-explore` 的 explore 阶段**禁止**委托 `grill-with-docs` / `domain-modeling`（它们会写仓库根 `CONTEXT.md` / `docs/adr/`，与任务目录落点冲突）。
- 安装仓外 skill 前走 skills-store 的安全审计流程（先临时拉取 → audit-skill.sh → 再安装）。

## 公开仓纪律

- **只放机制，不放数据**：名册、案例、路由规则、运行痕迹存使用者私有位置。写任何文件前自查：有没有主机名、内网地址、项目名、真实任务描述？有就不属于这里。
- **运行时只读**：skill 装到各 agent 目录是字节复制而非软链，运行时往 skill 目录写东西只写进镜像、下次同步被覆盖——运行产物一律落仓库之外，`experience/patterns/` 只在源仓改。

## 其他

- `docs/agent-roster/`：agent-roster 的仓级文档（ADR、CONTEXT、README），保留自其独立仓的完整 git 历史；细则见 `docs/agent-roster/AGENTS.md`。
- `lark-cli` 的官方 `lark-*` skill 嵌在 lark-cli 二进制里（`lark-cli skills read` 按需读取），不装进 `~/.agents/skills`。
- 语言：面向使用者的文档用简体中文；命令名、路径、代码、状态值与既成术语（ACP、Endpoint、OpenSpec 等）保持原文。
