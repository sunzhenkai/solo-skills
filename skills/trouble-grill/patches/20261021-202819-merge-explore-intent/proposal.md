# 保存位置的任务台账改称 taskrail 任务

- target: skills/trouble-grill
- mode: update
- patch: 20261021-202819-merge-explore-intent
- risk: low
- status: proposed

## Intent

task-explore 并入 taskrail（同 id 的 taskrail patch）。「推荐保存位置」第一条「在 task-explore 任务里」改为「在 taskrail 任务里」，路径不变。

## Conflict check

none

## Rationale

旧 skill 名删除后读者找不到对应的台账来源。

## Files

- `skills/trouble-grill/SKILL.md`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/trouble-grill`；`python3 -m pytest skills tests -q`
