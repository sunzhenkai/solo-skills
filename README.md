# task-flow-skills

任务流与交付编排的可复用 Agent Skills（从 `sunzhenkai/dotfiles` 迁出，独立维护）。

## 包含的 Skills

| Skill | 用途 |
| --- | --- |
| `task-wizard` | 生成步骤级任务方案（动作/要点/验证 + 质量画像） |
| `task-explore` | 长周期/目标不清任务的探索台账（tasks/INDEX.md 推进） |
| `taskflow` | 一个 driver change 编排一批子 change 的任务生命周期 |
| `delivery-loop` | 把复杂交付目标编排成自动闭环（探索→实现→证据→评审→复验） |
| `role-based-reviewer` | 可组合的角色化只读评审（engineer/algo/data/sre/ops/biz/product/design/qa） |
| `agent-roster-flow` | 按 Stage 编排跨 agent 任务，逐段选 Endpoint 与模型委派执行 |

## 安装

### 通用（npx skills）

skill 源在仓库的 `skills/<id>/`；CLI 的发现优先级前缀含 `skills/`，整仓安装即可：

```bash
npx skills add sunzhenkai/task-flow-skills                 # 全部六个
npx skills add sunzhenkai/task-flow-skills -s taskflow     # 只装一个
```

### dotfiles 编目（第三方）

本仓库以 third-party group 形式接入 `dotf`：在 `agents/skills.yaml` 声明 group、由 `make skills-lock-update` 审计并写入 `agents/skills.lock.yaml`，再 `dotf agents -c` 下发。安装条目为上面六个 skill id。

## 外部依赖

六个 skill 里 `role-based-reviewer` 自包含，其余依赖下列**不在本仓库**的 skill / 工具（目标目录同为 `~/.agents/skills`）：

| 外部依赖 | 来源 | 被谁依赖 |
| --- | --- | --- |
| `openspec-explore` / `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` | `@fission-ai/openspec` CLI 生成 | taskflow、task-explore、task-wizard、agent-roster-flow |
| `grilling` | `mattpocock/skills` | task-explore（explore 阶段唯一委托） |
| `grill-with-docs` / `domain-modeling` | `mattpocock/skills` | task-wizard、agent-roster-flow（grill-with-docs 含两跳到 `grilling` + `domain-modeling`） |
| `agent-roster` | `sunzhenkai/agent-roster` | agent-roster-flow、task-explore（plan-review 委派） |
| `acpx`（二进制，非 skill） | https://acpx.sh | agent-roster 的委派执行 |
| `skill-upgrader` | `sunzhenkai/dotfiles` | delivery-loop（失败归因为 skill gap 时） |
| `commit-push` | `sunzhenkai/dotfiles` | agent-roster-flow（收尾可选） |

> `task-explore` 的 explore 阶段**禁止**调用 `grill-with-docs` / `domain-modeling`（它们会写仓库根 `CONTEXT.md` / `docs/adr/`，与任务目录落点冲突）；这两个只在 task-wizard / agent-roster-flow 的路径里出现。

### 一键安装（Makefile）

不在 `dotf` 环境里时，用仓库根的 Makefile：

```bash
make install-deps   # 外部 skill 全量 + 结尾 check-deps
make check-deps     # 逐项检查 ~/.agents/skills，缺项非零退出
make install-acpx   # acpx 缺失提示（需按上游方式手动装）
```

细分 target：`install-openspec` / `install-matt` / `install-agent-roster` / `install-dotfiles`。安装位置可用 `SKILLS_DIR=` 覆盖。

已用 `dotf agents -c` 的不需要本 Makefile——`dotf` 已覆盖上述全部来源（openspec-* 由同一入口调 `openspec init` 生成）。

## 说明

- 源布局：`skills/<id>/`（git 真相）。仓库内 `.agents/skills -> ../skills` 是**本地软链、已 gitignore 不提交**——dotfiles 第三方 lock 校验器拒绝 symlink，且 `subdirectory` 直接指向 `skills/<id>`，无需该链。
- 每个 skill 自包含（`SKILL.md` + `references/` + `scripts/` + `tests/` + `evals/` + `patches/`/`evolutions/`），目录结构相对各自根目录。
- `agent-roster-flow` 依赖底层的 `agent-roster` skill（不在本仓库，来自 `sunzhenkai/agent-roster`）。完整外部依赖见上节「外部依赖」与 `make install-deps`。
- License: MIT。
