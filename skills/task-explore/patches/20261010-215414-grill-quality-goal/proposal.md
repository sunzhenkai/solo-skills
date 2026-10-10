# grilling 提问维度补质量目标

- target: skills/task-explore
- mode: update
- patch: 20261010-215414-grill-quality-goal
- risk: low
- status: proposed

## Intent

解决执行中暴露的缺口（源自一次真实任务会话）：grilling 的提问维度是「预期目标、成功标准、范围、约束、未知」，质量目标（观感 / 性能等）只能借「成功标准」顺带覆盖，无任何显式提示，导致 UI 美观度等质量维度在 explore 阶段被漏问，直到复杂档 design 阶段才被质量画像兜底——medium / simple 档则全程无人问。

本 patch：

1. `phase-explore.md` 提问维度显式加入「质量目标」，并要求对不可确定性度量的项（典型：UI 观感、体验手感）追问验收方式或参照。
2. 质量目标澄清结论写入 `explore/` 纪要，作为 design 阶段质量画像草稿的输入，不另起文档。

非目标：不改 grilling skill 本身；不改质量画像字段；不给 simple / medium 强加画像。

## Conflict check

- taskrail wizard 模板新增的「质量属性」节是本 patch 提问结论的落点之一，两者互补（wizard 定稿前必填，explore 负责澄清），无重复定义。无冲突。
- phase-explore 步骤 7 已有「术语结晶写 glossary / ADR」的落盘纪律，本 patch 在同一条下补质量目标落点，不新增写盘位置。无冲突。

## Rationale

改动两处一句话，不改变 explore 流程结构；可验证：apply 后 phase-explore 第 5、7 步含质量目标字样。

## Files

- `skills/task-explore/references/phase-explore.md` — 步骤 5 提问维度加质量目标；步骤 7 补质量目标澄清结论的落点。

## Validation

- 应用前检查：`git apply --check --recount`。
- 应用后检查：与 proposal 核对；无隐私内容。
