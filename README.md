# solo-skills

sunzhenkai 的第一方 Agent Skills 集合：任务流编排、交付闭环、角色评审、跨 agent 委派、代码/仓库/知识工具链（从 `sunzhenkai/dotfiles` 与 `sunzhenkai/agent-roster` 迁入，独立维护）。

## 包含的 Skills

### 任务流与交付编排

| Skill | 用途 |
| --- | --- |
| `task-wizard` | 生成步骤级任务方案（完成判据 + 动作/要点/验证 + 决策收敛；不产质量画像） |
| `task-goal` | goal 模式下唯一的确认与审阅协议（接方案 → 派审 → 收敛 → 三档开工）；复杂档产质量画像与显式降级 |
| `task-explore` | 长周期/目标不清任务的探索台账（tasks/INDEX.md 推进） |
| `taskflow` | 一个 driver change 编排一批子 change 的任务生命周期 |
| `task-delivery` | 把复杂交付目标编排成自动闭环（探索→实现→证据→评审→复验） |
| `role-based-reviewer` | 可组合的角色化只读评审（engineer/algo/data/sre/ops/biz/product/design/qa） |

### 跨 agent 委派

| Skill | 用途 |
| --- | --- |
| `agent-roster` | 名册化委派：Endpoint 探测、选人、契约执行、Handoff 回收 |
| `agent-roster-flow` | 按 Stage 编排跨 agent 任务，逐段选 Endpoint 与模型委派执行 |

### 代码与仓库工具

| Skill | 用途 |
| --- | --- |
| `commit-push` | 分析变更、起草提交说明、commit 并 push |
| `code-explore` | 仓库代码理解工作流（问答/调用链/影响面/知识沉淀） |
| `solo-code-review` | 未提交改动 / MR / PR 的结构化审查 |
| `repo-manager` | 仓库生命周期管理 |
| `project-init` | 按约定脚手架创建或对齐项目 |
| `project-spec-mirror` | 项目 spec 镜像同步 |
| `service-manager` | 项目服务启停 / 状态 / 日志台账 |
| `lark-cli` | 飞书 / Lark CLI 路由 |

### 知识与内容

| Skill | 用途 |
| --- | --- |
| `llm-wiki` | 本地 Markdown 知识 wiki 维护 |
| `pretty-view-html` | 把已有内容做成浏览器阅读 HTML |
| `role-chat` | 多视角角色对话陪练 |

### Skill 工具链（自进化）

| Skill | 用途 |
| --- | --- |
| `skills-store` | skill 审计与安装门禁 |
| `skill-evolver` | 从多次真实执行进化已有 skill |
| `skill-upgrader` | SKILL.md 一次性升级为自进化结构 |
| `trouble-grill` | 问题排查拷问 |

## 安装

### 通用（npx skills）

skill 源在仓库的 `skills/<id>/`；CLI 的发现优先级前缀含 `skills/`，整仓安装即可：

```bash
npx skills add sunzhenkai/solo-skills                 # 全部
npx skills add sunzhenkai/solo-skills -s taskflow     # 只装一个
```

### dotfiles 编目（第三方）

本仓库以 third-party group 形式接入 `dotf`：在 `agents/skills.yaml` 声明 group、由 `make skills-lock-update` 审计并写入 `agents/skills.lock.yaml`，再 `dotf agents -c` 下发。

## 外部依赖

上表的 skill 之间互引（如 `taskflow` 委托 `openspec-*`、`agent-roster-flow` 委托 `agent-roster`）都已在仓内解决；仍依赖下列**不在本仓库**的 skill / 工具（skill 目标目录同为 `~/.agents/skills`）：

| 外部依赖 | 来源 | 被谁依赖 |
| --- | --- | --- |
| `openspec-explore` / `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` | `@fission-ai/openspec` CLI 生成 | taskflow、task-explore、task-wizard、agent-roster-flow |
| `grilling` | `mattpocock/skills` | task-explore（explore 阶段唯一委托） |
| `grill-with-docs` / `domain-modeling` | `mattpocock/skills` | task-wizard、agent-roster-flow（grill-with-docs 含两跳到 `grilling` + `domain-modeling`） |
| `acpx`（二进制，非 skill） | https://acpx.sh | agent-roster 的委派执行 |

> `task-explore` 的 explore 阶段**禁止**调用 `grill-with-docs` / `domain-modeling`（它们会写仓库根 `CONTEXT.md` / `docs/adr/`，与任务目录落点冲突）；这两个只在 task-wizard / agent-roster-flow 的路径里出现。

### 一键安装（Makefile）

不在 `dotf` 环境里时，用仓库根的 Makefile：

```bash
make install-deps   # 外部依赖全量（openspec-* + grilling 系列）+ 结尾 check-deps
make check-deps     # 逐项检查 ~/.agents/skills，缺项非零退出
make install-acpx   # acpx 缺失提示（需按上游方式手动装）
```

细分 target：`install-openspec` / `install-matt`。安装位置可用 `SKILLS_DIR=` 覆盖。

已用 `dotf agents -c` 的不需要本 Makefile——`dotf` 已覆盖上述来源（openspec-* 由同一入口调 `openspec init` 生成）。

## 说明

- 源布局：`skills/<id>/`（git 真相）。仓库根 `.claude/skills/` 下的软链仅为本仓开发时在 Claude Code 里即时生效，不影响安装路径（安装一律走 `npx skills` / `dotf`）。
- skill 结构按「最小 → 完整」分层：`SKILL.md` + `references/` 是底线，`tests/` `evals/` `examples/` `experience/` `patches/`/`evolutions/` 按各 skill 成熟度逐步补齐（现状多数 skill 尚无全套）；规范定义见 AGENTS.md「结构约定」。
- `agent-roster` 的仓级文档（ADR、CONTEXT、README）在 `docs/agent-roster/`，保留自其独立仓的完整 git 历史。
- `lark-cli` 的官方 `lark-*` skill 嵌在 lark-cli 二进制里（`lark-cli skills read` 按需读取），不需要也不应该装进 `~/.agents/skills`。
- License: MIT。
