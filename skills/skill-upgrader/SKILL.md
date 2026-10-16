---
id: skill-upgrader
name: skill-upgrader
description: "以可审计 patch 更新已有 Skill（update）、升级为自进化结构（self-upgrade），或按真实执行经验进化正文（evolve，原 skill-evolver）。用户点名 skill-upgrader / skill-evolver、要求改已有 Skill 正文，或其他 skill 需要走 patches/ 审计时使用。"
---

# Skill Upgrader

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文，不要逐词硬翻。

本 Skill 是**公用**工具：可对任意含 `SKILL.md` 的目录做可审计更新，或做一次性自进化结构升级。所有生产改动必须先写入目标 Skill 的 `patches/`（`evolve` 模式写 `evolutions/`），禁止先改生产文件、事后补 patch。

## 与相关 Skill 的关系

| Skill | 职责 |
|-------|------|
| **本 skill** | 任意 Skill：模式门禁后，`update`（改正文/配套）或 `self-upgrade`（加 examples/evals/experience）；二者都走 `<skill-dir>/patches/` |
| `evolve` 模式（原 `skill-evolver`） | 基于多次真实执行：提案 → `evolutions/` 候选 → eval → 晋升生产稿；进入时读 [references/evolve.md](references/evolve.md) |

- 用户点名 `skill-evolver` 或要求按**执行经验**进化时：选 `evolve` 模式，按 [references/evolve.md](references/evolve.md) 执行（用 `evolutions/`，不写 `patches/`）；下文工作流/patch 协议只适用于 `update` / `self-upgrade`。
- `update` / `self-upgrade` **不**根据经验改目标 Skill 的核心行为（那是 `evolve`）。目标尚未具备自进化目录且用户要自更新时，走 `self-upgrade`。

## 模式门禁（强制）

未判定模式前，不得写 patch、不得改生产文件。

根据用户表述判定 **唯一** 模式：

| 模式 | 何时选用 | 做什么 |
|------|----------|--------|
| `update` | 修改已有行为、流程、门禁、references/scripts、修 bug、澄清规则等，**不**以「变成自进化」为目的 | 对生产内容做最小可审计 patch |
| `evolve` | 点名 `skill-evolver`，或要求基于多次真实执行经验进化正文（仅显式触发） | 读 [references/evolve.md](references/evolve.md)，提案 → `evolutions/` 候选 → eval → 晋升 |
| `self-upgrade` | 明确要把已有 Skill **切换/升级为自更新**（加 examples / evals / experience，并注入自进化指令） | 按布局模板补目录与注入段落；改动仍打包进 patch 再应用 |

判定规则：

1. **只说「改 / 修 / 更新 / 重构 Skill」**且未提自进化 → `update`。
2. **点名自进化 / 自更新 / 加 examples·evals·experience / 升级为可进化** → `self-upgrade`。
3. **两者都像或都不像**：先问一句二选一，不猜。笼统的「优化一下这个 Skill」不算已选定模式。
4. **按真实执行经验进化正文**（含点名 `skill-evolver`）→ `evolve`。
5. **从零创建 Skill** → 停止；走写作/安装类流程。

一次会话只处理 **一个** 目标 Skill、**一种** 模式、**一轮** patch。

## 门禁（通用）

1. **仅显式触发**：用户点名本 skill / `{{slash:skill-upgrader}}`，或明确要求更新已有 Skill / 升级为自进化。
2. **必须有目标**：给出 skill 名、id 或含 `SKILL.md` 的目录。未指定先问，不猜。
3. **禁止从零创建**：没有现成 `SKILL.md` 就停止。
4. **禁止伪造历史**：`self-upgrade` 时没有真实成功案例就不要编 examples；没有真实执行就不要写 experience 条目。
5. **先 patch 后应用**：任何生产改动必须先有本轮 `proposal.md` + `change.patch`，校验通过并按风险门禁确认后再 `git apply`。

