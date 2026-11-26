# P2 升级：向 taskflow 执行纪律注入接缝处单测试垂直 TDD 节奏

- target: skills/taskflow
- mode: update
- patch: 20261127-004500-p2-tdd-and-seam-execution
- risk: medium
- status: proposed

## Intent

补强 `skills/taskflow/references/execution-discipline.md` 的代码级实施纪律：业务逻辑改动与 bug 修复默认在设计约定的公开接缝（seam）上采用单测试垂直 TDD 节奏（每次只写一个验证外部行为的失败测试 Red → 最小实现通过 Green → 重构），避免批量预写绑定内部结构的脆弱测试；模块深化重构后用新接口测试替换旧浅层碎测试（replace, don't layer）。

非目标：不改变 worktree / driver 协议、不强制纯样式或纯配置小改跑完整 TDD、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskrail/patches/20261127-004500-p2-matt-engineering-core/`（在 `design.md` 约定 seam 与测试面，与本处实施期 TDD 节奏首尾衔接）。
- 保持 `SKILL.md <= 8192 B` 与现有契约测试全通过。

## Rationale

`execution-discipline.md` 原本只要求“跑 focused tests”，执行者容易先一口气写完实现再补绑定内部细节的脆测试。引入按接缝单测试垂直循环与 replace-don't-layer 原则后，测试直接守卫行为契约且能经受内部重构。

## Files

- `skills/taskflow/references/execution-discipline.md`：在「实施中」补充接缝处单测试垂直 TDD 与 replace-don't-layer 纪律。
- `skills/taskflow/evals/cases.yaml`：新增接缝单测试垂直 TDD 评估案例。
- `skills/taskflow/tests/test_execution_spine_contract.py`：新增 TDD 节奏与接缝替换测试守卫。

## Validation

- `git apply --check --recount skills/taskflow/patches/20261127-004500-p2-tdd-and-seam-execution/change.patch`
- `git diff --check -- skills/taskflow`
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`
- `make check-names` 与 `make check-style`
