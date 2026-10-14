# taskrail 契约（阶段 / 载荷 / 闸口 / 目录）

本文件是 task* 族重组后的**唯一真源**。`taskrail`（含确认协议 [confirm-protocol.md](confirm-protocol.md)）/ `task-explore` / `taskflow` 与本文有出入时，以本文为准（术语定义见本文「术语」节）；各 skill 正文只写执行细则，不另造阶段枚举。

## 流程

```text
confirm_mode: human | goal

wizard → explore(+grill) → design → approve → [handoff] → propose → apply → archive
         ↑ expand 可插在 explore / design 之后
         ↑ handoff = 动作，不是 phase
```

| 档位 (`tier`) | 路径 |
|---------------|------|
| simple | wizard → apply(直接实现 + 验证) → done |
| medium | wizard → explore(仅 grill) → design(可轻) → approve → handoff → propose → apply → archive |
| complex | wizard → explore(+grill) → design → approve → handoff → propose → apply → archive |

简单/中等是**跳过**中间阶段（simple 跳过 explore / design / approve / handoff，直接实现；medium 的 explore 仅为 grill），不是另一套 skill。

### simple 专条

- simple **不建 driver、不走 OpenSpec**：wizard 定稿（意图确认 + 含判据的简短 plan）后直接实现；验证命令与结果写入 `TASK.md`「验证」节，过完成门即 `done`。
- 实现中发现超出局部修改（跨模块、需拆切片、命中复杂硬指标）→ 停下升档为 medium，补 explore / approve / handoff。
- 不可逆、线上、对外发送等动作仍按确认协议逐步授权；`criterion` 同样不得无声改写。

## 非 phase 动作

下列是动作，**不得**写入 `TASK.md.phase`：

| 动作 | 时机 | phase / status 影响 |
|------|------|---------------------|
| `grill` | 属 `explore` 子步骤；有台账时委托 `grilling` | 不单独占 phase |
| `handoff` | approve 已冻结后、进入 `propose` 前；委托 task-explore `handoff` | `status:=handed-off`，`phase:=propose`，写入 `driver` |
| `expand` | explore / design 后按需 | 建子任务目录；父 `phase` 不变 |

### approve 出口

`status` 为 `ongoing` 且尚未 `handed-off` 时，approve 完成后的唯一推荐下一步是 `handoff`。查证项与外部依赖写入「可带进实现的未决」，未决不阻断交接。同一已冻结方案的多条实施线建成该 `{slug}-driver` 的 taskflow 子 change。禁止用当轮叙事改写 `criterion`。已冻结方案含实施动作且尚未 `handed-off` 时，拒绝进入 archive。

## 意图变更

用户在 wizard 之后改主意（或 grill / design / apply 发现与 `wizard/intent.md` 冲突）时，按序，不得跳步：

1. 重跑 `task-intent`，改写 `wizard/intent.md` 并在其纠偏记录追加一行（旧版靠 git 追溯）。
2. 「做完的样子」变了 → 走确认协议**显式**改 `criterion`（human 逐条确认；goal 审阅收敛），记入 `TASK.md` 决策节；这是唯一合法改写，不算「用当轮叙事改写」。
3. phase 回退：只改细节 → 留在当前 phase；改范围 / 判据且未 `handed-off` → 回 `wizard`（方案未冻结）或 `design`（已有设计）；已 `approve` 的须重新 approve。
4. 已 `handed-off`：探索侧不回退，经 taskflow 开修订子 change（或修订 driver 判据快照），未勾 checkbox 按新判据重排；已交付部分写显式决策。

## 目录

```text
tasks/
├── INDEX.md
├── ongoing/{slug}/
│   ├── TASK.md
│   ├── wizard/plan.md
│   ├── wizard/intent.md         # task-intent 确认版（含纠偏记录）
│   ├── evidence/intent/         # 意图摸底详情（只读 subagent 写）
│   ├── explore/                 # grill 纪要等（可选）
│   ├── design/
│   ├── approve/                 # 评审意见 + APPROVED.md
│   ├── handoff.md               # 交接摘要（可选；也可写在 TASK.md 交接节）
│   ├── glossary.md              # 惰性
│   └── {sub}/                   # expand：只一层
└── archive/{yyyy-mm-dd}/{slug}/
```

