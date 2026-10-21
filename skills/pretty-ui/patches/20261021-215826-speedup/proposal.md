# 提速：方向说决定、截图分档、单一停止标准、按需加载与阅读页模板

- target: skills/pretty-ui
- mode: update
- patch: 20261021-215826-speedup
- risk: medium
- status: proposed

## Intent

用户反馈用 pretty-ui 生成页面慢。复审定位三处主因：方向阶段要么停下问用户、要么在 goal 模式下照样写三个方向并做跨方向差异检验，还要上网截 2–3 家标杆的首屏与控件；评审循环每轮重截全视口全状态，制作者与评审者各扫一遍规则，停止标准在 SKILL.md、critique.md 与 taskrail 之间不一致；page 模式为几小段整份读 direction / critique / system，交付前还读开发用的 evals。

本轮改变的行为：

- 方向由本 skill 自选一个并用陈述句说决定，同轮接着做；用户点名要多个方案时才出三个候选（差异检验只在这时跨候选做）。system 的缺项也自定，不再问一轮。
- 标杆截图降到 1–2 家首屏，兼作隔离评审的参照集。
- 单组件打磨、小范围改版走 build 轻量：轻量方向卡（定义上移到 SKILL.md）、基础档截图、自查。
- 看图拆出 `references/evidence.md`，分基础档 / 状态档 / 复审档；复审只截问题涉及处，状态档交付前截一次。
- 派隔离评审时制作者只做减法、眯眼与检查结果，完整扫查和问题表交给评审者。
- critique.md「迭代与停止」成为唯一停止标准：结论“通过”才收敛，同一问题连续两轮没改好就停。
- 新增 `assets/reading-page.html` 起手模板（字体栈唯一真源），`check_page.py --offline` 零报错零提示。
- page 模式发现同主题时不停下：照常写独立页，归类方案写进交付说明，已有文件不动。
- SKILL.md 去掉运行时读 examples / evals，只留 skill-upgrader 指针；build 每步补“完成”判据；铁律标规则号、阈值以 rules.md 为准。

保持不变：goal 模式不停下，由另一个模型对照参照页审改前改后截图；human 模式评审后把截图交给用户确认；不可逆动作（移动、覆盖）默认不做。

非目标：不改脚本逻辑、规则条目与严重度；不改 role-based-reviewer、taskflow。

## Conflict check

- taskrail `done.md` 引用 critique.md「第 1 节」「第 3–4 节」与 direction.md 第 6 节的轻量卡：同轮出 `skills/taskrail/patches/20261021-215826-pretty-ui-speedup/` 改指 evidence.md、critique.md 节名与 SKILL.md「轻量方向卡」，`confirm-protocol.md` 加一句观感验收以 critique「迭代与停止」为准。
- role-based-reviewer 链接 rules.md、taskflow evals 提到 direction.md：路径未变，不需改。
- html-diagram 是收录的上游文件：只改 frontmatter description 为正向表述，NOTICE 同步说明。

## Rationale

- 实测字节：build 制作方读入由约 61.5 KB 降到约 39.5 KB（build 轻量约 19 KB）；page 模式由约 63 KB 降到约 27 KB（含 5.6 KB 模板）。
- 少一整轮人工往返（独立使用时的方向提问与 system 提问），goal 模式少写两份方向与线框；每轮截图从最坏约 22 张降到 4 张加涉及处。
- 停止标准统一后，P1-only 的“需改”在 pretty-ui 与 taskrail 判定一致，避免多跑一轮。

## Files

- `skills/pretty-ui/SKILL.md`：路由加 build 轻量；方向说决定；每步完成判据；轻量方向卡；看图与确认方式；按需读取加 evidence.md、模板；自进化缩成一句指针
- `skills/pretty-ui/references/evidence.md`：新增（由 critique §1 拆出并分档）
- `skills/pretty-ui/references/critique.md`：删 §1、重编号；自查分派评审 / 不派评审；迭代与停止成为唯一标准
- `skills/pretty-ui/references/direction.md`：标杆 1–2 家首屏兼参照集；单方向差异检验 + 「出多个候选时」；§8 说决定；轻量卡改指 SKILL.md
- `skills/pretty-ui/references/system.md`：§2 缺项自定；字族指向模板；布局行长指向 T2
- `skills/pretty-ui/references/page.md`：从模板起手；同主题不重组；看图改指 evidence.md
- `skills/pretty-ui/references/rules.md`：约定冲突时约定先行并写明
- `skills/pretty-ui/references/html-diagram/REFERENCE.md`、`NOTICE.md`：description 正向化与说明
- `skills/pretty-ui/assets/reading-page.html`：新增
- `skills/pretty-ui/tests/*.py`、`skills/pretty-ui/evals/cases.yaml`：同步

## Validation

- 应用前：`git apply --check --recount`（仓库外干净副本）
- 应用后：`git diff --check`；`~/.local/bin/pytest -q`；`make check-names`；`make check-style`；`check_page.py --offline assets/reading-page.html`；`contrast.py --matrix` 校验模板亮暗两套配色
