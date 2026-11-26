# P0 修复：消除标识/枚举冲突并收紧 task_state.py 机械门禁

- target: skills/taskrail
- mode: update
- patch: 20261127-002600-p0-contract-and-gates
- risk: high
- status: proposed

## Intent

收口 taskrail 审阅中发现的标识冲突、状态枚举割裂与脚本机械门禁漏洞：

1. 将 `references/review.md` 的 Blocker / Major 评审发现编号由 `F-n` 改为 `RF-n`，消除与 `context/current.md` 待明确区 `F-n` 的命名碰撞。
2. 将 `current_ref` 的意图枚举值统一为 `intent`（脚本兼容归一化旧值 `intake` -> `intent`），使 `contract.md`、`templates.md`、`evals/cases.yaml`、`router.md` 与 `task_state.py` 保持一致。
3. 补齐 `scripts/task_state.py` 的四项机械校验与解析缺陷：
   - `init` 生成 `PLAN.md` 时默认带 `## 实施确认`（`- 状态：pending`），且切 `execute` 时缺少 `## 实施确认` 或状态非 `confirmed / not-required` 一律阻断；
   - 切 `plan` / `execute` 时校验 `context/current.md` 意图确认状态为 `confirmed` 或 `not-required`，切 `execute` 时校验 `criterion` 非空；
   - `APPROVED.md` 须非空，`done` / `reconcile` 要求 `SUMMARY.md` 存在且含非标题、非占位的实质正文；
   - 修复 `parse_task()` 解析转义引号 `criterion` 的往返损坏问题。

非目标：不改变动态路由结构、不调整小/中/大任务的确认档位设计（留待 P1/P2）、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskflow/patches/20261127-002600-p0-handoff-worktree-and-direct-alignment/`（同步消除 `taskflow` 中 `direct` 跳过 `approve` 的冲突表述，并补齐 `check_handoff.py` 父批准继承与 `prepare_worktree.py` 子任务路径隔离）。
- 仓级配套改动（非本 patch 范围）：同步 `docs/task-flow/README.md`、`AGENTS.md`、`scripts/check_output_style.py`、`scripts/e2e_cross_repo.py`、`tests/test_output_style.py`。
- 保持 `SKILL.md` 体积、一层直链、正向表述与 stdlib-only 脚本约束不变。

## Rationale

`review.md` 与 `contract.md` 共用 `F-n` 会在决策/总结引用时直接碰撞；`router.md` 指向 `intent` 而脚本只认 `intake` 会导致调用报错；`init_task()` 原本未写 `## 实施确认` 且 `plan_confirm_state()` 对缺失返回 `None` 放行，使新任务可绕过实施确认门禁；意图确认与空 `SUMMARY.md` 未机械校验也留下了静默跳过的缺口。本轮将上述边界全部收敛进脚本机械校验与单测守卫。

## Files

- `skills/taskrail/references/review.md`：评审发现编号由 `F-n` 改为 `RF-n`。
- `skills/taskrail/references/contract.md`：`current_ref` 统一为 `intent`（保留旧值 `intake` 兼容说明），同步 `task_state.py` 机械检查说明。
- `skills/taskrail/references/templates.md`：新建根任务示例说明同步为 `current_ref: intent`（兼容旧值 `intake`）。
- `skills/taskrail/evals/cases.yaml`：意图确认案例同步为 `current_ref` 从 `intent` 开始。
- `skills/taskrail/scripts/task_state.py`：统一 `intent` 与 `intake` 兼容别名，修复标量引号解析，`init` 默认写入 `PLAN.md` 实施确认，并在 `update` / `reconcile` 补齐意图确认、非空 `criterion`、必填实施确认、非空 `APPROVED.md` 与实质 `SUMMARY.md` 校验。
- `skills/taskrail/tests/test_taskrail_contract.py`：同步 `intent` 契约并新增 `RF-n` 防冲突守卫。
- `skills/taskrail/tests/test_explore_contract.py`：同步 `templates.md` 中 `current_ref: intent` 守卫。
- `skills/taskrail/tests/test_task_state.py`：更新并扩充机械门禁、旧值别名、空总结拦截与引号往返单测。

## Validation

- 在工作树根运行 `git apply --check --recount skills/taskrail/patches/20261127-002600-p0-contract-and-gates/change.patch`。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`、`python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'` 与 `python3 -m unittest discover -s tests -p 'test_*.py'`。
- 运行 `make check-names` 与 `make check-style`，确认 0 报错 0 告警。
