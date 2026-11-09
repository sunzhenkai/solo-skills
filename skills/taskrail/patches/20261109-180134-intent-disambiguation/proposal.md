# 意图识别增加最小区分探索与证据纠偏

- target: skills/taskrail
- mode: update
- patch: 20261109-180134-intent-disambiguation
- risk: medium
- status: proposed

## Intent

现有意图门保证新意图经过复述与确认，但多种合理解释仍可能在缺少区分证据时被直接确认。将 intent 调整为最小认知循环：形成当前最佳理解，在意图有歧义或关键假设把握低时只读最有区分度的现场，再用具体完成结果和边界反例复述。后续证据推翻当前理解时，即使 criterion 原文未变也重入 intent。

新增三个声明式行为案例，覆盖多种交付物、方案与真实结果不一致、确认后被证据纠偏。非目标：不新增 reference、状态或固定阶段，不改变 human / goal 确认方式，不扩大技术探索范围。

## Conflict check

intent 负责形成和修正理解，explore 继续负责代码事实；intent 只允许消除当前歧义所需的最小只读取证。router 统一声明重入信号，confirm-protocol 继续独占确认停点。测试与 eval 沿用现有结构。

## Rationale

改动直接针对“第一个合理解释被过早锁定”和“criterion 未变就不重入”两处机制缺口。协议规则可由文本契约测试守卫，真实场景由 eval 提供可评审的判据；改动局限于 taskrail。

## Files

- skills/taskrail/references/intent.md：增加最小区分探索、具体结果与边界反例。
- skills/taskrail/references/router.md：增加理解不确定及证据推翻意图时的重入信号。
- skills/taskrail/tests/test_intent_contract.py：守卫意图侧行为。
- skills/taskrail/tests/test_intent_loop_contract.py：守证据纠偏路由。
- skills/taskrail/evals/cases.yaml：增加三个行为案例。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m pytest skills/taskrail/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style`。
- 解析 evals YAML，核对实际 diff 仅含 proposal 声明的生产文件。
