# 观感目标（设计感 / 好看）不分档收口

- target: skills/role-based-reviewer
- mode: update
- patch: 20261015-223500-aesthetic-goal
- risk: medium
- status: applied

## Intent

intent 角色新增 🔴 检查：自加限制或缩窄目标。

背景：一次「提升设计感，多用颜色 + 图表」的 goal 任务全流程合规却几乎没变好看——实现没有视觉方向、意图被缩窄并自加了不做项、评审没有参照集无法评观感、没人看过截图。

## Conflict check

none：只在观感目标时加规则；唯一出处为 taskrail gate-packs「审美目标（不分档）」，其余为指针。

## Files

- references/roles/intent.md、tests/test_role_based_reviewer_contract.py
