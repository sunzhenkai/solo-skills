# Proposal：命令词表、handoff→propose、explore 轻重、瘦身（Wave 1）

## Intent

D2–D4：命令 ≠ `TASK.md.phase`；handoff 成功置 `phase: propose`；explore 区分仅 grill / 完整；`new/chat/save/resume` 细则下沉 references。

## Mode / Risk

`update` / `medium`（用户已确认按推荐做完）

## Validation

`python3 -m pytest skills/task-explore/tests skills/taskrail/tests/test_task_family_contract.py -q`
