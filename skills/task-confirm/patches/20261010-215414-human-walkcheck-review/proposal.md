# human 闸口强制走查 + 点名派审

- target: skills/task-confirm
- mode: update
- patch: 20261010-215414-human-walkcheck-review
- risk: medium
- status: proposed

## Intent

解决执行中暴露的缺口（源自一次真实任务会话（human 模式））：wizard 定稿等 human 闸口只有「列选项等人确认」，**没有评审动作**——方案与流程总览的「判据可检查 / 步骤可达判据 / 交付标准无漏越界」无人核对，本人点「按推荐」不等于评审，导致 human 与 goal 模式质量门槛不对等。

本 patch：

1. human 模式在 wizard 定稿 / approve 闸口增加**强制走查**：呈现前自走三连（判据可检查 / 流程总览或推荐方案步骤可达判据 / 交付标准无漏越界），呈现中附结论一行；走查不过先修方案。
2. human 模式开放**点名派审**：用户点名评审（名册 / subagent / 同事已评）时复用现有「审阅」节（P 级判定与收敛规则不变），human 闸口表的「推荐整体」即审阅的推荐默认。
3. 闸口输入材料补「流程总览」（wizard 定稿 / approve 时），与 taskrail 契约刚加的走查项对齐。

非目标：goal 模式审阅机制不动；不自动给 human 派审（仍由用户点名）；approve 的结构门细则仍在 task-explore phase-approve，不复制。

## Conflict check

- taskrail 硬边界「不复制 task-confirm 的审阅规则」：本 patch 正是审阅规则的唯一落点，contract 处只留存在性指向。无冲突。
- 「永不因审阅收敛自动放行」清单不变；走查是呈现前自检，不降低任何退出点门槛。无冲突。
- 名册评审在 task-explore phase-approve 已有先例，本 patch 不重复其细则，只给 human 入口。无冲突。

## Rationale

走查三连取自本 SKILL.md 审阅表现有「方案/步骤闸口」审项，human 版只是把同一标准变成呈现前强制自检，不引入第二份规则。可验证：apply 后 human 闸口模板必含走查结论行；点名派审路径引用现有审阅节。

## Files

- `skills/task-confirm/SKILL.md` — 「human 闸口呈现（强制）」节加走查与点名派审两段；「闸口输入」节材料清单补流程总览。

## Validation

- 应用前检查：`git apply --check --recount`。
- 应用后检查：与 proposal 核对；走查三连与审阅表审项一致；frontmatter 未动（注意源库 frontmatter 与安装副本不同，patch 只触及正文）。
