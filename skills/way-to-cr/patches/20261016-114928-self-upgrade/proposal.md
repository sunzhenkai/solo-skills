# solo-code-review 补齐自进化结构（examples/evals/experience + 注入指针）

- target: skills/solo-code-review
- mode: self-upgrade
- patch: 20261016-114928-self-upgrade
- risk: medium
- status: proposed

## Intent

给 solo-code-review 补齐 skill-upgrader 约定的自进化目录结构，使后续正文优化（接入 OCR v1.12.9 新 flag、delegate fallback 等）能按 examples/evals/experience + patches 的审计链路进行：

- `examples/README.md`、`evals/README.md`、`experience/README.md`（复制自 skill-upgrader references，无真实案例，不编造）
- `evals/cases.yaml`：从现有 SKILL.md 抽取 10 条可验证 case（触发门禁、确认门、MR fetch-only、凭据禁令、产物落盘、总结打印、评论确认门、只读边界、回归测试）
- `experience/{failures,successes,patterns}/.gitkeep`
- SKILL.md 末尾追加一句自进化指针（原文其余内容一字不动）

非目标：不在本轮修改任何审查流程、命令、门禁；OCR v1.12.9 能力接入走下一轮 `update`。

## Conflict check

- SKILL.md 现无「自进化」段落，追加不与现有内容冲突；frontmatter 不动。
- 仓内 taskrail 等 skill 已有同构 examples/evals/experience 结构，本目录与之风格一致。
- `patches/20260820-010341-copy-code-review/` 历史记录不动。

## Rationale

仓库 AGENTS.md 约定：结构缺失先走 skill-upgrader 一次性升级，再基于后续变更留痕。当前 solo-code-review 缺 examples/evals/experience，且 tests/ 只测脚本、无文本契约保护；先把结构立起来，cases.yaml 同时充当后续 update 轮的回归清单。

## Files

- skills/solo-code-review/SKILL.md — 末尾追加「自进化」一节（一句指针）
- skills/solo-code-review/examples/README.md — 新增（复制源）
- skills/solo-code-review/evals/README.md — 新增（复制源）
- skills/solo-code-review/evals/cases.yaml — 新增，10 条从原文抽取的 case
- skills/solo-code-review/experience/README.md — 新增（复制源）
- skills/solo-code-review/experience/{failures,successes,patterns}/.gitkeep — 新增空目录占位

## Validation

- 应用前：`git apply --check --recount` 通过；cases.yaml 每条能在 SKILL.md 原文找到依据
- 应用后：`python3 -m pytest skills/solo-code-review/tests -q` 仍 5 passed；`make check-style` 无新增告警；SKILL.md frontmatter 未变、原正文 diff 仅为末尾追加
