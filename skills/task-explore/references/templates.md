# 落盘模板（TASK.md / INDEX.md / design）

<!-- 原 task-template.md -->
# 任务文档骨架

`new` 时按此创建 `{taskRoot}/TASK.md`。按已知信息填写，未知留空，不要编造。元信息字段见 [../../taskrail/references/contract.md](../../taskrail/references/contract.md)。**输入含现成方案时（含上游 taskrail wizard 的流程总览方案、他人设计稿），把目标、完成判据、事实、假设、质量属性、流程总览、阻塞点、坑逐条登记进「方案」小节**，不要只填目标。输入里没有完成判据时不要编造。**输入含质量画像或显式降级时（上游 taskrail 确认协议 / 复杂档），在同一小节逐字登记原文快照**，不概括、不改写、不换成路径或小节指针；输入里没有画像或降级时删去对应行，不要编造。

`save` 时更新同一文件：改 `updated` 与有变化的章节，不要整文件重写后丢掉仍有效的内容。同时同步 `tasks/INDEX.md` 对应行（标题、日期、一句话目标），不要把进展抄进索引。

```markdown
# <Title>

- slug: <task-name>
- parent: <父任务 slug；仅子任务保留此行，顶层任务删除>
- status: ongoing
- phase: wizard  # 仅允许：wizard|explore|design|approve|propose|apply|archive|done；禁止 chat/handoff/save 等命令名
- confirm_mode: human
- tier: <simple | medium | complex；未知可暂空>
- criterion: <完成判据原文；没有则留空，不要编造>
- driver: <handed-off 后填写>
- evidence_root: <仓外证据根；无则删本行>
- created: YYYY-MM-DD
- updated: YYYY-MM-DD

## 目标

- [要达成什么]

## 非目标

- [明确不做的]

## 现状

[已知事实、已读材料、约束。链到代码或文档路径。]

## 方案

[上游或已有方案；无则留空。已定则写全，未定则写下当前候选与缺口。]

- 完成判据：[输入里的那一条可检查的话；没有则删去本行，不要编造]
- 质量画像原文快照：[上游 taskrail 确认协议 复杂档含画像时逐字登记，`角色底线` 三条一并带上；没有则删去本行，不要编造]
- 显式降级原文快照：[逐字登记每条「维度 / 默认期望 / 实际选择 / 原因 / 确认状态」，`pending` 原样保留；没有则删去本行]
- 事实：[对上出处的现状或外部参照；没有则删去本行]
- 假设：[未对上出处的，含未找到的外部参照；没有则删去本行]
- 质量属性：[观感 / 性能 / 可靠性 / 可维护性等；不可确定性度量的写验收方式或参照；不适用写原因；没有则删去本行]
- 流程总览：[每步动作 — 要点 / 验证；末步走得到判据]
- 阻塞点：[会卡住整个方案的事，或「无」]
- 坑：[易踩的坑、隐性依赖、顺序敏感点，或「无」]

## 进展

- YYYY-MM-DD：[本轮结论，一条一事]

## 已做决定

唯一的决定清单：意图确认、grill、design、各闸口和实现中定下的决定都追加到这里，不在别处另记。

| # | 决定 | 理由 | 可逆 | 来源阶段 |
|---|------|------|------|----------|
| D-1 | [定了什么] | [一句为什么] | 是 / 否 | wizard / explore / design / approve / apply |

- 带进实现的未决：[列表，或无]
- 回退：[选错了怎么撤]

## 交接

- driver: `{task-name}-driver`（handoff 后填写）
- 质量画像 / 显式降级原文快照：[上游复杂档带画像时，handoff 时从「方案」小节逐字复制；没有则删去本行]
- 归档路径：[handoff / archive 后填写]

## 子任务

- [仅父任务保留本小节，子任务删除] `{sub}` — [一句话方向]（状态，YYYY-MM-DD 创建）

## 未决问题

- [ ] [还不知道的]

## 下一步

- [explore / chat / design / approve / handoff / archive / 其它]
```

归档前把 `status` 改为 `archived`，元信息加上 `archived: YYYY-MM-DD`，并按 `references/archive-reopen.md` 写 **归档** 小节（本次结论、关闭原因、未决清点、交付侧现状、入链结果），并在同目录写 `SUMMARY.md`（给人读的时间线总结，骨架见 `references/archive-reopen.md`）。handoff 成功后把 `status` 改为 `handed-off`，加上 `handed-off: YYYY-MM-DD` 与 `driver: {task-name}-driver`（任务留在 `ongoing/`，不搬目录）。status 取值：`ongoing` / `handed-off` / `blocked` / `done` / `archived`。`reopen` 后 `status` 回 `ongoing`，保留 `archived: YYYY-MM-DD` 作历史并加 `reopened: YYYY-MM-DD`。


<!-- 原 index-template.md -->
# 任务索引骨架

