# wizard 阶段

进入本阶段后执行。产出步骤级、可移交的任务方案，落盘 `wizard/plan.md`，并写入 `TASK.md` 的 `criterion` / `tier` 与「方案」节。不做详细设计、不写实现代码。

## 原则

- **先查后问**：能查到的先查；问前必给推荐答案。**禁止**空问清单（只列问题、不写推荐）。
- **步骤级颗粒度**：每步一个可执行动作，不超过 2 行，含要点与验证。
- **完成判据**：单独成节、一条可检查的话；下游按原文采用。
- **交付标准**：只取与本任务相关的交付面；无则写「无」。
- **阻塞点与坑必须显式列出**，没有写「无」。
- **简洁**：半屏内；判据、流程总览、阻塞点、建议路由不可省。
- **流程总览锚点**：「流程总览」节是从现状到完成判据的完整步骤链（只读摸底探索得出），不是示例清单——末步必须走得到判据，每步带验证点。它是后续 design / propose / apply 的对齐锚点：下游步骤不得无声偏离，偏离须写显式决策（见 taskrail 契约阶段载荷表）。
- **质量属性必问**：定稿前确认「质量属性」节已填；观感 / 性能等不可确定性度量的目标写验收方式或参照，不用「高质量」一类形容词收工。Web UI 有观感目标时，另写视觉方向与天花板参照集（[gate-packs.md](gate-packs.md)「审美目标（不分档）」）。
- **交付类别必判**：任务有交付产出时，在 `wizard/plan.md` 判定交付类别（Web UI / 服务 / 数据 / 部署密钥 / 文档 Skill），按 [gate-packs.md](gate-packs.md) 写入适用门包与**基准物**；验收方式不能只写「对照外部产品或参考实现」；外部参照可以进天花板参照集供评审对照，但不代替验收。
- **Web UI → Active Instance 前置**：交付类别为 Web UI 时，只读扫描交付项目根是否存在 `status: frozen` 的 `design-system/v1` Active Instance；将状态、根路径、contract / binding / projection digest（或「缺失」）写入 `wizard/plan.md`「Active Instance」节。缺失时写明前置动作：design 阶段建立 Active Instance 至 freeze（有参照源先提炼 tokens / primitive）；complex 在 freeze 前不得进入可批准的 design 定稿；simple 可记 adopt-only 路径但须后续显式降级。不把 DS 本体写入 `tasks/`。

## 决策收敛

落稿前把所有要人拍板的缺口写进「坑 / 注意事项」（写成「推荐=…」，勿裸问题）：

1. **需逐步授权**：线上、泄密风险、破坏性 git、删除或不可逆改写、改密钥或权限、对外发送、不可逆迁移——始终要用户逐步点名。
2. **执行前授权清单**：走完本次步骤需一次性放行的可逆、仓内、非线上动作；用户接受方案即视为已放行；未列入的一律按①处理。

方案交出后，下游只做「按此执行 / 调整哪步 / 改路由」；执行中新缺口走确认协议（[confirm-protocol.md](confirm-protocol.md)），不回流本阶段重写协议。

## 步骤

1. 意图确认：委托 `task-intent`（[../../task-intent/SKILL.md](../../task-intent/SKILL.md)），落 `wizard/intent.md`；human 模式纠偏到用户确认；goal 模式由 `role-based-reviewer roles=intent` 异源强模型代审（最多 2 轮，不过则记显式降级继续）。歧义影响走向时才问（带推荐答案）。确认版「做完的样子」是 `criterion` 的起草来源，不得无声改写。
2. 只读摸底；事实与假设分开。
3. 涉及数据写删迁或改表时，写备份与回滚路径（仅针对本次改动）；大 size / 不可回滚写入「风险点」。
4. 外部参照：读并做完 [external-precedent.md](external-precedent.md)。必做：复杂档；中等档涉及选型 / 外部集成 / 协议对接。其余跳过。
5. 按模板写 `wizard/plan.md`（含交付类别与门包节；无交付产出写「不适用」）；同步 `TASK.md`（`criterion`、`tier`、方案节）。写不出可检查判据则停，走确认协议（[confirm-protocol.md](confirm-protocol.md)）。
6. 闸口「wizard 定稿」：`criterion` 与 `wizard/intent.md`「做完的样子」一致，或在方案中写明差异；未决口子须已带推荐再交确认协议（human 三选一；goal 审阅收敛后同轮继续）。禁止空问清单。

## 输出模板

```markdown
# 任务方案：<任务名>

## 目标
<任务名 + 一句话背景>

## 完成判据
<一条可检查的话>

## 交付标准
- <…；无则写「无」>

## 交付类别与门包
- 交付类别：<Web UI / 服务 / 数据 / 部署密钥 / 文档 Skill / 不适用>
- 适用门包：<引用 taskrail/references/gate-packs.md 对应类别条目；不适用写「无」>
- 基准物：<标准 / 契约定稿 / 冻结基线——禁止外部产品或参考实现；Web UI 须含 Active Instance 路径与 digest>
- 未覆盖即降级：<按显式降级登记，含 A/B 定级与证据要求>

## Active Instance（仅 Web UI；其它类别写「不适用」）
- 状态：<frozen / 缺失 / adopt-only 候选>
- 根路径：<交付项目根下 Active Instance 目录；缺失写「无」>
- contract digest：<…或无>
- binding digest：<…或无>
- projection digest：<…或无>
- 前置动作：<已就绪 / design 阶段建立 Active Instance 至 freeze / simple 拟 adopt-only + 显式降级>

## 前提
- 事实：…
- 假设：…

## 质量属性
- <与本任务相关的质量目标：观感 / 性能 / 可靠性 / 可维护性…；不可确定性度量的写验收方式或参照；不适用写「不适用」+ 原因>

## 流程总览
1. <动作> — 要点：…；验证：…；从现状探索得出，末步走得到判据，全程无断点>

## 阻塞点
- <…；无则写「无」>

## 坑 / 注意事项
- <含①②授权清单；无则写「无」>

## 风险点
- <…；无则写「无」>

## 不做的事
- <…>

## 建议路由
<简单 / 中等 / 复杂 + 一句话理由>
```

## 复杂度档位

先看复杂：命中任一条即复杂。`tier` 取值 `simple` / `medium` / `complex`（中文呈现可用 简单/中等/复杂）。

| 档位 | 典型 | wizard 之后 |
|------|------|-------------|
| 简单 | 局部修改 | 直接实现 + 验证（不建 driver）→ done |
| 中等 | 跨模块/仓库、改动量稍大 | explore(仅 grill) → design(可轻) → approve → handoff → propose → apply → archive |
| 复杂 | 项目级重构、逻辑重塑、涉及面广 | explore(+grill) → design → approve → handoff → propose → apply → archive |

- 产品交付硬指标命中即复杂：多主页面；两以上角色/权限边界；持久化跨请求/用户复用；外部集成/实时协作/通知/审计；项目级重构。单组件、单页原型、无持久化静态演示不触发。
- 跨模块/仓库本身是中等；同时属项目级重构等则升复杂。
- 简单与中等拿不准且未命中复杂：往简单靠一档并说明。
- 有任务目录时 grill 委托 `grilling`，纪要可落 `explore/`；禁止在任务目录路径调用 `grill-with-docs` / `domain-modeling`（会写仓库根文档）。无台账的一次性拷问才用 `grill-with-docs`（两跳 `grilling` + `domain-modeling` 逐字保留）。
- 委托前确认 skill 可读；不可用则报告安装选项，不发明等价命令。
