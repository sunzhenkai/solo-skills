# Patch Result: ruling-format

- patch_id: 20260929-192715-ruling-format
- status: applied
- risk: medium（用户已在应用前确认具体改动内容）
- applied: 2026-09-29

## 验证

- `git apply --check --recount` 通过
- `git apply --recount` 通过；`git diff --check -- skills/` 无空白错误
- `python3 -m pytest skills -q`：305 passed, 1 skipped
- 实际 diff 与 proposal 一致：Stage 7 回归门尾部补裁决呈现形状（冲突项 + 双方口径原文 + 推荐裁决 + 一句话决定；一次性说明、不列选项、不登记为任务）
- 无隐私内容；未触碰历史 patches/

## 关联

- 配套：`skills/task-goal/patches/20260929-192710-goal-wait-protocol`
