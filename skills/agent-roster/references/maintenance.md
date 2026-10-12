# 留痕、固化与名册维护

## 留痕：什么时候写 Trace

只在以下情形写，例行成功不写——否则有用的教训会被「派给 X，成功」淹没：

- 委派失败、超时，或结果需要返工
- 使用者纠正了选人决定
- 编排者自己绕过了流程：自任受派方，或越过门禁的等待继续推进
- 结果明显超出预期
- 用了新的委派方式或新的 Endpoint

字段见 [references/trace-format.md](trace-format.md)。其中「为什么选它」是唯一能在将来固化成 Routing Rule 的东西，必须从 `decision.md` 原样搬过来，不要重写。

## 固化：什么时候把案例变成规则

攒着不用的 Trace 只是历史。固化（Promotion）是唯一能让选人变准的动作，而它不会自动发生——必须有人在固定时刻检查。

**时机**：写完一条 Trace 之后立即检查，其他时候不查。尤其不要在路由途中插入这个判断，那时候使用者在等结果。

检查用 `scripts/promotion_check.py`（同一句「为什么选它」跨 Trace 精确计数，达门槛打印提案草稿）；脚本只负责把「没人去数」补上，提案与写入仍走下面的确认门禁。

**门槛**：同一个「为什么选它」的理由，在**不同任务**的 Trace 里复现两次以上。不是「同类任务攒够几条」——Trace 只在有教训时才写，按任务分类计数永远凑不齐。这个 2 和 `experience/patterns/` 的准入门槛是同一个数，不用记两套。

**动作**：攒够了就停下来向使用者提案，说清是哪几条 Trace、复现的是哪句理由、建议写成什么规则。使用者确认后按去向分两条路：

- 规则带 Host 名、只对当前使用者成立 → 直接写进 `routing.md`。
- 结论已脱敏、换台机器换个项目仍然成立 → 走 `$skill-upgrader` 的 `patches/` 审计，进本文件正文或 `patterns/`。

分野的理由（源仓 ADR 0003）：带 Host 名的规则随名册走私有数据，脱敏结论才进公开仓。攒够了却不提案，和凭空编规则一样有害：前者让系统永远停在现读现判，后者让它学到假的东西。

## 名册维护

```bash
python3 <skill-dir>/scripts/probe_endpoints.py            # L1：装没装、什么版本
python3 <skill-dir>/scripts/probe_endpoints.py --level 2  # L2：ACP 适配器能不能握手
python3 <skill-dir>/scripts/probe_endpoints.py --render   # 输出可粘贴的 Markdown 状态块
python3 <skill-dir>/scripts/probe_endpoints.py --write    # 直接回填画像「探测状态」段（L3 记录永不被挤掉）
```

探测分三层，失败时要能区分三种完全不同的处置：

1. **L1 存在性** — CLI 在不在 PATH、什么版本。零成本，随时可跑。
2. **L2 握手** — 起 ACP 适配器走完 `initialize` 就断开。零 token，能确认适配器真的拉得起来。
3. **L3 冒烟** — 真发一句 prompt，确认登录态、额度与模型可用。花钱花时间，手动触发，脚本不做。

探测只回填 Endpoint 文件的客观状态段，**Disposition 归人维护**，格式见 [references/endpoint-schema.md](endpoint-schema.md)。

第一版只探测本机。远端 Host 的 Endpoint 可以手工登记，但跨机执行不在范围内。