`tasks/INDEX.md` 是派生目录。单任务真相在各 `TASK.md`。`new` / `save` / `decide` / `handoff` / `archive` / `reopen` 时改对应行；漂移则按目录重建。

Ongoing 按 `updated` 新到旧；Archived 按归档日新到旧。一句话取目标首条，不要抄进展日志。`handed-off` 行（含子任务）以 `→ {task-name}-driver` 结尾；父任务行一句话聚合子任务状态（如「2 子任务：1 已交接、1 设计中」）。子任务的任务列写 `{parent}/{sub}`、路径列写嵌套路径；父归档整树搬家后子任务行路径批量更新为新位置。

```markdown
# Tasks

派生索引。编辑单任务请改对应 `TASK.md`，然后 `save`。

## Ongoing

| 任务 | 标题 | 更新 | 一句话 | 路径 |
|------|------|------|--------|------|
| gateway-timeout | 网关超时排查 | 2026-09-15 | 查清 5xx 来源 | `ongoing/gateway-timeout/` |
| big-quest/api-style | 接口风格子任务 | 2026-09-20 | 定 REST 还是 RPC | `ongoing/big-quest/api-style/` |

## Archived

| 任务 | 归档日 | 标题 | 一句话 | 路径 |
|------|--------|------|--------|------|
| quota-alert | 2026-09-01 | 配额告警误报 | 确认阈值与静默窗口 | `archive/2026-09-01/quota-alert/` |
| session-auth | 2026-09-15 | 会话方案 | 已决：服务端 session → session-auth-driver | `archive/2026-09-15/session-auth/` |
| big-quest/auth | 2026-09-21 | 认证子任务 | 已交接：服务端 session → auth-driver | `archive/2026-09-21/big-quest/auth/` |
```

没有进行中或已归档任务时，保留表头，表体不写占位行。


<!-- 原 design-template.md -->
# 设计文档骨架

`design` 阶段脚手架。按问题裁剪，不是每节都必填。

只写入 `<taskRoot>/design/`（`tasks/ongoing/{task-name}/design/`）。不要写到仓库 `docs/design/` 或 OpenSpec change 目录。

---

# <Title>

> 一段话：做什么、为什么、选哪条路。

## Context

- **Problem**: [要补的缺口]
- **Stakeholders**: [谁关心、谁能卡住、谁受益]
- **Success criteria**: [怎样算做成]
- **Constraints**: [技术、业务、时间、团队、合规]
- **Out of scope**: [本设计明确不做的]

## Current State

现状简述。链到已有文档、ADR、代码路径。标出必须契合的既有模式。

## 外部参照

这一轮追的做法。每条写一句话做法和公开出处，并写明采信了哪一条。未找到则写明缺什么。同一问题已有仍对得上的出处时，摘录已有条目。

## Options Considered

| Option | Cost | Risk | Reversibility | Time | Complexity |
|--------|------|------|---------------|------|------------|
| A      |      |      |               |      |            |
| B      |      |      |               |      |            |
| C      |      |      |               |      |            |

每个选项 1–3 行说明。

## Recommended Approach

**Recommendation: Option X**，因为 [主因]。

接受的取舍：

- [trade-off 1]
- [trade-off 2]

回退计划：[选错了怎么撤]。

## 设计依据

每个架构 / 接口 / 技术栈选择一行：`选择 → 模式 / 原则 → 为何适用 → 可检后果`。

- [选择] → [模式 / 原则] → [为何适用] → [少了什么：耦合面 / 接口面 / 重复 / 可替换点 / 可测性 / 回归面]
- 不引入模式的选择：[选择] → 当前做法，理由 […]
- 本任务不涉及这三类选择：「不适用」+ 一句原因

## Architecture

```
┌──────────────────────────────────────────────┐
│     ASCII or Mermaid diagram of the system   │
└──────────────────────────────────────────────┘
```

- **Component A**: [职责]
- **Component B**: [职责]
- **Data flow**: [请求 / 事件 / 状态传播]

## Interfaces

### API / message contracts

```
<Type or schema sketch>
```

### Key types

```pseudo
struct Foo { ... }
```

## State Management

- Where state lives: [DB / cache / in-memory / external]
- State transitions: [如有状态机]
- Consistency model: [strong / eventual / read-your-writes]

## Failure Modes

| Failure | Likelihood | Impact | Mitigation |
|---------|------------|--------|------------|
| [scenario] | low/med/high | [blast radius] | [handling] |

## Rollout / Migration

若改动已有系统：

- Phase 1: [shadow / dark launch / feature flag]
- Phase 2: [gradual rollout]
- Phase 3: [full migration + cleanup]

## Open Questions

- [ ] [仍未决]
- [ ] [需要的 spike]

## Cross-References

- **Related designs**: [兄弟文档]
- **Task doc**: `../TASK.md`
- **Downstream**: [本设计解锁的下一步，通常是 save / chat；实现须用户明确要求]
