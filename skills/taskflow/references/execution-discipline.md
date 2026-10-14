# taskflow：执行纪律

由 [../SKILL.md](../SKILL.md)「纪律」引用。Driver 协议逐字块见 [driver-template.md](driver-template.md)。

## 进度归属

- 子 change 的 `tasks.md` 记**实现**进度，driver 的 `tasks.md` 记**编排**进度，后者必然滞后于前者。
- driver 的某条实施 checkbox 只在对应子 change 全部 checkbox 已勾、且在其 planning root 下 `openspec validate --strict --type change {task}-<slice>` 通过之后才允许勾选。
- 不持久化第二份完成度、暂缓或分支状态记录。暂缓原因写进 driver `proposal.md` 的验证记录小节。
- 已知代价：`openspec archive` 对未勾 checkbox 不设防。完成度靠上述纪律与 stock skill 的确认环节；归档前置校核见「收尾机械校核」节。

## 涉及面与交付分支

- 角色只有三个取值：`必须`（会修改）、`建议`（只读参考）、`排除`。`建议` 与 `排除` 仓保持只读。
- 切分支规则只以 [driver-template.md](driver-template.md) 的 Driver 协议逐字块为准，此处不复述。
- 模板之外的增量：部分仓已准备成功、其它仓停下时，已准备成功的仓保留现状以便重试。

## 质量画像与降级确认

- 质量画像与显式降级原文快照由上游任务描述带入 driver proposal，实施阶段不改写、不删减，只按下面规则补新发现的降级。
- 子 change 实施中发现新的生产性降级——凡比默认期望少交付的都算，改名成「技术选型」「本期简化」也一样——先按 [../../taskrail/references/quality-profile.md](../../taskrail/references/quality-profile.md) 定级。**A 类**（缩完成判据或交付面；拿不准归 A）：标 `pending`，写入 driver `proposal.md` 的验证记录，作为需要用户决策的项停下等用户，不静默接受、不自行确认。**B 类**（判据与交付面都不缩）：经审阅收敛临时确认记 `provisional`，不停机不等用户，到用户在场点（真人门、收口）集中追认。这命中 Driver 协议「一轮结束」三条件里的「需要用户决策」；不依赖该决策的其余条目仍按「一轮结束」继续。
- 执行者、子代理与审阅收敛都不算用户确认；B 类 `provisional` 是唯一例外——经审阅收敛写入，但只算临时确认，追认前不算 `confirmed`。用户点名接受该项、明确全部确认、按意图命中已列授权项（复述生效，见 [../../taskrail/references/confirm-protocol.md](../../taskrail/references/confirm-protocol.md)「授权」节）、或在用户在场点追认后，才允许勾相关验收标准 checkbox，并在验证记录把该项记为 `confirmed`，保留维度与实际选择以便追踪；追认否决按该项回滚说明处理后回降级确认门重定级。
- driver 的最终验收必须按 [references/acceptance-rubric.md](acceptance-rubric.md) 给出五维分数与证据，并满足五维均 ≥2、UI/UX 均值 ≥2.5；缺分不得勾验收标准 checkbox。

## 收尾机械校核

对 driver 执行 stock 归档**之前**，逐条机械核对（不靠记忆、不用汇总口径替代逐条说明）：

- 子 change 全勾，且各自在其 planning root 下 `openspec validate --strict --type change {task}-<slice>` 通过；driver 对应实施 checkbox 与子 change 状态一致。
- 显式降级表无 `pending`、无未追认 `provisional`。
- 每轮评审产出的 Blocker / Major 全部有 disposition（`fixed` 或 `accepted-recorded` 含理由）；无 disposition 不得判收敛、不得回填验收。
- 证据与当前产物状态一致（换代码后旧证据作废，重跑受影响层）。

**禁止 `--yes` 掩盖未勾**：`openspec archive` 报未勾时先回填真实状态，或保持未勾；**归档后记录不可回改**——未勾齐就不归档，禁止「先归档再补正」。进度归属节所述「archive 对未勾 checkbox 不设防」指的是工具不设防，设防的是本节。

## 一轮结束

「一轮结束」三条件与逐条列未勾项的规则只以 [driver-template.md](driver-template.md) 的 Driver 协议逐字块为准，此处不复述。

模板之外的增量：不因一项卡住就整轮停下；不把未完成项勾成完成；不用「某 change 还剩 3 项」这类按 change 汇总的数量代替逐条说明。

「需要用户决策」结束一轮时，按 [../../taskrail/references/suspension.md](../../taskrail/references/suspension.md) 的挂起五元组呈现（等待项、授权形状、阻塞面、非依赖面、恢复触发）：依赖该决策的 checkbox 停，不依赖的继续按「一轮结束」推进，不整轮停摆。用户输入到达先比对授权形状——逐字点名或意图命中（复述生效）都算，命中即恢复对应条目，未命中重申仍停，不写成选项列表。

## 并行执行

