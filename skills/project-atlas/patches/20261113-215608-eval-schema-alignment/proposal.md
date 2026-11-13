# 对齐 Atlas eval 结构契约

- target: skills/project-atlas
- mode: update
- patch: 20261113-215608-eval-schema-alignment
- risk: low
- status: proposed

## Intent

为 project-atlas/evals/cases.yaml 的现有与本轮新增案例补齐仓级必需的 id/kind/judge/description/given/expect.must 结构；保留各案例原始语义和期望。

## Conflict check

仓级 tests/test_evals_structure.py 要求统一结构，Atlas 原有 input/expected 写法与该契约不一致。本轮仅做结构迁移，不改 Skill 行为。

## Rationale

本轮修改了该 eval 文件，交付前须通过覆盖它的仓级测试。结构对齐可由确定性测试验证。

## Files

- skills/project-atlas/evals/cases.yaml：转换六个案例的字段结构。

## Validation

- 机械生成 change.patch，git apply --check --recount。
- 应用后运行 git diff --check、Atlas 测试与仓级 eval 结构测试。
