# 观感目标（设计感 / 好看）不分档收口

- target: skills/taskrail
- mode: update
- patch: 20261015-223500-aesthetic-goal
- risk: medium
- status: applied

## Intent

gate-packs 新增「审美目标（不分档）」：视觉方向、天花板参照集、真实演示数据、改前改后截图、异源 design 评审；goal 自判迭代，human 给用户看截图。完成门加第 9 条；quality-profile / phase-wizard / user-report 加指针；phase-wizard 外部参照措辞放宽为可进参照集。

背景：一次「提升设计感，多用颜色 + 图表」的 goal 任务全流程合规却几乎没变好看——实现没有视觉方向、意图被缩窄并自加了不做项、评审没有参照集无法评观感、没人看过截图。

## Conflict check

none：只在观感目标时加规则；唯一出处为 taskrail gate-packs「审美目标（不分档）」，其余为指针。

## Files

- references/gate-packs.md、references/quality-profile.md、references/phase-wizard.md、references/user-report.md、SKILL.md（完成门 9；删一句与 gate-packs 重复的说明控体积）\n- tests/test_aesthetic_goal_contract.py（新）、tests/test_deliverable_class_contract.py、evals/cases.yaml
