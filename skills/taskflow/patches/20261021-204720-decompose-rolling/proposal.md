# driver 滚动展开：依赖满足才展开子 change、逐片提交、片间检查点不停人

- target: skills/taskflow
- mode: update
- patch: 20261021-204720-decompose-rolling
- risk: high
- status: proposed

## Intent

这是 taskrail 同 id patch 的执行侧。原规则有两个问题：

- 子 change 的 artifacts 要在 propose 阶段一次性备齐，apply 阶段不能改 change 语义。后一片依赖前一片的代码时，只能按设想的接口去写。
- 只在收尾提交一次，跨会话续跑时没有检查点可以回退。

改法如下：

1. **Driver 协议**：
   - 子 change 按依赖分批展开：依赖的实施项都已勾的切片才建子 change，起草时以 worktree 里的代码为准。
   - 实施项要等对应子 change 全勾、validate 通过、这一片已经提交之后才勾。
   - 每勾一条实施项，过一次片间检查点，不停人：按新认识补拆、合并或改顺序（只动未勾的项，记进「已做决定」），再展开下一批。动到判据或范围的，走 taskrail「意图变更」。
   - 提交由编排者做，每片一次、收尾一次。
2. **propose 产出约定**：
   - 实施段按路线图一片一条，依赖写在括号里。
   - 新增「滚动展开」小节：propose 只展开就绪的那批切片。展开一片，就是对 `{task}-<slice>` 委托 stock `openspec-propose`。后面切片的细节只要没超出路线图那一行，就属于 approve 已批的范围。
   - 删掉「一次性备齐」那句。
3. **SKILL.md**：阶段路由和委托说明补上 `{task}-<slice>`；「执行」节写明逐片提交和片间检查点。
4. **execution-discipline 与 multi-worker**：
   - execution-discipline：实施项的勾选条件补上「已提交」；实现者输入改为「提交留给编排者」。
   - multi-worker：片间检查点归主会话串行做，每次只提交那一片的文件。

非目标：入口门脚本、收尾校核、子 change 的归档方式（3.5 逐个 `--yes`）都不变。

## Conflict check

- 已经建好的 driver，其 `proposal.md` 里是旧版协议块，按旧协议继续即可。新协议只对之后建的 driver 生效。
- worker 不再自己提交。这和 agent-roster「可写委派前看任务 worktree 是否干净」一致：每片提交后 worktree 回到干净状态，下一次委派不会被拦。
- 同轮 patch：taskrail（拆分机制）、agent-roster。

## Rationale

- **滚动展开**：后面的切片基于已经落地的代码起草，不靠设想。
- **逐片提交**：给跨会话续跑留检查点，也让 worktree 在片与片之间保持干净。
- **检查点不停人**：拆得越细，停得也不会越多。

## Files

- `skills/taskflow/SKILL.md`
- `skills/taskflow/references/{driver-template,execution-discipline,multi-worker}.md`
- `skills/taskflow/evals/cases.yaml`：新增 1 条
- `skills/taskflow/tests/test_check_handoff.py`：逃生口用例里的 phase 值从 explore 改为 design
- 新增 `skills/taskflow/tests/test_rolling_wave_contract.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：
  - `git diff --check`
  - `python3 -m pytest skills tests -q`
  - `make check-style`
