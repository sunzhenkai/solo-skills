# 示例：程序化广告系统 Atlas

本例使用虚构的全链路广告平台，展示如何用“系统总览 + 主链路 + 多视角 + 领域下钻”组织复杂系统。它是一份内容示例，不对应真实公司、产品或源码；实际 Atlas 中的路径和结论须由目标项目证据核实。

## 1. 建议落点

```text
docs/atlas/
├── index.md
├── flows/
│   ├── ad-request.md             # 请求到曝光、计费与反馈
│   ├── campaign-launch.md        # 创建到审核、投放与预算生效
│   └── conversion-attribution.md # 转化回传到归因与模型反馈
├── architecture/
│   ├── online-serving.md         # 在线服务、依赖与故障传播
│   └── offline-learning.md       # 离线数据、训练与模型发布
├── data/
│   ├── budget-state.md           # 预算读写、扣减与一致性
│   └── event-stream.md           # 请求、曝光、点击、转化事件
├── cross-cutting/
│   ├── experiment-and-pacing.md  # 实验分流与平滑投放
│   └── privacy-and-fraud.md      # 隐私约束与反作弊
└── domains/
    ├── traffic/index.md          # 流量接入、请求规范化
    ├── campaign/index.md         # 计划、创意、定向与审核
    ├── decision/index.md         # 召回、预估、出价与竞价
    ├── delivery/index.md         # 预算、频控、曝光与计费
    ├── measurement/index.md      # 监测、归因与报表
    └── learning/index.md         # 样本、训练、评估与发布
```

## 2. `index.md` 示例

```markdown
---
title: 程序化广告系统
level: 0
status: draft
sources: []
source_digest:
verified_commit:
---

# 程序化广告系统

## 系统边界

本平台连接广告主、流量方和用户：把广告主的投放目标与预算转化为实时竞价决策，完成广告展示、计费、效果度量，并利用合规的反馈数据优化后续决策。

平台覆盖流量接入、投放配置、在线决策、交付控制、效果度量和模型学习。创意制作工具、广告主资金清算和流量方财务付款属于外部系统，本平台通过接口与其协作。

## 参与者与价值

| 参与者 | 提供 | 获得 |
|---|---|---|
| 广告主 | 投放目标、预算、创意、定向约束 | 合规曝光、转化与效果报告 |
| 流量方 | 广告请求、可用版位与流量约束 | 广告收益与填充率 |
| 用户 | 符合隐私规则的上下文与交互 | 与场景相关的广告内容 |
| 运营人员 | 审核、实验和异常处置策略 | 可控的投放与审计能力 |

## 业务闭环

广告请求进入后，系统依次完成流量规范化、候选召回、效果预估、出价竞价、预算与频控校验，再返回获胜创意。曝光和点击事件驱动计费、报表与反作弊；合规转化进入归因和样本生成，模型评估与发布再影响后续召回和出价。

    投放配置 → 在线请求 → 决策竞价 → 曝光计费 → 转化归因 → 样本训练 → 模型发布
        ↑                                                                      ↓
        └──────────────────── 投放策略与预算调整 ←─────────────────────────────┘

## 按目标阅读

| 我想…… | 阅读路径 |
|---|---|
| 理解一次广告如何展示和计费 | [广告请求主链路](flows/ad-request.md) → [在线决策](domains/decision/index.md) → [交付控制](domains/delivery/index.md) |
| 理解预算为什么超投或停投 | [预算状态](data/budget-state.md) → [交付控制](domains/delivery/index.md) → [实验与平滑投放](cross-cutting/experiment-and-pacing.md) |
| 排查在线延迟或局部故障 | [在线服务架构](architecture/online-serving.md) → [广告请求主链路](flows/ad-request.md) → 对应领域页 |
| 理解模型如何影响线上决策 | [转化归因主链路](flows/conversion-attribution.md) → [离线学习架构](architecture/offline-learning.md) → [模型学习](domains/learning/index.md) |
| 修改投放或计费规则 | [投放计划](domains/campaign/index.md) → [交付控制](domains/delivery/index.md) → [广告请求主链路](flows/ad-request.md) |

## 多视角导航

### 主链路

- [广告请求：从流量到反馈](flows/ad-request.md)（首批）
- [投放计划上线](flows/campaign-launch.md)（draft）
- [转化归因与模型反馈](flows/conversion-attribution.md)（draft）

### 架构

- [在线服务架构](architecture/online-serving.md)（首批）
- [离线学习架构](architecture/offline-learning.md)（draft）

### 数据与状态

- [预算状态与一致性](data/budget-state.md)（首批）
- [广告事件流](data/event-stream.md)（draft）

### 横切机制

- [实验与平滑投放](cross-cutting/experiment-and-pacing.md)（draft）
- [隐私与反作弊](cross-cutting/privacy-and-fraud.md)（draft）

### 领域

- [流量接入](domains/traffic/index.md)
- [投放计划](domains/campaign/index.md)
- [在线决策](domains/decision/index.md)
- [交付控制](domains/delivery/index.md)
- [效果度量](domains/measurement/index.md)
- [模型学习](domains/learning/index.md)

## 当前覆盖

首批只保证“广告请求 → 曝光计费”的主链路及其在线架构、预算状态可下钻。投放上线、归因、离线学习和横切策略仍为 draft；外部财务结算不在本期 Atlas 范围内。
```

