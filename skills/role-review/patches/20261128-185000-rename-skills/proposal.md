# 改名为 role-review

- target: skills/role-review
- mode: update
- patch: 20261128-185000-rename-skills
- risk: low
- status: proposed

## Intent

将 role-based-reviewer 改名为 role-review（对齐 role-chat），并同步内部对 agent-docs 的引用。

## Conflict check

与其余受影响 skill 及 `archive/README.md` 同步更新，无冲突。

## Rationale

统一 skill 命名（`role-review`、`agent-docs`、`project-patterns`）并保持跨 skill 引用与契约测试一致。

## Files

- `skills/role-review/SKILL.md`
- `skills/role-review/evolutions/20260929-role-thicken-batch1/decision.md`
- `skills/role-review/evolutions/20260929-role-thicken-batch1/eval.md`
- `skills/role-review/evolutions/20260929-role-thicken-batch1/proposal.yaml`
- `skills/role-review/evolutions/20260929-role-thicken-batch2/decision.md`
- `skills/role-review/evolutions/20260929-role-thicken-batch2/eval.md`
- `skills/role-review/evolutions/20260929-role-thicken-batch2/proposal.yaml`
- `skills/role-review/evolutions/20260930-heterogeneous-review/SKILL.md.candidate`
- `skills/role-review/evolutions/20260930-heterogeneous-review/decision.md`
- `skills/role-review/evolutions/20260930-heterogeneous-review/proposal.yaml`
- `skills/role-review/evolutions/20261011-review-output-contract/SKILL.md.candidate`
- `skills/role-review/evolutions/20261011-review-output-contract/decision.md`
- `skills/role-review/evolutions/20261011-review-output-contract/eval.md`
- `skills/role-review/evolutions/20261011-review-output-contract/proposal.yaml`
- `skills/role-review/evolutions/20261011-review-output-contract/references/brief-protocol.md.candidate`
- `skills/role-review/patches/20260828-183715-drop-task-workflow-downstream/change.patch`
- `skills/role-review/patches/20260828-183715-drop-task-workflow-downstream/proposal.md`
- `skills/role-review/patches/20260828-183715-drop-task-workflow-downstream/result.md`
- `skills/role-review/patches/20260925-030131-uiux-role/change.patch`
- `skills/role-review/patches/20260925-030131-uiux-role/proposal.md`
- `skills/role-review/patches/20260925-030131-uiux-role/result.md`
- `skills/role-review/patches/20260925-031016-split-role-files/change.patch`
- `skills/role-review/patches/20260925-031016-split-role-files/proposal.md`
- `skills/role-review/patches/20260925-031016-split-role-files/result.md`
- `skills/role-review/patches/20260927-005051-workflow-caller/change.patch`
- `skills/role-review/patches/20260927-005051-workflow-caller/proposal.md`
- `skills/role-review/patches/20260927-005051-workflow-caller/result.md`
- `skills/role-review/patches/20260927-094200-structured-workflow-description/change.patch`
- `skills/role-review/patches/20260927-094200-structured-workflow-description/proposal.md`
- `skills/role-review/patches/20260927-094200-structured-workflow-description/result.md`
- `skills/role-review/patches/20260927-144200-icon-form-consistency/change.patch`
- `skills/role-review/patches/20260927-144200-icon-form-consistency/proposal.md`
- `skills/role-review/patches/20260927-144200-icon-form-consistency/result.md`
- `skills/role-review/patches/20260927-171900-density-tier-justification/change.patch`
- `skills/role-review/patches/20260927-171900-density-tier-justification/proposal.md`
- `skills/role-review/patches/20260927-171900-density-tier-justification/result.md`
- `skills/role-review/patches/20260930-172217-diag-role/change.patch`
- `skills/role-review/patches/20260930-172217-diag-role/proposal.md`
- `skills/role-review/patches/20260930-172217-diag-role/result.md`
- `skills/role-review/patches/20260930-172942-skill-reviewer-role/change.patch`
- `skills/role-review/patches/20260930-172942-skill-reviewer-role/proposal.md`
- `skills/role-review/patches/20260930-172942-skill-reviewer-role/result.md`
- `skills/role-review/patches/20260930-173857-ceiling-refset-boundary/change.patch`
- `skills/role-review/patches/20260930-173857-ceiling-refset-boundary/proposal.md`
- `skills/role-review/patches/20260930-173857-ceiling-refset-boundary/result.md`
- `skills/role-review/patches/20261008-design-rationale-engineer/change.patch`
- `skills/role-review/patches/20261008-design-rationale-engineer/proposal.md`
- `skills/role-review/patches/20261008-design-rationale-engineer/result.md`
- `skills/role-review/patches/20261014-remove-ui-templates-dependency/change.patch`
- `skills/role-review/patches/20261014-remove-ui-templates-dependency/proposal.md`
- `skills/role-review/patches/20261014-remove-ui-templates-dependency/result.md`
- `skills/role-review/patches/20261014-ui-overreach-speed/change.patch`
- `skills/role-review/patches/20261014-ui-overreach-speed/proposal.md`
- `skills/role-review/patches/20261014-ui-overreach-speed/result.md`
- `skills/role-review/patches/20261015-223500-aesthetic-goal/change.patch`
- `skills/role-review/patches/20261015-223500-aesthetic-goal/proposal.md`
- `skills/role-review/patches/20261015-223500-aesthetic-goal/result.md`
- `skills/role-review/patches/20261015-231000-no-bookkeeping-questions/change.patch`
- `skills/role-review/patches/20261015-231000-no-bookkeeping-questions/proposal.md`
- `skills/role-review/patches/20261015-231000-no-bookkeeping-questions/result.md`
- `skills/role-review/patches/20261015-231500-source-first-intent/change.patch`
- `skills/role-review/patches/20261015-231500-source-first-intent/proposal.md`
- `skills/role-review/patches/20261015-231500-source-first-intent/result.md`
- `skills/role-review/patches/20261015-234800-despecialize-task-boundary/change.patch`
- `skills/role-review/patches/20261015-234800-despecialize-task-boundary/proposal.md`
- `skills/role-review/patches/20261015-234800-despecialize-task-boundary/result.md`
- `skills/role-review/patches/20261015-intent-role/change.patch`
- `skills/role-review/patches/20261015-intent-role/proposal.md`
- `skills/role-review/patches/20261015-intent-role/result.md`
- `skills/role-review/patches/20261016-000800-trim-overdesign/change.patch`
- `skills/role-review/patches/20261016-000800-trim-overdesign/proposal.md`
- `skills/role-review/patches/20261016-000800-trim-overdesign/result.md`
- `skills/role-review/patches/20261016-084733-writing-review/change.patch`
- `skills/role-review/patches/20261016-084733-writing-review/proposal.md`
- `skills/role-review/patches/20261016-084733-writing-review/result.md`
- `skills/role-review/patches/20261020-233500-task-series-deep-review/change.patch`
- `skills/role-review/patches/20261020-233500-task-series-deep-review/proposal.md`
- `skills/role-review/patches/20261020-233500-task-series-deep-review/result.md`
- `skills/role-review/patches/20261021-202540-pretty-ui-rule-ids/change.patch`
- `skills/role-review/patches/20261021-202540-pretty-ui-rule-ids/proposal.md`
- `skills/role-review/patches/20261021-202540-pretty-ui-rule-ids/result.md`
- `skills/role-review/patches/20261021-202819-merge-explore-intent/change.patch`
- `skills/role-review/patches/20261021-202819-merge-explore-intent/proposal.md`
- `skills/role-review/patches/20261021-202819-merge-explore-intent/result.md`
- `skills/role-review/patches/20261118-014208-skill-role-description-convention/change.patch`
- `skills/role-review/patches/20261118-014208-skill-role-description-convention/proposal.md`
- `skills/role-review/patches/20261118-014208-skill-role-description-convention/result.md`
- `skills/role-review/patches/20261118-224642-default-ui-routing/change.patch`
- `skills/role-review/patches/20261118-224642-default-ui-routing/proposal.md`
- `skills/role-review/patches/20261118-224642-default-ui-routing/result.md`
- `skills/role-review/patches/20261123-201100-clarify-adjacent-boundaries/change.patch`
- `skills/role-review/patches/20261123-201100-clarify-adjacent-boundaries/proposal.md`
- `skills/role-review/patches/20261123-201100-clarify-adjacent-boundaries/result.md`
- `skills/role-review/patches/20261123-202100-decouple-ui-hard-links/change.patch`
- `skills/role-review/patches/20261123-202100-decouple-ui-hard-links/proposal.md`
- `skills/role-review/patches/20261123-202100-decouple-ui-hard-links/result.md`
- `skills/role-review/patches/20261124-144900-ui-guardrails-and-check/change.patch`
- `skills/role-review/patches/20261124-144900-ui-guardrails-and-check/proposal.md`
- `skills/role-review/patches/20261124-144900-ui-guardrails-and-check/result.md`
- `skills/role-review/patches/20261124-234800-plain-output-omit-empty/change.patch`
- `skills/role-review/patches/20261124-234800-plain-output-omit-empty/proposal.md`
- `skills/role-review/patches/20261124-234800-plain-output-omit-empty/result.md`
- `skills/role-review/patches/20261127-164500-rename-way-to-cr/change.patch`
- `skills/role-review/patches/20261127-164500-rename-way-to-cr/proposal.md`
- `skills/role-review/patches/20261127-164500-rename-way-to-cr/result.md`
- `skills/role-review/references/inference-and-speed.md`
- `skills/role-review/references/protocol.md`
- `skills/role-review/references/roles/algo.md`
- `skills/role-review/references/roles/biz.md`
- `skills/role-review/references/roles/data.md`
- `skills/role-review/references/roles/design.md`
- `skills/role-review/references/roles/engineer.md`
- `skills/role-review/references/roles/ops.md`
- `skills/role-review/references/roles/product.md`
- `skills/role-review/references/roles/qa.md`
- `skills/role-review/references/roles/skill.md`
- `skills/role-review/references/roles/sre.md`
- `skills/role-review/references/severity.md`
- `skills/role-review/tests/test_review_output_contract.py`
- `skills/role-review/tests/test_role_review_contract.py`

## Validation

- `python3 -m unittest discover -s skills/role-review/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
