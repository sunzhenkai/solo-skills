# wizard 阶段

产出步骤级、可交给下游的方案：落 `wizard/plan.md`，写 `TASK.md` 的 `criterion` / `tier` 与「方案」节。不做详细设计、不写代码。

子任务（`TASK.md` 有 `parent:`）跳过第 1 步，意图沿用父任务（[large-scope.md](large-scope.md)「推进子任务」）；第 7 步不停，说决定接着做。

## 步骤

1. **意图**：按 [intent.md](intent.md) 探索并起草复述，落 `wizard/intent.md`（`status: draft`，第 7 步确认后改 `confirmed`）。复述先不单独发，到第 7 步和 plan 要点一起说。确认版「做完的样子」是 `criterion` 的起草来源，改它只走契约「意图变更」。
2. **补实现入口**：复用 `evidence/intent/` 的摸底，只补写步骤需要的实现入口（模块、文件、命令），已读过的资料不重读。
3. **写 plan**：按下方模板；同步 `TASK.md`。写不出可检查判据就按 [user-report.md](user-report.md) 第 5 节「卡住」停，说清缺什么。
4. **定档**：局部修改、一句话说得清 → `skip`；其余 → `full`（契约「流程」）。定为 `full` 时当场查执行条件：`openspec` CLI 与 `openspec-*`、`taskflow` skill 可用，修改仓是 git 仓，planning root 有 `openspec/` 根。缺 skill 或 CLI 就说怎么装；没有 `openspec/` 根，把「交接前在该仓跑 `openspec init --tools none`」写成一条决定，放进第 7 步的消息。
5. **拆分（仅 `full`，默认不拆）**：一个 driver 一次做完就能验判据的，不拆，这一步不留痕迹。要分几块做时按 [large-scope.md](large-scope.md) 定切片还是子任务，把路线图写进 plan：每项一句话目标、子判据、依赖。
6. **（full 档可选）外部参照**：方案依赖选型 / 外部集成 / 协议对接时，按 [external-precedent.md](external-precedent.md) 查一次。
7. **定稿闸口**：`criterion` 与「做完的样子」一致（不一致就写明差异）。把意图复述和 plan 要点（判据、步骤、档位；拆了再加路线图，一行一项）合成一条消息，按 [confirm-protocol.md](confirm-protocol.md)「停点」表放行；意图纠偏在这一步进行。

## 写法

- 每步一个可执行动作，不超过两行，带验证点；末步走得到判据。下游 design / apply 按这些步骤走，偏离就写进「已做决定」。
- 有歧义就按推荐写成决定带理由，不留裸问题。
- 涉及数据写删迁或改表：写备份与回滚路径；这类动作本身按真阻塞停（[user-report.md](user-report.md) 第 5 节）。
- 观感类目标加一条验收（[done.md](done.md)「观感验收」）；Web UI 交付读 [ui-delivery.md](ui-delivery.md)。

## `wizard/plan.md` 模板

必填四节；其余按需加，没有就不写。

```markdown
# 方案：<任务名>

## 目标
<一句话背景 + 要达成什么>

## 完成判据
<一条可检查的话>

## 步骤
1. <动作> — 验证：<怎么确认这步做成>

## 不做
- <只来自用户原话的限制；自己想加的写进「假设」>

<!-- 按需：路线图 / 交付标准 / 交付类别 / 质量属性（观感方向与参照）/ 事实与假设 / 风险与回滚 -->
```

拆了才加「路线图」节，格式与三条要求见 [large-scope.md](large-scope.md)「路线图」：

```markdown
## 路线图
| 项 | 类型 | 目标 | 子判据 | 依赖 |
|---|---|---|---|---|
| <slice 或 sub> | 切片 / 子任务 | <一句话> | <可检查的一句> | <项名或 —> |
```

`check_handoff.py` 要求交接时写「交付类别」「适用门包」两行；plan 里有交付产出时顺手写上类别（Web UI / 服务 / 数据 / 部署 / 文档 Skill / 不适用），门包按 [quality-appendix.md](quality-appendix.md) 的类别名，或写「无」。
