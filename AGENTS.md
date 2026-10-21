# AGENTS.md

本文件为 AI agent 提供本仓库的快速上下文与工作约定。

> **约定**：本仓库不建 `CLAUDE.md` 等 agent 专属副本，统一以 `AGENTS.md` 为唯一上下文文件（各 agent 通过软链或配置指过来）。

## 这是什么

sunzhenkai 的第一方 Agent Skills 集合（公开仓，MIT）：任务流编排、交付闭环、角色评审、跨 agent 委派、代码/仓库/知识工具链。**无业务代码、无构建**——git 真相只有 `skills/<id>/`。skill 清单与用途见 `README.md`。

- 根目录 `.claude/skills -> ../skills` 是整目录单软链，仅为本仓开发时在 Claude Code 里即时生效，不是安装路径。
- 安装方式见 README「安装」一节（npx skills / dotf 编目 / Makefile）；`skills-lock.json`、`.agents/` 已 gitignore。

## 常用命令

无构建、无 lint 配置；自动化门禁只有 pytest 契约测试。

```bash
python3 -m pytest skills -q               # 全部测试（秒级）
python3 -m pytest skills/<id>/tests -q    # 单个 skill 的测试

make check-style    # 输出风格检查（意图复述字段齐全；SKILL.md >8KB、description 过长、引用链超一层、禁令词偏多只告警）
make check-deps     # 检查外部依赖 skill 是否就绪（缺项非零退出）
make install-deps   # 安装外部依赖（openspec-* + grilling），结尾跑 check-deps
make install-acpx   # acpx 缺失提示（二进制，需按上游方式手动装）
```

`SKILLS_DIR=` 可覆盖安装目标（默认 `~/.agents/skills`）。已用 `dotf agents -c` 的环境不需要本 Makefile。

## 结构约定

每个 skill 自包含，目录相对各自根：

- `SKILL.md`：正文，YAML frontmatter（`id` / `name` / `description`）。description 是常驻上下文的触发指针，只写正向的 WHAT + WHEN：关键词前置，每个真分支一个触发词，不写「何时不用」；与相邻 skill 的边界放正文一句。
- 主要靠用户点名触发、且没有别的 skill 自动调用的，frontmatter 设 `disable-model-invocation: true`，description 改成给人读的一行摘要。
- SKILL.md 只从正文一层直链 `references/` 等文件，不经中间文件再跳。
- `references/`：按需加载的细则。`scripts/`：**只依赖 Python 3 标准库**，不引第三方包。
- `agents/`：部分 skill 携带的第三方 agent 配置（如 `openai.yaml`），可选。
- `tests/`：stdlib unittest 写的**文本契约测试**——校验 SKILL.md 与 references 里的阶段门禁、落点、硬闸等文本约束，不模拟执行；断言优先锚定正向行为句，而非「不要 / 禁止」字面。改正文后必须过测试。
- `evals/`：声明式案例（`cases.yaml`），无自动 runner，供人工 / agent 评审。
- `examples/` `experience/` `patches/` `evolutions/`：示例、经验、变更审计。

## 改 skill 正文的流程

- 结构缺失（无 `examples/` / `evals/` / `experience/`）先走 **skill-upgrader** 一次性升级结构。
- 基于真实执行经验改正文走 **skill-upgrader 的 `evolve` 模式**（原 skill-evolver）：仅显式触发，**禁止自动进化**（一次失败 / 一次用户纠正都不足以改 skill）；先展示 Evolution Proposal，用户确认后才写 `evolutions/<date-slug>/`（proposal.yaml + decision.md + eval.md + 候选稿）。
- 变更留审计痕迹：每次改某个 skill 的正文或配套，就在该 skill 下新建 `patches/<YYYYMMDD-HHMMSS>-<slug>/`（proposal.md + change.patch + result.md），或走 `evolutions/`。`patches/` 有变更即补：skill 第一次被改时随该次变更创建，不预建空目录。

## 外部依赖（不在本仓）

skill 之间的互引已在仓内解决；仍依赖下列仓外内容（详见 README「外部依赖」）：

| 依赖 | 来源 | 被谁依赖 |
| --- | --- | --- |
| `openspec-explore` / `openspec-propose` / `openspec-apply-change` / `openspec-archive-change` | `@fission-ai/openspec` CLI 生成 | taskflow、taskrail、agent-roster（flow 模式） |
| `grilling` | `mattpocock/skills` | `grill-with-docs` 的下游（agent-roster flow 模式） |
| `grill-with-docs` / `domain-modeling` | `mattpocock/skills` | agent-roster（flow 模式）；无台账一次性拷问 |
| `acpx`（二进制，非 skill） | https://acpx.sh | agent-roster 的委派执行 |

