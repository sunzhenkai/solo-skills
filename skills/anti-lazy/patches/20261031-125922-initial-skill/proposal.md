# 创建 anti-lazy 初版

- target: skills/anti-lazy
- mode: update
- patch: 20261031-125922-initial-skill
- risk: low
- status: proposed

## Intent

新增一个以提示语引导思考的 skill，帮助 agent 理解用户意图、核实现场证据、定位关键差距并按证据收口，减少字面响应、假设现状和提前交付。

## Conflict check

- `trouble-grill` 负责根因排查的证据定级与假设验证；`anti-lazy` 只做通用意图与交付差距对齐，正文已标明边界。
- 轻任务保持直接回答，不引入固定输出模板。

## Rationale

短提示能激活模型的目标、证据和验收视角，同时避免用冗长规则制造形式主义或扩大任务范围。

## Files

- `skills/anti-lazy/SKILL.md`
- `skills/anti-lazy/tests/test_anti_lazy_contract.py`
- `skills/anti-lazy/evals/cases.yaml`
- `README.md`

## Validation

- `python3 -m pytest skills/anti-lazy/tests -q`
- `python3 -m pytest skills tests -q`
- `make check-names`
- `make check-style`
- `git diff --check`
