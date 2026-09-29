# Proposal：Goal 执行协议从 task-wizard 解耦，新建 task-goal

## 背景

task-wizard 同时是「方案生成器」和「goal 执行协议」（Goal 方案 + 审阅 + 退出点 + 授权占七成篇幅），两个职责焊在一起；task-explore 的「Goal 里的确认」反向依赖 task-wizard 的审阅，同一机制两份写法；delivery-loop 自己判 goal 又指定 task-wizard 走 Goal 分支。

## 决定

1. **新建 task-goal**：承接 task-wizard 的 Goal 方案整节（不套模板/正文/外部参照/审阅/旧方案/写完之后/退出点/授权/执行中改步骤/做完），语义不变。references 迁入 quality-profile.md 与 legacy-plans.md；external-precedent.md 留在 task-wizard（方案定稿前的动作归方案层），task-goal 自产方案时复用同文件。
2. **起手输入约定（新接口）**：接到上游 task-wizard 方案原文时跳过产方案，逐字采用，直接外部参照 → 审阅。
3. **评审者三选一必选**：role-based-reviewer / agent-roster / subagent 三选一、选中唯一、每次审阅记录评审者；复杂档初审固定 role-based-reviewer；新增退出点「评审者未定」；旧的「其余情况：当前宿主拉起的子 agent」兜底措辞废弃。
4. task-wizard 收窄为纯方案层：删 Goal 分支，加「决策收敛」，CONTEXT 的 Goal 术语整体迁入 task-goal CONTEXT。
5. task-explore 的「Goal 里的确认」改为指针（审阅规则以 task-goal 为准），保留推荐默认取法。
6. delivery-loop 改名 task-delivery：goal 模式动作改为「确认与方案审阅委托 task-goal」；Stage 1 复杂判据删除，改为委托 task-wizard 产方案并读其档位。

## 理由

- 职责单 owner：方案在 task-wizard、确认/审阅在 task-goal、编排在 task-delivery/task-explore/taskflow。
- 评审独立性由结构保证（方案作者与评审发起方是两次调用），不靠纪律。
- 「评审者必选」把独立评审从复杂档的制度推广到所有档位，杜绝默认滑向兜底。

## 验证

- task-goal 契约测试 23 条（含三选一、评审者未定、接方案逐字采用、task-wizard 无 Goal 分支）。
- task-wizard 契约测试改为：Goal 节与术语不存在、决策收敛存在、references 迁移。
- taskflow / task-explore 测试同步改指 task-goal。
- 全仓 `python3 -m pytest skills -q`：282 passed, 1 skipped。

## 明确不改

审阅机制语义（边界四件套、环节表、P 级、核对循环、完成程度显式判定、pending 降级门）、复杂度三档定义、taskflow、agent-roster。
