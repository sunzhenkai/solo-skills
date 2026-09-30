# task* 系列常驻 context 瘦身 + Self-evolution 注入块收敛

- target: skills/{taskflow,task-explore,task-wizard,task-goal,task-delivery,skill-upgrader,repo-manager,skills-store}
- mode: update（多 skill 打包）
- patch: 20260930-101500-task-skill-context-prune
- risk: medium
- status: proposed

## Intent

按 `writing-for-agents` 的三条杠杆收口 task* 系列的常驻成本与样板重复，不改任何行为规范：

1. **description 瘦身**（context pointer 只留触发分支）：5 个 task skill 的 description 复述了正文已承载的实现细节。
   task-explore 463 → 242 字符（含 11 阶段清单与 goal 确认段），taskflow 296 → 200（删 `skip_specs`、零脚本、第二份账本），
   task-wizard 192 → 105，task-delivery 248 → 190。task-goal 265 → 255，仅把「复杂档先外部参照」等正文细节折叠，
   触发门（`/goal`、挂载、上游委派）逐字保留。触发分支一个不删。
2. **Self-evolution 注入块压成指针式短块**：84 行样板 × 4 个 skill（taskflow、task-goal、repo-manager、skills-store）
   压成 18 行且四份逐字同文；`skill-upgrader/references/skill-injection.md` 同步为新模板。
   原块内 `Experience → Repeated Pattern → Improvement Proposal → Eval → Pass → Update Skill`
   与 `Single Failure → Directly modify SKILL.md` 两个 ASCII 流程图是空转的仪式性内容（真正的门禁一句「先提案再改」已覆盖），
   且 taskflow 版与 task-goal 版已实际漂移（taskflow 少了 skill-upgrader 分支）。
3. **正文内复述去重**：删 task-goal「减少确认」节与「不套模板」节重复的「推荐走 task-explore」一句；
   task-explore `handed-off` 段去掉与文首定义重复的「交付进度只认 taskflow checkbox」前缀；
   task-delivery `loop-protocol.md` Stage 7 的观感段改为指向 SKILL.md「观感类质量目标」。
   三处均确认无测试钉住、无行为语义损失。

非目标：不动 Driver 协议固定文本、验收 rubric 通过线、退出点判定、挂起五元组、降级 A/B 分类、
state-machine 网格、goal_transition 脚本；不碰任何 `evolutions/` 与历史 `patches/`。

## Conflict check

- 既有契约测试全绿（415 passed, 1 skipped）。新增 `TestSelfEvolutionSingleSource` /
  `TestDescriptionTriggerBranches` 锁住本轮两条不变量：短块四份逐字同文并与注入模板一致；taskflow description 保留触发分支且不复述正文细节。
- `skill-upgrader` 的幂等规则（「已有同等 Self-evolution 段落则不要再贴一份」）不受影响：模板仍是同一 `## Self-evolution` 标题与同构小节。
- repo-manager / skills-store 的契约测试不钉 Self-evolution 文本；两仓自进化目录（examples/evals/experience）未动。

## Rationale

常驻 context 每轮都付费：description 与 SKILL.md 正文在 skill 触发后全量进上下文，84 行样板乘 4 个 skill 是纯重复成本。
收敛为单一模板 + 触发分支最小化后，改一次模板只需同步一处（模板文件），四份生产块由新增的单源测试防漂移。

## Files

- `skills/task{flow,explore,wizard,goal,delivery}/SKILL.md` — description 瘦身；taskflow/task-goal 的 Self-evolution 块换短版
- `skills/{repo-manager,skills-store}/SKILL.md` — Self-evolution 块换短版（与上四份同文）
- `skills/skill-upgrader/references/skill-injection.md` — 注入模板同步为短版
- `skills/task-delivery/references/loop-protocol.md` — Stage 7 观感段改指针
- `skills/taskflow/tests/test_taskflow_contract.py` — 新增两组契约断言

## Validation

- 应用前：`git apply --check --recount`（已在干净工作区验证通过）
- 应用后：`git diff --check`；`python3 -m pytest skills -q` → 415 passed, 1 skipped
- 行数：taskflow 258 → 192、task-goal 318 → 251、repo-manager 382 → 316、skills-store 362 → 296
- 隐私检查：无密钥 / 内部 URL / 公司信息；模板占位符仍为 `<skill-dir>`
