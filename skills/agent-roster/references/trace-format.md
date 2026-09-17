# Trace 格式

一条 Trace 一个文件：`<data_root>/agents/traces/<YYYYMMDD>-<slug>.md`。

Trace 不是日志。它是写给「下一次选人」看的，所以关键不在于发生了什么，而在于**当时为什么这么选，以及这个选择被证明对不对**。

## 模板

```markdown
# <一句话说清这次委派要做什么>

- Date: YYYY-MM-DD
- Endpoint: <host>/<kind>
- Permission: read-only | write
- Outcome: completed | failed | timeout
- Rework: 是 | 否

## 候选与选择

候选有 <...>。选了 <...>，因为 <...>。

> 从 run 目录的 `decision.md` 原样搬过来，不要重写。

## 实际结果

<产出了什么，好在哪、差在哪。返工的话写清返工了什么>

## 教训

<可复用的结论。如果只是这次的特殊情况，写明「仅此一例」，不要上升成规律>
```

## 什么时候写

只在这些情形写，例行成功不写：委派失败或超时、结果需要返工、使用者纠正了选人决定、结果明显超出预期、用了新的委派方式或新的 Endpoint。

## 从 Trace 到规则

同一条结论累积到**两次以上独立证据**，才有资格提案写进 `routing.md`，且必须由使用者确认——走 `$skill-upgrader` 的 `patches/` 审计。单次教训留在 Trace 里就够了。

如果一条结论已经脱离具体 Host 和具体任务、对任何人都成立，它就不再属于私有数据，可以脱敏后进本仓库的 `experience/patterns/`。脱敏要显式做：去掉主机名、项目名、任务细节，只留规律本身。
