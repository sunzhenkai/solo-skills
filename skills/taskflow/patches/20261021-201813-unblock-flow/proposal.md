# 经 taskrail 委托时代答 stock openspec 的停顿；入口门补查批准与判据

- target: skills/taskflow
- mode: update
- patch: 20261021-201813-unblock-flow
- risk: medium
- status: proposed

## Intent

task 系列复审（流程卡点与闭环）第 1 步「先修卡点」的 taskflow 部分。用户在会话里选定「按三步走：先修卡点 → 合并 task-explore / task-intent → 再做拆分」，本 patch 属其第 1 步。

- stock `openspec-propose` 有「产物写完就停、等新请求再 apply」的规划边界，`openspec-apply-change` 遇到不清楚会暂停列选项，`openspec-archive-change` 会问未勾项和是否同步 spec。经 taskrail 推进时这些停顿让 goal 模式也停下。新增「经 taskrail 委托时」一节：按表代答，停不停只看 taskrail 停点表；单独点名 taskflow 时照 stock 原样交互。
- driver 模板 3.5 写明子 change 用 `openspec archive {task}-<slice> --yes` 非交互归档（已在 openspec 1.14 实测：同步 spec 并归档，不提问）。
- `check_handoff.py` 原来不查方案是否批准、判据是否非空、driver 名是否对，approve 前的任务也能补个交接节混过入口门。补三项检查，子任务按 slug 末段取 driver 名。

非目标：Driver 协议、子 change 切分方式与 worktree 规则不变（拆分相关的改动在第 3 步）。

## Conflict check

- taskrail `confirm-protocol.md` 同轮加一句「stock 自带的停顿不算停点」指向本节；taskrail 契约 approve 出口第 4 条同轮补写入口门核对项。
- 入口门变严：按 task-explore 模板建的 TASK.md 在 handoff 时本就写 `driver`、有 `criterion` 与 `approve/APPROVED.md`；e2e 样例 `taskrail/examples/minimal-webui` 已满足。

## Rationale

stock skill 由上游生成、不在本仓改；在调用方写代答表是唯一不改上游的办法。入口门的新检查都是交接载荷里本来就要求的字段，只是此前没机械校验。

## Files

- `skills/taskflow/SKILL.md`：新增「经 taskrail 委托时」代答表。
- `skills/taskflow/references/driver-template.md`：3.5 写明非交互归档命令。
- `skills/taskflow/scripts/check_handoff.py`：补查 `approve/APPROVED.md`、`criterion`、`driver` 名。
- `skills/taskflow/tests/test_check_handoff.py`：夹具补齐新字段，新增 4 条用例。
- `skills/taskflow/tests/test_stock_delegation_contract.py`：新增，锚定代答表。

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/taskflow`；`python3 -m pytest skills/taskflow/tests -q`；全量 `python3 -m pytest skills tests -q`
