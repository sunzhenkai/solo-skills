# 修流程卡点与闭环：交接后的位置、完成通知与任务归档、full 档就绪检查前移

- target: skills/taskrail
- mode: update
- patch: 20261021-201813-unblock-flow
- risk: medium
- status: proposed

## Intent

task 系列复审（流程是否通顺、合理、闭环）第 1 步「先修卡点」的 taskrail 部分。用户在会话里选定「按三步走：先修卡点 → 合并 task-explore / task-intent → 再做拆分」，本 patch 属其第 1 步，不改结构。

- **交接后的位置**：handoff 之后 `phase` 由谁回写、resume 时怎么判断做到哪，原文没写。契约新增一节，按 driver 状态（有无 `tasks.md`、有无未勾项、是否已归档）推导 `phase`；SKILL.md resume 指向它。
- **终点**：full 档路径止于 `archive`，`done` 的位置与「归档」的四种含义混在一起。full 路径补 `→ done`；术语加「归档」：`phase: archive` 只指归档 driver，任务归档是搬任务目录、`done` 后同轮做；`status` 规则写明做完归档仍是 `done`、未完成关闭才是 `archived`。
- **完成通知**：完成时没有固定的对用户说法，代码在任务分支、台账与同步过的 spec 在主工作树，用户不知道怎么合入。user-report 新增第 8 节「完成通知」模板；skip 升 full 时留在主工作树的改动也写进通知。
- **就绪检查前移**：OpenSpec 不可用或仓里没有 `openspec/` 根，原来要到 handoff 建 driver 才发现。改为 wizard 定档为 `full` 时当场查，缺 `openspec/` 根就把 `openspec init --tools none` 记为决定写进定稿消息（已实测该命令非交互，只建 `openspec/` 结构）。
- **stock 停顿不算停点**：confirm-protocol 加一句，指向 taskflow 新增的代答表。
- grill 不再委托外部 `grilling`（与 task-explore 同轮），依赖说明随之更新；入口门核对项写进契约。

非目标：阶段枚举、停点表、skill 结构不变；拆分与合并分别在第 3、2 步。

## Conflict check

- 同轮 patch：taskflow（代答表、入口门补查）、task-explore（grill 内联、归档两种情况、脚本路径）、task-intent（`draft` 状态）。本 patch 的指针依赖它们。
- 另一会话同日改了 `references/done.md` 与两份测试（pretty-ui 改名）；本 patch 不碰这些文件。`evals/cases.yaml` 在其已暂存版本之上追加。
- 契约测试锚定的流程串 `wizard → … → archive` 仍为子串，不受 `→ done` 影响。

## Rationale

每一处都是「流程走到这里，模型不知道下一步或会停下来问」的缺口；补的都是确定的规则或模板，可用契约测试锚定。

## Files

- `skills/taskrail/SKILL.md`：依赖说明、resume 推导、`archive` / `done` 行、完成节。
- `skills/taskrail/references/contract.md`：full 路径、skip 升档遗留、grill 说明、入口门核对项、「交接后的位置」节、`status` 规则、阶段载荷、「归档」术语。
- `skills/taskrail/references/phase-wizard.md`：第 1 步落 `draft`，第 4 步就绪检查。
- `skills/taskrail/references/user-report.md`：第 8 节完成通知与一组前后对比。
- `skills/taskrail/references/confirm-protocol.md`：stock 停顿不算停点。
- `skills/taskrail/evals/cases.yaml`：新增 4 条案例。
- `skills/taskrail/tests/test_flow_closure_contract.py`：新增，锚定上述规则。

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/taskrail`；`python3 -m pytest skills/taskrail/tests -q`；全量 `python3 -m pytest skills tests -q`；`make check-style`；`make check-names`