有多 agent / 子代理能力时，对**无未完成依赖、范围不重叠**的单位优先并行；没有该能力则主会话串行，其余纪律不变。并行只改变执行方式，完成度仍只认 checkbox，不另建账本。

两层都可以并行：

| 层 | 单位 | 可以并行 | 必须串行 |
|----|------|----------|----------|
| change | 子 change `{task}-<slice>` | 落在不同必须仓，或主会话已确认实现范围不重叠 | 同一工作树且可能改同一批文件或互相依赖契约；准备段切分支；收尾段回归 / 回填 / 提交 / 归档 |
| task | 同一 change 的 checkbox | 互不依赖且文件范围不重叠 | 有先后依赖、共享同一文件、或需要用户决策 |

每个子代理只领一个单位（一个子 change，或同一 change 内一组已声明不重叠的 checkbox），并同时满足：

- 在该单位的 planning root 下执行，且显式给出 change name
- 只改自己范围内的代码与自己的 `tasks.md` checkbox
- 不勾 driver 编排项（仍由主会话在子 change 全勾且 `validate --strict` 通过后勾）
- 不发明等价命令，不扩大到 `建议` / `排除` 仓的写入

主会话负责派发、汇总、处理冲突与未勾原因。子代理失败或超时不是整轮结束理由，按「一轮结束」继续其余独立项。

两条派发前置纪律：

- **旗舰先行**：交付类别命中门包、且属首次实现或大改时，先只派一个**旗舰切片**——按契约文件把该类交付的代表面做到全量（含门包要求的可自动化门与运行态证据），经门包「必载专家能力」评审通过后才允许并行铺开；旗舰切片同时是其余切片的复制样板。无样板可循（新交付类别、新页面族）时不得直接并行。
- **同类失败升级**：**≥2 个单元报告同一类失败**（同一契约错误、同一类门失败、同一类返工）时，判定为**契约或计划缺陷**：停并行、回 `design` 修契约，再重新派发；不得按各自 bug 逐个修。

并行飞行期间主会话仍可写共享文件，两条协调纪律：

- 改共享面必广播：修改 shared 组件签名、共享类型、编排文件等子代理会读会引用的文件前，立即 `write agent://all`（或定向 `write agent://<id>`）广播改动点、影响面与子代理范围是否调整；收到广播的子代理按修正后契约继续，不视为打断。
- 补写已分配文件前核对范围：动手写文件前先对照派发分配表确认不在任一在跑子代理的范围内；已写入则立即定向通知该子代理收敛其范围。

## 实现者输入

默认正常交付：按 [references/implementer-isolation.md](implementer-isolation.md)，实现者必须拿到质量画像或保留语义的子范围裁剪、相关验收要求与运行约束；完整 rubric 和跨范围审阅意见仍由审阅者持有。普通任务不得盲派。

交付面命中 [../../taskrail/references/gate-packs.md](../../taskrail/references/gate-packs.md) 的类别时，实现者输入除上述外 MUST 再携带三件，缺任一件不得派发：

- **契约文件**：共享面（接口、类型、primitive、目录与命名、样板切片）已冻结的产物指针；并行派发前必须已存在，冻结后漂移走「并行执行」的共享面广播纪律。Web UI：指针 = Active Instance 根路径 + contract / binding / projection 三条 digest（与 handoff 载荷一致）。
- **门包**：适用交付类别的门包条目（可自动化门 / 运行态证据 / 主观项）+ 本切片负责产出的证据清单。
- **证据要求**：证据须为可复跑命令与输出、断言脚本或截图 / 录屏，并绑定产物状态（提交号或 dirty 摘要）；未覆盖条目按 taskrail 确认协议「未覆盖即降级」登记。Web UI：优先 `ui_evidence_check` current-build 证据与 Gallery。

## Web UI 实现委托

交付类别为 Web UI 时：

- UI 切片（含旗舰切片）的页面实现 MUST 消费 driver 所记 frozen Active Instance（或已确认的 adopt-only）。先按代表页 two-pass 方法（先定 design thesis 与壳层，初稿后再修订一轮）实现并修订一条主流程代表页，其余表面从该页的壳层与字阶长出。功能切片不代替这次修订。
- 无 Active Instance 且无已确认 adopt-only 降级时，先建立 Active Instance 再写页面。
- UI 切片完成 = `ui_evidence_check.py` report exit 0 + design 评审文件 `--validate-review` exit 0（见 gate-packs「Web UI」）；`ui-skills-root` 与零散 craft skill 不替代代表页 two-pass 与 Active Instance。
- 发现须改 token / pattern / page-type / binding 语义：停并行，回 design 阶段修订 Active Instance 并重新 freeze，刷新 digest 与 `design/contract.md` / driver 指针后再派发；不得在 apply 内改 core。
- 并行派发前契约 = 三条 digest；漂移走共享面广播，且须与 Active Instance freeze 再对齐。

只有任务显式标记 benchmark / regression 时才盲测复跑：实现者只拿同一份样例/需求原文与运行约束，不拿画像、rubric、期望清单或审阅意见；复跑不追加事后提示。
