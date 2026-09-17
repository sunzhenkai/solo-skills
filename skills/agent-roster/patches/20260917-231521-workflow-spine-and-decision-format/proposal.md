# 补上委派主干顺序、decision.md 格式与失败处置

- target: skills/agent-roster
- mode: update
- patch: 20260917-231521-workflow-spine-and-decision-format
- risk: medium
- status: proposed

## Intent

正文此前是五个平行小节（路由 / 委派 / 回收 / 留痕 / 固化），执行顺序、`decision.md` 的落盘位置与格式、失败后的处置都要靠读者自行推断。本轮补齐四处：

1. **主干顺序**：新增「一次委派的完整顺序」六步清单，把五个小节串成可勾选的执行序列，并点明第 2 步（先写决策）与第 6 步（写完 Trace 才查固化）就是两条不变量所在。
2. **Run 目录与 decision.md**：把 `<run-id>` 的生成规则与 `mkdir` 提到路由第 4 步，并定义 `decision.md` 的四个必填项（候选 / 选中 / 理由 / 依据）。
3. **失败处置**：回收段新增「失败、超时与返工」，按三类失败给出不同动作；不变量同步加一条。
4. **目录可见性**：说清运行位置只有 `SKILL.md`、`references/`、`scripts/`、`examples/`，并给 `examples/` 补一行台账。

非目标：不改选人算法、不改权限两档、不改 `acpx` 门禁、不动探测脚本、不新增 references 文件。

## Conflict check

**顺序空洞（本轮修掉的实际 bug）**：正文要求「在执行之前」把决策写进 `~/.cache/agent-roster/runs/<run-id>/decision.md`，但 `run_dir` 的 `mkdir` 只存在于 `delegation-contract.md` 的委派命令里，`<run-id>` 的构造规则也只在那段 bash 中。按正文顺序执行会往一个尚不存在的目录写文件。本轮把建目录移到路由阶段，契约里的命令改为复用 `$run_id`，两处不再各自造一个 Run 目录。

与既有门禁不冲突：`acpx` 四态检查仍在第 3 步，未受影响；探测分层、权限两档、固化门槛 2 次均未改动。新增清单第 6 步与「固化」小节的「写完 Trace 之后立即检查」一致，不构成第二套时机。

**与 self-upgrade 的冲突（已避让）**：实测安装副本只有 `SKILL.md`、`references/`、`scripts/`、`examples/`，`evals/`、`experience/`、`patches/` 不在运行位置。因此不注入「运行时参考 evals / 记录 experience」的标准自进化正文——那会是一条执行不了的指令。`examples/` 虽随安装分发但目前为空，按禁止伪造历史的约束也不引导去读。本轮只把目录可见性这一客观事实写清。

## Rationale

三处缺口的共同成因是：正文按**主题**分节，而执行是按**时间**展开的。主题分节下，每个小节各自正确，但小节之间的先后、以及某一步失败后该退回哪一步，没有任何一句话负责。清单补的就是这条时间轴。

`decision.md` 是本 skill 唯一贯穿始终的载体——不变量「先写后执行」靠它，固化时的「为什么选它」也必须从它原样搬运。`endpoint-schema.md` 和 `trace-format.md` 都有专门的格式文档，只有它没有，于是每次写出来的字段都不一样，固化时就搬不动。四个必填项直接写进正文而非新开 reference，是因为字段少，且它必须在路由途中被看到。

失败处置的缺失会让编排者默认重跑。三类失败里只有一类适合重发，另外两类重发都是纯浪费——受派方没起来时重发只会再失败一次，产出跑偏时重发会拿到同样跑偏的结果。

## Files

- `skills/agent-roster/SKILL.md`：新增「一次委派的完整顺序」小节；「数据在哪」补 Example 行并改写分发说明；路由第 4 步补 Run 目录与 `decision.md` 字段；回收段新增「失败、超时与返工」；不变量加一条失败处置，并把「创作目录甚至不会被复制过去」改为点名 `experience/`、`evals/`、`patches/`——`examples/` 实际会被复制，原表述与本轮新增的 Example 行相互矛盾。
- `skills/agent-roster/references/delegation-contract.md`：委派命令复用路由阶段建好的 `$run_id`，不再自己 `mkdir`。

## Validation

- `git apply --check --recount` 通过。
- 应用后核对：正文出现六步清单；路由第 4 步含 `run_id` 构造与四个必填项；契约中不再出现第二处 `mkdir -p "$run_dir"`；frontmatter `name` 仍为 `agent-roster`；引用的 `references/*.md` 与 `docs/adr/*.md` 路径均存在；无主机名、家目录、项目名等私有内容。
