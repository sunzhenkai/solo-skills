# explore 与 design 阶段

<!-- 原 phase-explore.md -->
# explore 命令

进入本命令后执行。未绑定任务则先回到 `SKILL.md` 的绑定规则。

## 仅 grill 与完整 explore

| 形态 | 何时 | 做什么 |
|------|------|--------|
| **仅 grill** | taskrail `tier: simple` / `medium` | 只委托 `grilling` 追问细节、边界与约束（目标 / 做完的样子 / 不做 以 `wizard/intent.md` 确认版为准，不重问）；纪要可落 `explore/`；不强制 glossary/ADR 全套 |
| **完整 explore** | `tier: complex` 或用户点名完整探索 | 下文步骤全做（含外部参照、术语/ADR） |

针对任务，不断探索预期目标。**只委托 `grilling`。** 禁止调用 `grill-with-docs` 或 `domain-modeling`：它们会写仓库根 `CONTEXT.md` / `docs/adr/`，与任务目录落点冲突。

1. 必须已绑定任务；否则先走绑定。
2. 先读 `TASK.md`、已有 `glossary.md` 与 `design/`。
3. `TASK.md` **方案** 小节已有上游方案（含 taskrail wizard 的流程总览方案）时，已对上出处的事实与已知步骤照原样复核，不重问。方案里的假设仍是假设。grill 只针对未覆盖的预期目标、成功标准、质量目标、范围、约束与未知。会改方案走向的未知，先读并做完 [external-precedent.md](../../taskrail/references/external-precedent.md)，再问剩下的决策。方案随后按 explore / design 结论更新回该小节。
**意图已定**：经 taskrail 且 `wizard/intent.md` 为 `confirmed` / `assumed` 时，其「你要的是 / 做完的样子 / 不做」视为已定，grill 不重问；只问细节、边界、术语与约束。grill 中发现与确认版冲突：停下回 `task-intent` 纠偏，不在 grill 里改写意图；后续按 taskrail 契约「意图变更」处理判据与 phase。
4. 读取并遵循 `grilling`。不可用则用它的轮次格式当面问；**不要发明等价命令**，也不要改调 `grill-with-docs`。
5. 问的是**预期目标、成功标准、质量目标、范围、约束、未知**。质量目标含观感 / 性能 / 可靠性等维度；不可确定性度量的（典型：UI 观感、体验手感）追问验收方式或参照。事实自己查，决策交给用户。
6. 发现任务含多个可独立推进的方向时，**提示一次**可 `expand`/`split` 拆子任务，不阻断、不自动创建；用户确认后走 `expand`。
7. 术语结晶时由本 skill 写入 `{taskRoot}/glossary.md`；独立决策写入 `{taskRoot}/design/adr-<slug>.md`。禁止写仓库根 `CONTEXT.md`、`docs/adr/`。质量目标（含观感 / 体验类）的澄清结论写入 `explore/` 纪要，供 design 阶段质量画像草稿吸收，不另起文档。
8. 结束本轮时列出已澄清目标与仍开放的 frontier，并提示是否 `save`。

术语/ADR 可当时写入任务目录；那不是对 `TASK.md` 的替代，进展仍要按主文件提示是否更新任务文档。

## 外部参照钩子（原 external-precedent.md）

细则唯一真源：[taskrail/references/external-precedent.md](../../taskrail/references/external-precedent.md)。先搜后读、来源分级、一次尝试、事实/假设二分写入，一律按该文件执行，本文件不复制第二份。

本 skill 只保留阶段钩子：

- `design`：写对比表之前做一次。
- `explore`：只有这个未知会改方案走向时做。其余问题照常问。
- 同一问题、已记下的出处仍对得上：沿用已有条目。
- 问题变了、出处对不上、或当时记的是未找到：再做一次。

落盘：写入设计稿的「外部参照」一节。更新 `TASK.md` 方案时，事实和假设分列，假设保持为假设。笔记里写明这一轮追的是哪一个做法，以及结果是事实、假设，还是两条相反的事实，然后继续本阶段原来的下一步。


<!-- 原 phase-design.md -->
# design 阶段

进入本阶段后执行。未绑定任务则先回到 `SKILL.md` 的绑定规则。落盘时再读 [templates.md](templates.md)。

针对任务方案进行设计。从原 `task-design` 移植：**写入 `{taskRoot}/design/`，不是 `docs/design/`，也不是 OpenSpec driver。**

**在方案不明朗时，应主动打断，提示缺口。** 未过门禁不得假装设计完成。

## 门禁（先于落盘）

缺任一项就停下，列出缺口，建议先 `explore` 或继续 `chat`，不要写空心方案：