- 任务编排入口是 **`taskrail`**；确认协议是 taskrail 的薄引用 `skills/taskrail/references/confirm-protocol.md`。design 第一步的 grill 由本仓自问自答（方法见 `taskrail/references/design.md`），不委托外部 skill。
- 安装仓外 skill 前走 skills-store 的安全审计流程（先临时拉取 → audit-skill.sh → 再安装）。

### task* 要点

- 流程：`wizard → design(grill) → approve → [handoff] → propose → apply → archive → done`（档位 `skip` / `full`：skip 直接实现 + 验证、不建 driver；full 经 handoff 走 OpenSpec；handoff 是动作不是 phase）。
- 拆分：wizard 第 5 步定，默认不拆；同一份交付拆成一个 driver 下的切片（按依赖滚动展开、逐片提交），要分别交付的才拆子任务，放在父任务的 `subtasks/` 下（继承父任务意图，范围内不停；父任务验总判据收尾）。细则 `taskrail/references/large-scope.md`。
- 台账：凡经 taskrail 的任务进 `tasks/ongoing/{slug}/`，`TASK.md` 持 `phase` / `confirm_mode` / `criterion`；交付进度仍只认 OpenSpec checkbox。
- 契约真源：`skills/taskrail/references/contract.md`；完成清单：`skills/taskrail/references/done.md`；流程与使用总览（给人读）：`docs/task-flow/README.md`。
- 两件套：`taskrail`（意图确认、探索、设计、审批、交接都是它的阶段细则）+ `taskflow`（交接后的执行）。
- 意图确认：wizard 第 1 步按 `taskrail/references/intent.md`（落 `wizard/intent.md`；goal 由另一个模型按该文件第 5 节清单代审）；`taskrail intent <目标>` 只做这一步。design 第一步的 grill 在其后，只追细节不重问意图。
- 跨 skill 常用词统一：**台账**（ledger，持久记账文件：task 系列的 `TASK.md`/`INDEX.md`、repo-manager 的 `.repo-manager.md`）、**交接**（handoff，动作；agent-roster 的 Handoff 指受派方的产出文件）、**grill**（自问自答拷问，trouble-grill 用于排查）。新文本沿用这三个词，不另造同义词。
- 术语：`skills/taskrail/references/contract.md`「术语」节；端到端回归样例：`skills/taskrail/examples/minimal-webui/`（`tests/test_e2e_handoff_flow.py`）。

## Skill 设计原则

- **通用性优先**：skill 面向一类问题而非一个具体场景。通过机制（协议、阶段门禁、契约）解决问题，避免为单一案例特例化；遇到具体需求时先问「这类问题的一般解是什么」。
- **SKILL.md 体量**：单个 `SKILL.md` 宜控制在约 8KB 以内（`make check-style` 超限告警，不阻断）——正文只留触发、路由、不可跳过的门禁要点与指针，模板、逐条细则与例外下沉到 `references/`，按命令/阶段按需加载。
- **可自进化**：skill 随真实执行经验改进，链路统一由 skill-upgrader 承担（`evolve` 正文演进、`update` / `self-upgrade` 修订与结构升级），经验沉淀在 `experience/`、变更留痕在 `patches/` / `evolutions/`。各 skill 正文不复制自进化样板，需要时只留一句指向 skill-upgrader 的指针。
- **正向表述**：正文写目标行为；确需硬闸（不可逆、安全）时保留，并配一句正向的安全默认。

## 公开仓纪律

- 提交前跑 `make check-names`、`make check-style`（`.project-denylist` 列具体项目名；确需保留的行加 `project-name-allow`）与 `~/.local/bin/pytest skills tests`（或环境中的 pytest）。

- **这是开源仓库**：任何提交都可能被公开检索，应避免提交隐私信息（密钥、内部 URL、主机名、内网地址、公司/项目名、真实任务描述）。写任何文件前自查一次。
- **只放机制，不放数据**：名册、案例、路由规则、运行痕迹存使用者私有位置。
- **运行时只读**：skill 装到各 agent 目录是字节复制而非软链，运行时往 skill 目录写东西只写进镜像、下次同步被覆盖——运行产物一律落仓库之外，`experience/patterns/` 只在源仓改。

## 其他

- `docs/agent-roster/`：agent-roster 的仓级文档（ADR、CONTEXT、README），保留自其独立仓的完整 git 历史；细则见 `docs/agent-roster/AGENTS.md`。
- `lark-cli` 的官方 `lark-*` skill 嵌在 lark-cli 二进制里（`lark-cli skills read` 按需读取），不装进 `~/.agents/skills`。
- 语言：面向使用者的文档用简体中文；命令名、路径、代码、状态值与既成术语（ACP、Endpoint、OpenSpec 等）保持原文。
