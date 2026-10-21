# 拆分机制：wizard 出路线图、两种拆法、子任务继承意图、父任务收尾、续跑取就绪项；explore 并入 design

- target: skills/taskrail
- mode: update
- patch: 20261021-204720-decompose-rolling
- risk: high
- status: proposed

## Intent

task 系列复审第 3 步，也是用户选定的三步走的最后一步。复审发现复杂任务拆成很多子任务时有几处卡点：拆分只有一份附录 large-scope.md，要到 design 之后才发现要拆；每个子任务都从头走 explore → design → approve，human 模式下每个子任务各停一次；父任务没有收尾条件；resume 只按最近更新挑任务。本 patch 做这几件事：

1. **wizard 第 5 步「拆分」**：只对 full 档，默认不拆。不拆时不留痕迹，这就是留白。要拆就把路线图写进 plan.md，每项写一句话目标、子判据、依赖。human 模式在 wizard 定稿那一次停里一起看路线图（一行一项），不新增停点。goal 模式的审阅者另核三条：子判据合起来覆盖总判据、彼此不重叠、依赖无环。这三条同时写进闸口前自查和严重级。原第 5、6 步顺延为 6、7。
2. **large-scope.md 重写为拆分细则**，两种拆法写死：
   - 同一份交付、能在同一条分支上合入的，做成一个 driver 下的切片，这是默认做法。
   - 要分别交付或在不同修改仓、且互不用对方代码的，才拆成子任务。
   - 有代码依赖就是切片；只拆一层；有子任务时父任务自己不实现。
3. **子任务继承父任务**：父任务确认过的意图加路线图里自己那一行，就是子任务的意图，不重跑意图确认。子任务的 wizard 不停。方案没超出路线图那一行的范围和子判据时，approve 也不停，`APPROVED.md` 注明「在父任务路线图范围内」。超出范围或要改子判据，才按 approve 行停。
4. **父任务收尾**：父任务只持意图、路线图和总判据，wizard 定稿后进 `phase: apply` 推进子任务。子任务全部 done 后，按 done.md 验一次总判据，结果写在父 `TASK.md`「验证」节。过了父任务才 done，然后发一次完成通知（每个子任务的分支各一行），整树同轮归档。done.md 第 1 条补上父任务的验证落点。
5. **续跑**：resume 报「N 个里做完了 M 个」和正在做哪个。用户说「继续」时，取依赖已满足、还没做完的下一项，正在做的优先，不按最近更新挑。goal 模式下项与项之间不停；真阻塞只停依赖它的项。
6. **explore 并入 design**：design 分两步，第一步 grill，第二步写方案，两步都不停人。
   - phase 枚举去掉 `explore`，旧任务的 `phase: explore` 按 `design` 读。
   - `explore-design.md` 改名为 `design.md`，grill 纪要落 `design/grill.md`（旧任务的 `explore/` 照读）。
   - 路线图长时，design 写到能批的程度就行；还没就绪的项，细节等轮到它时按当时的代码补。
7. 切片在 driver 里怎么滚动展开、片间检查点、逐片提交，写在 taskflow（同 id patch）。本 skill 只在契约和 large-scope 里放指针。

非目标：
- 不改判据规则、意图变更规则和真阻塞清单。
- 不改 `check_handoff.py`：子任务的 slug 写 `{parent}/{sub}`、driver 名取末段，第 1 步已经支持。

## Conflict check

- phase 枚举有变化：已有任务里的 `phase: explore` 按 `design` 读（契约「流程」里的兼容行），下次写 `TASK.md` 时改成新值。
- 同轮 patch：
  - taskflow：滚动展开、逐片提交、片间检查点。
  - agent-roster：Complex 轨道的「wizard / explore」改为「wizard 与 grill」。
- 仓级文件同步流程串和拆分说明：README、AGENTS、`docs/task-flow/README.md`。
- 另一会话改过 done.md，改动已暂存。本 patch 只在第 1 条末尾追加半句，应用前逐文件核对基线一致。

## Rationale

- **拆分在 wizard 决定**：判据要分几块验，在意图确认后就看得出来，不该等到 design 之后才当意外处理。
- **拆法收成两种**：写死「有代码依赖就是切片」，子任务之间就不会互相等对方还没合入的代码。
- **子任务继承意图、范围内不停**：human 模式下拆成 N 个子任务，也不多出停点。
- **父任务单独收尾**：有了自己的完成条件，整棵任务树才闭环。
- **explore 并入 design**：explore 本来就不停人，产物和意图摸底、design 高度重叠。并成 design 第一步后，少一个 phase，也少一次文件跳转。

## Files

- `skills/taskrail/SKILL.md`
- `skills/taskrail/references/{contract,phase-wizard,large-scope,confirm-protocol,approve,handoff,intent,ledger,templates,user-report,done}.md`
- `skills/taskrail/references/explore-design.md` 改名为 `design.md`
- `skills/taskrail/evals/cases.yaml`：改 2 条，新增 7 条
- `skills/taskrail/tests/`：改 7 份，新增 `test_decompose_contract.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：
  - `git diff --check`
  - `python3 -m pytest skills tests -q`
  - `make check-style`、`make check-names`
  - evals YAML 可解析