- 目标能一句话说清
- 成功标准可检验
- 「方案」含质量画像与显式降级原文快照时，先按「画像展开」把它落进设计稿再落盘；快照缺失则按缺口停下报告，不自己补一份画像
- 约束（技术 / 时间 / 范围）已知或已标明未知
- `wizard/plan.md` 有「流程总览」时，设计步骤逐条对齐总览；新增 / 删改 / 改序写显式决策（与 taskrail 契约阶段载荷表同一要求）
- 能形成至少两个可行方案；否则说明还缺哪些信息
- 架构 / 接口 / 技术栈的选择都写得出依据（设计模式或软件工程原则）；写不出就列入未决，不算设计完成。本任务不涉及这三类选择时写「不适用」并说明，不为凑数贴模式名
- 命中交付类别门包时（[../../taskrail/references/gate-packs.md](../../taskrail/references/gate-packs.md) 判定见 taskrail wizard 的「交付类别与门包」节）：设计稿必须含**契约文件指针**（共享面冻结产物：接口 / 类型 / primitive / 目录与命名 / 样板切片）与**证据计划**（该交付类别的证据形式、产物状态绑定方式与覆盖边界）。缺任一项按缺口停下，不写空心方案
- **Web UI Active Instance 门**：交付类别为 Web UI 时，先核对交付项目根 Active Instance。**medium / complex**：无 `status: frozen` 则停下，先在交付项目根建立 Active Instance 至 freeze（有参照源先提炼 tokens / primitive），**不写空心 UI 方案**、不在 design 稿重定义 token / primitive 精确值。**simple**：无 freeze 仅可走 adopt-only（沿用交付仓已有组件库），并在质量画像登记显式降级（未确认不得进入可批准定稿）。已 freeze 时 `design/contract.md` MUST 含：Active Instance 根路径、contract / binding / projection 三条 digest、（如有）package pin；任务 design 只做业务 IA、页面清单 ↔ Page Type、数据与验收。

推荐若依赖未决项，把未决单独列出，不要写成已定。

## 画像展开（上游含质量画像时）

- 设计稿正文**逐字复制** `TASK.md`「方案」里的质量画像与显式降级原文快照，再在其下展开；`TASK.md` 路径或小节指针不能替代原文。
- 每条 `角色底线` 至少展开到三个可检查面：UI（哪个页面、哪些交互与状态）、数据（一致性、并发、持久化假设）、验收（怎么验：运行、截图、测试、启动步骤）。写成可检查的话，「高质量」「体验好」「足够健壮」不算。
- 展开只细化画像已有字段，不改档位与范围，也不新增架构 / 接口 / schema / 代码骨架设计。某条展不下去：列入未决并提示缺口，不默默省掉。
- 输入里没有质量画像时本节不适用，不要为设计稿编造一份。

## 设计依据（架构 / 接口 / 技术栈）

每个影响架构、接口或技术栈的选择，写明依据与它换来的可检后果。这是「方案」与「贴模式名」的分界：模式名本身不是依据。

- 一行一条：`选择 → 模式 / 原则 → 为何适用 → 可检后果`。
- 可检后果写成少了什么——耦合面、接口面、重复、可替换点、可测性、回归面；「更优雅」「更规范」不算。
- 模式要落到具体的变化点或重复点：「这里用了工厂模式」不是依据，「这三处创建分支只差一个参数，收进一个构造点」才是。
- 引入该模式拿不出可检后果时，写「不引入」并说明当前做法为何够用，不为对齐名词引入结构。
- 既有代码里已有同类问题的成熟做法时，优先对齐并链到它（「现状」节），偏离处写明理由。
- 写不出依据的选择列入未决，不算已设计。

与「外部参照」的分工：外部参照追的是别人怎么做的**出处**（[external-precedent.md](../../taskrail/references/external-precedent.md)），设计依据写的是本选择**凭什么成立**；一条选择可以两者都有，互不替代。

## 三阶段：探索 → 设计 → 写入任务

停在实现边界。只写入 `{taskRoot}/design/`。

1. **探索（对话，可不落盘）**：干系人与成功标准；现状（读代码与已有文档）；约束；未知与风险（写明「还不知道 X」）。写对比表之前读并做完 [external-precedent.md](../../taskrail/references/external-precedent.md)。问题仍模糊时给 2–3 种问题框架让用户选。
2. **设计**：至少两个可行方案再推荐。选项 + 对比表（成本、风险、复杂度、可逆性、工期）。产物见 [templates.md](templates.md)。推荐方案的架构 / 接口 / 技术栈选择按「设计依据」逐条给出。多用 ASCII / Mermaid。
3. **写入当前任务**（不晋升到仓库文档）：

| 文件 | 作用 |
|------|------|
| `design/README.md` | 文档索引 |
| `design/<topic>.md` | 主设计（可多篇） |
| `design/contract.md` | 契约文件指针与证据计划（命中交付类别门包时必需；只存指针，契约本体落交付仓；Web UI 另含 Active Instance 根路径与三条 digest） |
| `design/adr-<slug>.md` | 独立决策 |

## 边界

- 不写实现代码，不创建 OpenSpec `tasks.md`
- 命中门包时不得省略契约文件指针与证据计划；本 skill 只留指针，契约本体落交付仓并由交付仓维护
- Web UI：禁止在 `{taskRoot}/design/` 重写 `core/tokens.yaml` / primitive 精确值；改 DS 本体只在交付项目根修订 Active Instance 并重新 freeze
- 不把设计写到任务目录以外（尤其禁止 `docs/design/`）
- 必须有图和权衡表；推荐与未决分开写
- kebab-case、一篇一个 H1

## 对比表 / 推荐

```
| 方案 | 成本 | 风险 | 可逆性 | 工期 | 复杂度 |
|------|------|------|--------|------|--------|
| A    | $$   | 低   | 高     | 2w   | 低     |
| B    | $    | 中   | 低     | 1w   | 高     |

**推荐：方案 B**，因为 [主因]。
接受的取舍：[列表]。
回退计划：[如何撤回]。
```

## 交接

```
## 交接

**已设计**：[一句话]
**位置**：`{taskRoot}/design/`
**未决问题**：[列表，或无]
**下一步**：approve / expand / save / chat（要交付走 approve → handoff，不要直接写代码）
```

结束后提示是否更新 `TASK.md`。
