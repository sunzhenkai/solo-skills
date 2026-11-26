# design：契约、结构、兼容性与迁移

## 目的
为契约或结构变化给出可实施、可回退、可验证的方案。

## 进入条件
涉及大型项目 / 新建子系统、公共或内部接口、数据模型、架构依赖、大范围跨模块重构、复杂迁移、跨模块共享面，或实现会改变重要兼容行为。

## 跳过条件
完全沿用现有模式且没有契约 / 结构变化。grill 不是固定前置；只有存在关键取舍时先走 [grill.md](grill.md)。

## 所需输入
criterion、当前 plan、explore / diagnose 证据和已解决的 grill 决定。

## 执行方法
1. 写清现状证据、模块接缝（seam）与目标契约（优先深模块：小接口隐藏复杂实现，先钉死测试面——在公开接口测行为，不为单一实现造假想接缝；跨边界依赖按进程内 / 本地替身 / 自有远端 Ports & Adapters / 外部 Mock 分类，可选按 `codebase-design` 深化接口）、边界、兼容性、回滚和验证策略。
2. 推荐与被放弃方案各写取舍；仅当决定同时满足「难逆 + 无上下文会困惑 + 存在真实权衡」三条件时写极简 ADR（1–3 句讲清背景、决定与理由即可）并按 [user-report.md](user-report.md) 告知；涉及领域术语变更时按 `domain-modeling` 实时维护项目 `GLOSSARY.md` 并当场澄清冲突命名。
3. 多仓库共享契约放父任务 design，子任务只放自己的实现设计；不在每个子任务复制完整上下文。
4. 未就绪后续项只写边界与接口，细节轮到它时按当时代码补；`design/<topic>.md` 的未决节只列 `U-n / F-n` 与指针，问题详情由 `context/current.md` 维护。
5. 涉及跨项目通用接入或已沉淀模式先查 `project-design-patterns`（未装跳过）；Web UI 按需读 [ui-delivery.md](ui-delivery.md)；多方案对比 / 两次设计见下文「方案细则」。
6. 落盘后、开工前按 `anti-lazy` 核对用户决策边界与目标差距，按 [user-report.md](user-report.md) 整理人话摘要并交 [approve.md](approve.md) / [confirm-protocol.md](confirm-protocol.md) 放行。

## 产出
`design/README.md` 索引、`design/<topic>.md`、按需 ADR / contract / glossary；decisions 写决定。

## 完成门
接口与依赖明确，兼容 / 回滚可走，验证能覆盖 criterion；未决项显式且不会被当成已定；大型项目、重大改动或架构调整已具备面向用户的人话方案摘要。

## 退出与重入
命中 [approve.md](approve.md) 进入条件的方案转 approve 落 `reviews/APPROVED.md` 后再进 decompose / plan / execute；其余直接转 decompose / plan / execute。实现发现设计不足时带新证据重入，只修订受影响部分。

## 方案细则（可选）

- **对比表**（多条可行路线时用；只有一条可行路线时不凑第二个方案，写一句为何只有它）：列 `方案 | 成本 | 风险 | 可逆性 | 工期 | 复杂度`，并写推荐主因、接受的取舍与回退方式。
- **设计依据**：`选择 → 模式 / 原则 → 为何适用 → 可检后果`（写成减少耦合面 / 接口面 / 重复 / 回归面或提升可测性，「更优雅」不算；既有代码已有同类做法优先对齐）。
- **两次设计（Design It Twice，高风险 / 多解接口可选）**：并行派 2–3 个 fresh context subagent 按互斥约束设计（极简接口最大化 depth / leverage、最大扩展性、默认调用方零心智、跨网 Ports & Adapters），围绕 **depth**、**locality** 与 **seam** 对比推荐，避免凑稻草人方案。
- **质量画像展开**（用户点名时）：按 [quality-appendix.md](quality-appendix.md) 把每条底线落到可验证页面 / 数据 / 验收方式，只细化不扩范围。
