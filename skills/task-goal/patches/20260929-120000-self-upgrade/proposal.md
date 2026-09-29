# task-goal 自进化结构升级

- target: skills/task-goal
- mode: self-upgrade
- patch: 20260929-120000-self-upgrade
- risk: medium
- status: proposed

## Intent

为新建的 task-goal 补齐自进化结构（examples/ + evals/ + experience/）并在 SKILL.md 末尾注入标准 Self-evolution 段落。不改任何已有行为、门禁与协议文本。evals 从现有 SKILL.md 的 MUST / 禁止 / 门禁抽取，不发明能力；examples 与 experience 保持空骨架，不伪造历史。

## Conflict check

none。SKILL.md 无已有 Self-evolution 段落；patches/ 已存在（首轮解耦 patch），本模式不写 patches/ 业务内容；tests/ 已存在，evals 以 regression case 指向而非复制。

## Rationale

仓约（AGENTS.md「结构约定」）要求 skill 按成熟度补齐 evals/ experience/；task-goal 刚承接完整 goal 执行协议，提前立好 cases 可防后续改动破坏审阅机制。cases 全部可从原文找到依据，且已有 pytest 契约可作确定性 regression。

## Files

- skills/task-goal/examples/README.md（复制模板）
- skills/task-goal/evals/README.md（复制模板）
- skills/task-goal/evals/cases.yaml（按原文抽取 10 条）
- skills/task-goal/experience/README.md + failures/.gitkeep + successes/.gitkeep + patterns/.gitkeep
- skills/task-goal/SKILL.md（末尾追加 skill-injection 段落，<skill-dir> 替换为 skills/task-goal）

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills/task-goal/tests -q` 全过；frontmatter 未动；注入段落与 skill-injection.md 一致（仅 <skill-dir> 替换）；无密钥/主机名/内部 URL