- 凡经 `taskrail` 推进的任务一律建 `tasks/ongoing/{slug}/`（含简单档）。
- 无 `tasks/` 时须先获确认再建（沿用 task-explore 纪律）。
- 运行产物（证据、确认计数器）落**仓外**；`TASK.md` 只存指针（如 `evidence_root`）。
- 命中交付类别门包时，`design/` 落**契约文件指针**（指向仓库内已冻结的共享面契约）与证据计划，二者随交接进 driver。
- **Web UI**：共享面契约 = 交付项目根 `design-system/v1` Active Instance（`status: frozen` + contract / binding / projection digest）；指针与 digest 写在任务 `design/contract.md` 与 driver，**禁止**把 tokens / primitive 精确值复制进 `tasks/`。Active Instance 本体落交付项目根，由交付仓自己维护（task* 的 design 阶段负责建立 / 修订并 freeze）。
- 单任务产物只写当前任务目录；禁止写仓库根 `CONTEXT.md`、`docs/adr/`、`docs/design/`。

## TASK.md 元信息（封闭字段）

```yaml
slug: <kebab-case>
parent: <父 slug；仅子任务>
status: ongoing | handed-off | blocked | done | archived
phase: wizard | explore | design | approve | propose | apply | archive | done
confirm_mode: human | goal
tier: simple | medium | complex
criterion: "<完成判据原文一条>"
driver: null | "{slug}-driver"
evidence_root: <仓外路径或 null>
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

- `phase` 只允许上列封闭枚举。task-explore 的 `new` / `chat` / `save` / `resume` / `reopen` / `expand` / `handoff` 等是**命令**，禁止写入 `phase`。
- `phase` + 各阶段目录产物 = wizard→approve 区间的进度真相。
- propose 之后进度只认 OpenSpec checkbox（driver / 子 change）。
- **一本账**：`TASK.md` 是唯一任务账（目标、判据、phase、决策）；driver 只是 OpenSpec 执行记录，propose 之后的进度看其 checkbox，不在 driver 另记任务状态。`handed-off` **不等于** `done`。
- `done` 仅当完成判据成立且交付标准全过（复杂档另要求质量画像齐全、降级无 `pending`/`provisional`）。

`status` 随 `phase` 走，不另设矩阵：wizard–approve（及 simple 的 apply）为 `ongoing`；handoff 后为 `handed-off`；完成门过为 `done`；归档为 `archived`；`blocked` 停在原 `phase`。

## 阶段载荷契约

阶段跳转必须带齐；缺则停在上一 `phase`，禁止下游猜意图：

| 进入阶段 | 必须已有 |
|----------|----------|
| explore / design | `wizard/intent.md`（`status: confirmed` 或 `assumed`；本规则生效前的旧任务缺失不回溯）+ `criterion` + `wizard/plan.md`（或 TASK.md「方案」节等价正文，含流程总览与质量属性节；有交付产出时含交付类别与适用门包节；Web UI 另含 Active Instance 状态节） |
| design | 流程总览映射：设计步骤 ↔ 总览步骤逐条对齐；新增 / 删改 / 改序写显式决策，供 approve 结构门核对；命中门包时产出**契约文件指针**（仓库内已冻结的共享面契约）与证据计划；Web UI 指针必须含 Active Instance 根路径与三条 digest（档位门见 gate-packs） |
| approve | design 产出路径（或简单档的 plan / explore 纪要）+ `criterion` + 「不做的事」；命中门包时另附交付类别、适用门包与基准物；Web UI：complex 须 digest 与仓库 freeze 一致才可冻结；simple 无 freeze 仅当 adopt-only + 已确认显式降级 |
| propose（经 handoff） | `approve/APPROVED.md`（或 TASK.md 决策节已冻结）+ 判据原文；流程总览快照随交接进 driver；命中门包时门包与契约文件指针一并进 driver；`status: handed-off` 与 `driver` 已写入；`taskflow/scripts/check_handoff.py` exit 0 |
| apply | driver `tasks.md` 已由 propose 产出；simple：wizard 已定稿（`wizard/intent.md` + `criterion`） |
| archive（探索侧） | 用户确认关闭；子任务均已结 |

## 执行座位

高噪声 legwork（大范围摸底、调研、起草、实现切片、评审、验证复跑）**宜**交给 worker（宿主 subagent；点名 Endpoint 时走 `agent-roster`），以并行提速、保持主会话上下文干净。不新增 `phase`，不改变闸口与完成门。宿主无 subagent 或派出失败 → 主会话按同一落点与完成标准自做，**不得**因此停下或改道。

- wizard 意图探索是否并行摸底：跳过条件见 task-intent「何时跳过」。
- **永不派出**：闸口（确认协议）、危险退出、面向用户的提问与选项。
- 派出时交代清楚目标、输入、写入范围与产出位置；apply 的实现者输入引用 taskflow `implementer-isolation`。
- Worker 详情落盘，只回简短摘要（结论 / 落盘路径 / 未决）；转述给用户时按「对用户说话」；主会话不回灌工具轨迹、不转贴全文。产物缺失则停在当前 `phase`。
- `TASK.md` 的 `phase` / `status` / `driver` 仅编排者写；OpenSpec checkbox 由执行 `openspec-apply-change` 的一方按协议勾，编排者回收时核对。

## 确认闸口（封闭）

一律按确认协议（[confirm-protocol.md](confirm-protocol.md)），不在各 skill 复制第二份规则：

| 闸口 | 说明 |
|------|------|
| wizard 定稿 | 方案落盘前；human 含强制走查（判据可检查 / 流程总览可达判据 / 交付标准无漏越界，细则见确认协议），可点名派审 |
| explore 关键 | 探索方向/范围收敛（含仅 grill） |
| design 定稿 | 方案稿可审前 |
| approve | 结构门 + 评审门 + 冻结（medium / complex 必经；simple 跳过）；human 结构门含流程总览对齐核对，可点名名册评审 |
| expand 创建 | 拆子任务前 |
| 危险类退出点 | 线上 / 泄密 / 未点名危险操作等 |

- **human**：列选项（含推荐）/ 等人确认。
- **goal**：写推荐默认 → 派审 → 收敛即放行，同轮继续。
- 线上、泄密、破坏性 git、未点名危险操作：**永不**因审阅收敛自动放行。
- 同闸口连败 2 次 → 停并升级 human，或标 `blocked`。

## Skill 归属

| Skill | 职责 |
|-------|------|
| `taskrail` | 唯一编排入口；绑定任务；推进阶段；完成门 |
| `taskrail` 确认协议（`references/confirm-protocol.md`） | human/goal 确认与审阅；退出点；质量画像字段规范 |
| `task-explore` | 台账与 explore/design/expand/approve/handoff/archive 等**命令** |
| `taskflow` | driver + propose/apply/archive；交付 checkbox |

Web UI 不依赖仓外 skill：Active Instance 由 design 阶段在交付仓内建立并 freeze，业务页由 apply 阶段按代表页 two-pass 方法实现；task* 只认指针与 digest，不复制 DS 本体。

已删除的旧 id（`task-wizard` / `task-goal` / `task-delivery`）勿再引用；统一用上表四 skill。

## 对用户说话（task 系列共用，唯一出处）

凡是直接给用户看的话——意图复述、闸口提问、进度与状态、交接 / 完成通知、评审结论摘要、subagent 摘要转述——都按这几条；落盘的内部文件与证据（`TASK.md`、`intent.md`、driver、评审文件）可以保持结构化。

- 像同事说话：第一人称、完整句子，先说结论或要用户做什么，再说原因。
- 内部术语能不用就不用；非用不可时顺带一句白话（如「driver（交付用的总任务单）」「完成判据（怎样算做完）」）。tier、criterion、gate、slice、OpenSpec、phase 等不裸露。
- 不倒「字段：值」清单、不贴原始 ID 或路径堆；路径只在用户要去看时给。
- 有问题就问一个，带上推荐；结尾说清接下来会发生什么。

前后对比：

- 闸口提问 —— 前：「gate=approve；tier=medium；criterion 待确认；P1×1」；后：「方案我觉得可以定了：按中等规模处理，做完的标准是导出 5 秒内。还有一处小风险是大文件内存占用，我建议先加个上限再动手。按这个定下来吗？」
- 进度 —— 前：「driver checkbox 3/5，slice-2 apply done，gate pending」；后：「五步里做完了三步，第二部分已经实现并通过测试。接下来做剩下两步，预计不需要你介入。」
- 评审摘要 —— 前：「roles=engineer,qa；Blocker 0；Major 2（E-1、Q-1）」；后：「工程和测试两个角度看过了，没有必须马上修的问题；有两处建议修：错误处理漏了超时、缺一条回归测试。我先把这两处补上？」

## 术语（原 glossary.md）

taskrail / task-explore / taskflow 共用；其他文件出现下列术语时按本节理解，只链接本节，不另写定义。

### 任务与阶段

| 术语 | 含义 | 不要写成 |
|------|------|----------|
| 完成判据（`criterion`） | 一条可检查的话，判断任务是否做完；原文逐字传递 | 目标、objective |
| 交付标准 | 判据之外、本任务应有的交付面要求，每条可检查；没有写「无」 | 质量目标 |
| 档位（`tier`） | simple / medium / complex，由 wizard 判定，下游不重判 | 完成程度 |
| `phase` | 契约封闭枚举 `wizard \| explore \| design \| approve \| propose \| apply \| archive \| done`；命令名不得写入 | — |
| `handed-off` | `TASK.md.status`：已交接 taskflow，任务仍在 `ongoing/`，之后进度只认 checkbox | 归档 |
| 交接载荷 | `TASK.md`「## 交接」节：判据原文、交付类别、适用门包、契约指针（Web UI 含三条 digest）；`check_handoff.py` 只认它 | 口头交接 |
| driver | OpenSpec change `{task}-driver`，只编排子 change；子 change 为 `{task}-<slice>` | 第二份任务账本 |

### 确认与审阅

| 术语 | 含义 |
|------|------|
| 完成程度 | 审阅返回的高 / 中 / 低；只有「高」且无未消 P0/P1 才收敛 |
| 退出点 | 必须停下、把决定交回人的条件（见 [confirm-protocol.md](confirm-protocol.md)） |
| 授权 | 用户明确接受某条退出点已点名的动作；单独「继续」不算 |
| 门包 | 交付类别（Web UI / 服务 / 数据 / 部署密钥 / 文档 Skill）对应的可自动化门 + 运行态证据 + 主观项 + 必载专家能力，真源 [gate-packs.md](gate-packs.md) |
| 未覆盖即降级 | 门包条目或判据任一项未验证 = 生产性降级，须登记，不得以「看起来没问题」放行 |

### 质量画像与降级状态

| 状态 | 谁能写 | 含义 |
|------|--------|------|
| `pending` | 执行者登记 | 未确认；A 类（缩判据或交付面）挂 `pending` 即停 |
| `provisional` | 审阅收敛（仅 B 类） | 临时确认，须到用户在场点追认，完成门不认 |
| `confirmed` | 只有用户 | 点名接受、全部确认或在场追认 |

评审意见 disposition 只取两值：`fixed`（已修）/ `accepted-recorded`（接受并记录理由）。Blocker / Major 无 disposition 不得收敛。字段细则见 [quality-profile.md](quality-profile.md)。

### Web UI

| 术语 | 含义 | 不要混用 |
|------|------|----------|
| Active Instance | 交付项目根 `design-system/v1` 下的设计系统实例，由 task* 的 design 阶段在交付仓内建立并 freeze | 组件约定、样式说明 |
| freeze / frozen | Active Instance 的 `status: frozen`：契约已冻结，apply 只消费不改 core | 定稿 |
| 三条 digest | contract / binding / projection 三个摘要；写入 `design/contract.md` 与 driver，用来判断是否漂移 | 版本号 |
| adopt-only | simple 档无 Active Instance 时直接沿用交付仓已有组件库 / 样式体系；须登记并确认显式降级，豁免 Active Instance，并按 gate-packs 档位调度豁免重型证据门（`ui_evidence_check` / design 评审改为 SHOULD） | — |
| 代表页 | 一条主流程的代表页面：按代表页 two-pass 方法先实现并修订，其余表面从它长出 | 旗舰切片（并行层面的概念，代表页是其 UI 产物） |
| 旗舰切片 | 命中门包时先单独派出的首个切片，做到全量并过评审后才并行 | — |
| Gallery | 交付仓内的组件 / 页面展示页证据；只证明系统未漂，不替代 `ui_evidence_check` | 截图证据 |
| `ui_evidence_check` | [`scripts/ui_evidence_check.py`](../scripts/ui_evidence_check.py)：多视口截图 + axe WCAG 2.2 AA + 焦点走查 + 四态，出 `report.json`；完成门只认它 exit 0 | 自评 |
