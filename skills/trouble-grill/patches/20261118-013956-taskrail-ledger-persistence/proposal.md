# taskrail 任务内落盘对齐台账契约，description 改正向触发

- target: skills/trouble-grill
- mode: update
- patch: 20261118-013956-taskrail-ledger-persistence
- risk: medium
- status: proposed

## Intent

在 taskrail 任务里排查时，每轮「证据 + 用户输入 + 路径」追加到任务目录的 `evidence/diagnose.md`，坐实或推翻的结论连同回退条件写入 `context/current.md` 结论表，覆盖子任务路径；正文写明本 skill 是 taskrail diagnose 环节的排查方法，路由归 taskrail。description 去掉「不走本流程」，改为正向说明方法与触发场景。非目标：假设板、四道门、收口规则与 wiki-data 归档不变。

## Conflict check

原文要求追加到 `TASK.md` 的「进展」段：taskrail `templates.md` 无此段，且规定 TASK 只放热状态、证据进 `evidence/`；原路径也未覆盖 `subtasks/`。本改动对齐 taskrail，不改 taskrail。

## Rationale

按原文执行会让 TASK 无界增长、破坏 resume 的热状态读取。AGENTS.md 要求 description 只写正向 WHAT + WHEN，边界放正文（正文已有「不适用」一句）。

## Files

- skills/trouble-grill/SKILL.md：description；taskrail 关系一句；落盘位置第一条。
- skills/trouble-grill/tests/test_trouble_grill_contract.py：去掉锁定旧路径的断言，新增台账契约与正向 description 断言。

## Validation

- `python3 -m pytest skills/trouble-grill/tests -q`
- 全量测试与 `make check-style`
