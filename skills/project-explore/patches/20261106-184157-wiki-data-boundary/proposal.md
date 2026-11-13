# 更新 wiki-data 边界引用

- target: skills/code-explore
- mode: update
- patch: 20261106-184157-wiki-data-boundary
- risk: low
- status: proposed

## Intent

将知识 wiki 维护职责的下游名称由 `llm-wiki` 更新为 `wiki-data`，保持代码探索与知识库维护的既有边界不变。

## Conflict check

仅修改名称及对应契约断言，不改变阶段、写入门槛或探索行为。

## Rationale

避免改名后产生悬空引用，并以现有文本契约测试固定新名称。

## Files

- `skills/code-explore/SKILL.md`：更新下游 skill 名称。
- `skills/code-explore/tests/test_code_explore_contract.py`：更新边界断言与命名。

## Validation

- `git apply --check --recount` 通过后应用。
- 目标测试与全仓 `python3 -m pytest skills -q`。
- `git diff --check`。
