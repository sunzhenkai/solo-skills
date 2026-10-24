# design：契约、结构、兼容性与迁移

## 目的
为契约或结构变化给出可实施、可回退、可验证的方案。

## 进入条件
涉及公共 / 内部接口、数据模型、架构依赖、复杂迁移、跨模块共享面，或实现会改变重要兼容行为。

## 跳过条件
完全沿用现有模式且没有契约 / 结构变化。grill 不是固定前置；只有存在关键取舍时先走 [grill.md](grill.md)。

## 所需输入
criterion、当前 plan、explore / diagnose 证据和已解决的 grill 决定。

## 执行方法
1. 写清现状证据、目标契约、边界、兼容性、回滚和验证策略。
2. 推荐与被放弃方案各写取舍；独立难逆决定写 ADR 并按 [user-report.md](user-report.md) 告知，术语写 glossary。
3. 多仓库共享契约放父任务 design，子任务只放自己的实现设计；不在每个子任务复制完整上下文。
4. 未就绪后续项只写边界与接口，细节轮到它时按当时代码补。
5. Web UI 按需读 ui-delivery；对比表按需读 design-detail。

## 产出
`design/README.md` 索引、`design/<topic>.md`、按需 ADR / contract / glossary；decisions 写决定。

## 完成门
接口与依赖明确，兼容 / 回滚可走，验证能覆盖 criterion；未决项显式且不会被当成已定。

## 退出与重入
需要批准转 approve，多交付转 decompose，否则 plan / execute。实现发现设计不足时带新证据重入，只修订受影响部分。
