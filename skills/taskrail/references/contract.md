# taskrail 契约（阶段 / 载荷 / 闸口 / 目录）

本文件是 task* 族重组后的**唯一真源**。`taskrail`（含确认协议 [confirm-protocol.md](confirm-protocol.md)）/ `task-explore` / `taskflow` 与本文有出入时，以本文为准（术语定义见 [glossary.md](glossary.md)）；各 skill 正文只写执行细则，不另造阶段枚举。

## 流程

```text
confirm_mode: human | goal

wizard → explore(+grill) → design → approve → [handoff] → propose → apply → archive
         ↑ expand 可插在 explore / design 之后
         ↑ handoff = 动作，不是 phase
```

| 档位 (`tier`) | 路径 |
|---------------|------|
| simple | wizard → explore(仅 grill) → approve(轻) → handoff → propose(单切片) → apply → archive |
| medium | wizard → explore(仅 grill) → design(可轻) → approve → handoff → propose → apply → archive |
| complex | wizard → explore(+grill) → design → approve → handoff → propose → apply → archive |

简单/中等是**跳过**中间阶段（simple 跳过 design；simple/medium 的 explore 仅为 grill），不是另一套 skill。

### simple 专条

- 凡经 `taskrail` 的任务（含 simple）必须 `handoff` + taskflow：建 `{slug}-driver`，走 propose → apply → archive。
- `propose(单切片)`：driver 实施段默认仅 1 个子 change（或等价单切片编排），进度仍只认 checkbox。
- **禁止**在 taskrail 路径下无 driver 直接改业务代码。用户明确拒绝 OpenSpec → **退出 taskrail**，改直接实现（与 task-explore「何时不用」一致），不在本轨道开无账本分支。

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

1. 重跑 `task-intent`，产出新版本（`wizard/intent.md` 的 `version` +1，旧版移入「历史版本」节，不删）。
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
│   ├── wizard/intent.md         # task-intent 确认版（含 version / 历史版本）
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
- `handed-off` 只表示账本已换到 taskflow，**不等于** `done`。
- `done` 仅当完成判据成立且交付标准全过（复杂档另要求质量画像齐全、降级无 `pending`/`provisional`）。

### status × phase 合法组合

| status | 允许的 phase |
|--------|----------------|
| ongoing | wizard, explore, design, approve |
| handed-off | propose, apply, archive |
| blocked | 停在进入 blocked 时的 phase（上表该 status 原允许集合内） |
| done | done |
| archived | archive 或 done（目录已迁 `tasks/archive/`） |

## 阶段载荷契约

阶段跳转必须带齐；缺则停在上一 `phase`，禁止下游猜意图：

| 进入阶段 | 必须已有 |
|----------|----------|
| explore / design | `wizard/intent.md`（`status: confirmed` 或 `assumed`；本规则生效前的旧任务缺失不回溯）+ `criterion` + `wizard/plan.md`（或 TASK.md「方案」节等价正文，含流程总览与质量属性节；有交付产出时含交付类别与适用门包节；Web UI 另含 Active Instance 状态节） |
| design | 流程总览映射：设计步骤 ↔ 总览步骤逐条对齐；新增 / 删改 / 改序写显式决策，供 approve 结构门核对；命中门包时产出**契约文件指针**（仓库内已冻结的共享面契约）与证据计划；Web UI 指针必须含 Active Instance 根路径与三条 digest（档位门见 gate-packs） |
| approve | design 产出路径（或简单档的 plan / explore 纪要）+ `criterion` + 「不做的事」；命中门包时另附交付类别、适用门包与基准物；Web UI：medium/complex 须 digest 与仓库 freeze 一致才可冻结；simple 无 freeze 仅当 adopt-only + 已确认显式降级 |
| propose（经 handoff） | `approve/APPROVED.md`（或 TASK.md 决策节已冻结）+ 判据原文；复杂档含质量画像与显式降级原文快照；流程总览快照随交接进 driver；命中门包时门包与契约文件指针一并进 driver（Web UI 含三条 digest）；`status: handed-off` 与 `driver` 已写入；`TASK.md`「## 交接」含「交付类别」「适用门包」行，`taskflow/scripts/check_handoff.py` exit 0 |
| apply | driver `tasks.md` 已由 propose 产出 |
| archive（探索侧） | 用户确认关闭；子任务均已结 |

## 执行座位

高噪声 legwork **默认**交给 worker（同机通道抽象为**宿主 subagent**，不绑具体 Tool；点名 Endpoint 时走 `agent-roster`），不新增 `phase`，不改变闸口与完成门。目的：并行提速、主会话上下文不被工具轨迹污染。

**默认派出，能力缺失可自做。** 宿主无 subagent、或派出失败 → 主会话按同一落点与完成标准自做，**不得**因缺少派出能力停下或改道；有能力却不派时，在 `TASK.md` 进展里写一句理由。

| 单位 | simple | medium / complex |
|------|--------|------------------|
| wizard 意图摸底（task-intent） | 1 个（跳过条件见 task-intent「何时跳过」） | 2–3 / 3–4 个并行 |
| explore | worker 摸底；grill 提问留主会话 | worker（调研 / 起草；grill 提问与闸口留主会话） |
| design | （跳过） | worker |
| apply | worker | worker（并行与实现者输入见 taskflow） |
| 评审 / 验证复跑 | worker | worker（按角色并行，见 role-based-reviewer） |

**不派**：闸口（确认协议）、危险退出、面向用户的提问与选项；一句话能说清或预计改动 <30 行的活；强依赖主会话上下文、拆不开的步骤。同一批可并行的单位一次性发出；simple ≤1、medium ≤3、complex ≤5 个。

**交接契约（5 项，缺一不派）**：① 目标（一句话要回答 / 完成什么）；② 输入路径；③ 写入范围（apply 含 change 范围内业务代码；其余默认只读 + 落盘路径）；④ 输出格式（Digest）；⑤ 停止条件。apply 的实现者输入只引用 taskflow `implementer-isolation`，不另列。

**Digest（≤10 行）**：结论 / 落盘路径 / 未决 / 置信度。详情落盘，主会话只收 Digest，不回灌工具轨迹、不转贴全文；产物缺失则停在当前 `phase`。`TASK.md` 的 `phase` / `status` / `driver` 仅编排者写；OpenSpec checkbox 由执行 `openspec-apply-change` 的一方按协议勾，编排者回收时核对。

## 确认闸口（封闭）

一律按确认协议（[confirm-protocol.md](confirm-protocol.md)），不在各 skill 复制第二份规则：

| 闸口 | 说明 |
|------|------|
| wizard 定稿 | 方案落盘前；human 含强制走查（判据可检查 / 流程总览可达判据 / 交付标准无漏越界，细则见确认协议），可点名派审 |
| explore 关键 | 探索方向/范围收敛（含仅 grill） |
| design 定稿 | 方案稿可审前 |
| approve | 结构门 + 评审门 + 冻结（必经；简单档可轻量）；human 结构门含流程总览对齐核对，可点名名册评审 |
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