## 3. `flows/ad-request.md` 内容示例

主链路页写清跨领域顺序，每一步只保留业务结论；内部算法和状态机下钻到领域页。

```markdown
---
title: 广告请求：从流量到反馈
level: 1
status: draft
sources:
  - src/serving
  - src/delivery
  - src/events
source_digest:
verified_commit:
---

# 广告请求：从流量到反馈

## 业务前提

流量方已接入并取得合法请求授权；广告计划与创意已审核生效；请求携带的上下文满足流量约束与隐私策略。

## 端到端步骤

| 步骤 | 责任领域 | 输入 → 输出 | 关键规则 |
|---|---|---|---|
| 1. 接入请求 | [流量接入](../domains/traffic/index.md) | 原始请求 → 标准广告机会 | 校验版位、设备上下文与流量约束 |
| 2. 匹配投放 | [投放计划](../domains/campaign/index.md) | 广告机会 → 可投计划与创意 | 仅选择审核通过且在投放期内的候选 |
| 3. 在线决策 | [在线决策](../domains/decision/index.md) | 候选与模型特征 → 排序和出价 | 在延迟预算内完成召回、预估和竞价 |
| 4. 交付校验 | [交付控制](../domains/delivery/index.md) | 获胜候选 → 可交付创意 | 原子校验预算、频控和必要的频控占用 |
| 5. 返回展示 | [流量接入](../domains/traffic/index.md) | 创意与监测信息 → 广告响应 | 超时或无合适候选时返回无填充 |
| 6. 事件计量 | [效果度量](../domains/measurement/index.md) | 曝光/点击事件 → 计量与报表事实 | 去重、反作弊并按归属口径计费 |
| 7. 反馈学习 | [模型学习](../domains/learning/index.md) | 合规事件与转化 → 样本和候选模型 | 评估通过后发布，反馈影响后续决策 |

## 运行时与数据证据

- 同步调用、超时预算和降级路径见[在线服务架构](../architecture/online-serving.md)。
- 预算预留、确认与释放见[预算状态与一致性](../data/budget-state.md)。
- 请求、曝光、点击、转化的事件关系见[广告事件流](../data/event-stream.md)。

## 关键失败路径

- **决策超时**：终止低优先级计算并返回无填充或已缓存的合规候选，不绕过预算校验。
- **预算不足**：候选不可交付，继续选择其他候选或返回无填充。
- **展示成功但事件延迟**：在线响应不回滚；计量侧按事件去重和迟到规则补偿。
- **重复曝光事件**：保留原始事件用于审计，计费事实只确认一次。

## 业务结果

一次请求以“无填充”或“返回创意”结束；只有符合计量规则的曝光、点击和转化进入计费、报表与学习反馈。失败路径不得产生未经确认的计费事实。

[返回系统总览](../index.md)
```

## 4. 这份示例如何使用

在真实项目中先实现 L0 和一条最有价值的主链路，再补该链路涉及的领域、架构和数据页。示例中的“首批”是最小可读闭环，不代表已覆盖整个广告系统；每项结论都要替换为目标项目证据，并通过 `verify`、`build` 和 `check`。
