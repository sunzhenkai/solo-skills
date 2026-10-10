# wizard 流程总览锚点 + 质量属性节

- target: skills/taskrail
- mode: update
- patch: 20261010-215414-flow-overview-anchor
- risk: medium
- status: proposed

## Intent

解决执行中暴露的两个缺口（源自一次真实任务会话）：

1. **步骤走形无约束**：wizard 的「步骤」只是示例级清单，无完整性要求（末步须走得到判据），且下游 design / propose / apply 无对齐机制，步骤可被无声改写或丢弃。本 patch 把「步骤」升格为「流程总览」：从现状到完成判据的完整步骤链（由只读摸底探索得出），作为后续各阶段对齐锚点；design 须逐条映射，偏离写显式决策；approve 结构门核对；快照随 handoff 进 driver。
2. **质量属性缺失**：wizard plan 模板无任何质量维度，UI 美观度等质量目标直到复杂档 design 阶段才首次被质量画像覆盖，medium / simple 全程无承载字段。本 patch 在 plan 模板加「质量属性」节（通用维度：观感 / 性能 / 可靠性 / 可维护性；不可确定性度量的写验收方式或参照；不适用写原因），作为后续质量画像的来源输入。

非目标：不改 wizard 的提问/闸口流程本身；不改质量画像字段定义（quality-profile.md 不动）；不为 simple 档引入完整画像。

## Conflict check

- taskrail 硬边界「不复制 task-confirm 的审阅规则」：contract 闸口表只加走查存在性与指向（细则见 task-confirm），不复制判定规则。无冲突。
- taskflow 的职责：contract 只要求「流程总览快照随交接进 driver」，driver 如何用由 taskflow 自定。无冲突。
- 质量画像（复杂档 design 草稿、approve 冻结）机制不变，wizard 质量属性节是其上游输入，不替代。无冲突。

## Rationale

- 走查项（判据可检查 / 步骤可达判据 / 交付标准无漏越界）本就是 task-confirm 审阅表「方案/步骤闸口」的审项；本 patch 做的是把 wizard 产出物升格为可被这些审项约束的形态，并在编排层补对齐链路。可验证：apply 后新任务的 wizard plan 必含两节，下游载荷表有映射要求。
- 通用性：「流程总览锚点」对任意任务（不止 UI）成立；「质量属性」按通用质量维度表述，UI 美观只是实例。

## Files

- `skills/taskrail/references/phase-wizard.md` — 原则加两条；模板「步骤」→「流程总览」并加完整性要求；新增「质量属性」节；同步 简洁 bullet 用词。
- `skills/taskrail/references/contract.md` — 阶段载荷表：explore/design 行补「含流程总览与质量属性节」、新增 design 映射行、propose 行补总览快照进 driver；确认闸口表 wizard 定稿 / approve 行补 human 走查与对齐核对存在性。

## Validation

- 应用前检查：`git apply --check --recount`。
- 应用后检查：与 proposal 逐条核对 diff；`grep` 确认模板节名与载荷表行存在；无隐私内容；frontmatter 未动。