**不算触发**：安装外部 Skill、根据一次失败直接改正文（无模式门禁）、自动进化。

## 强制前置判断

确定改动前，完整读取目标 `SKILL.md` 及与请求直接相关的配套文件，并明确判断：

1. **意图**：要新增、删除或改变什么行为？模式是否已由门禁锁定？
2. **冲突**：是否与现有 frontmatter、门禁、流程、脚本、测试或其他 Skill 职责冲突？
3. **合理性**：改动是否通用、可执行、可验证？`self-upgrade` 是否真的需要自进化结构？

任一项不明确或存在多种会显著改变结果的解释时，先向用户提出聚焦问题，不写 patch。发现请求不合理或冲突时，说明依据并给出最小替代方案；不得机械执行。

## 公开性与隐私

写入目标 Skill 的内容须可随该 Skill 分发：

- 不写入个人姓名、账号、主机名、绝对家目录、凭据、密钥、内部 URL、公司信息或私有仓库内容。
- 路径使用相对路径或语义占位符（如 `<skill-dir>`、`<skill-name>`）。
- 示例使用虚构、通用数据。
- 机器特例留在本地配置，不进入共享 Skill。

## Patch 目录协议

每轮在目标 Skill 目录下新建 `patches/<YYYYMMDD-HHMMSS>-<slug>/`（proposal.md / change.patch / result.md）；目录规则、仓库根与生产稿定位、字段模板：**写 patch 前先读** [references/patch-protocol.md](references/patch-protocol.md)。

## 工作流（两模式共用）

update / self-upgrade 共用 7 步（模式门禁与定位 → 提案 → 风险 → 先写 patch → 校验与门禁 → 应用与验证 → 写结果）及 Progress 清单：**选定模式后先读** [references/workflow.md](references/workflow.md)。

## 模式：update

最小改动满足意图。保留原目标、流程、工具用法、输出与约束；不扩 scope、不顺手润色、不为「以后方便」塞自进化目录。

若用户其实要自进化结构，切回模式门禁，改走 `self-upgrade`，不要在 `update` 里偷偷加 `examples/` `evals/` `experience/`。

---

## 模式：self-upgrade

选定 `self-upgrade` 后读 [references/self-upgrade.md](references/self-upgrade.md)（保留原文、组装内容、Evolution Criteria）。组装时用到的文件都从这里直接打开：

- 复制清单 [references/layout.md](references/layout.md)；Eval 抽取规则与 schema [references/evals.md](references/evals.md)
- 追加到目标 SKILL.md 的一句指针 [references/skill-injection.md](references/skill-injection.md)
- 复制源 [references/examples-README.md](references/examples-README.md) / [references/evals-README.md](references/evals-README.md) / [references/experience-README.md](references/experience-README.md) / [references/cases.template.yaml](references/cases.template.yaml)
- 日后条目格式 [references/example-case.md](references/example-case.md) / [references/experience-entry.md](references/experience-entry.md)

## Versioning

修改 Skill 时不要直接覆盖原意而不留记录。本 skill 以 `patches/<id>/` 作为审计与版本线索；有 Git 时同时依赖 Git 历史。

## 安全约束

- 不把密钥、内部 URL、公司代码、个人凭据写进 examples / evals / experience / SKILL.md / patches 正文
- 不删除仍在生效的安全/门禁规则（除非 `update` 且用户确认该规则本身有害）
- `evals/cases.yaml` 只写可验证期望，不写攻击步骤、exploit、凭据

## Final Validation（self-upgrade）

self-upgrade 收尾校验清单见 [references/self-upgrade.md](references/self-upgrade.md)「Final Validation」。

## 交付

```text
skill: <name>
path: <skill-dir>
mode: update | self-upgrade
patch: <patch-id>
risk: low | medium | high
status: proposed | applied | failed | already-upgraded | aborted
change: <一句话>
validation: <通过项或失败原因>
next: <需要确认、sync 提醒、转 evolve 模式，或无>
```
