# wizard 阶段

产出步骤级、可交给下游的方案：落 `wizard/plan.md`，写 `TASK.md` 的 `criterion` / `tier` 与「方案」节。不做详细设计、不写代码。

## 步骤

1. **意图**：委托 `task-intent` 落 `wizard/intent.md`。确认版「做完的样子」是 `criterion` 的起草来源，不得无声改写。
2. **只读摸底**：先查一手资料；事实与假设分开写。
3. **写 plan**：按下方模板；同步 `TASK.md`。写不出可检查判据就停，按 user-report 说清缺什么。
4. **定档**：局部修改、一句话说得清 → `skip`；其余 → `full`（契约「流程」）。
5. **（full 档可选）外部参照**：方案依赖选型 / 外部集成 / 协议对接时，按 [external-precedent.md](external-precedent.md) 查一次。
6. **定稿闸口**：`criterion` 与「做完的样子」一致（不一致就写明差异），按 [confirm-protocol.md](confirm-protocol.md) 放行。

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

<!-- 按需：交付标准 / 交付类别 / 质量属性（观感方向与参照）/ 事实与假设 / 风险与回滚 -->
```

`check_handoff.py` 要求交接时写「交付类别」「适用门包」两行；plan 里有交付产出时顺手写上类别（Web UI / 服务 / 数据 / 部署 / 文档 Skill / 不适用），门包按 [quality-appendix.md](quality-appendix.md) 的类别名，或写「无」。
