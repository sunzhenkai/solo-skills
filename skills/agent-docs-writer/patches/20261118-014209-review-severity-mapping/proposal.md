# review 路径写明与 role-based-reviewer 的级别对应

- target: skills/agent-docs-writer
- mode: update
- patch: 20261118-014209-review-severity-mapping
- risk: low
- status: proposed

## Intent

review 细则写明 high / medium / low 与 `role-based-reviewer` 的 Blocker / Major / 默认不报一一对应；需要与其他岗位视角并列审查时交给其 `roles=skill`。非目标：评审维度与输出格式不变。

## Conflict check

none。`role-based-reviewer` 的 skill 角色同轮改为与本 skill 一致的 description 判据（其 patch `20261118-014208-skill-role-description-convention`）。

## Rationale

两处 skill 评审入口此前互不指向、级别体系不同，结论无法互相引用。

## Files

- skills/agent-docs-writer/references/review.md：「输出发现」节级别说明。
- skills/agent-docs-writer/tests/test_agent_docs_writer_contract.py：新增守卫断言。

## Validation

- `python3 -m pytest skills/agent-docs-writer/tests -q`
