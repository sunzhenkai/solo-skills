# P2 升级：向 taskrail 注入垂直切片、深模块接缝、前沿批量 grill 与红灯调试回路

- target: skills/taskrail
- mode: update
- patch: 20261127-004500-p2-matt-engineering-core
- risk: medium
- status: proposed

## Intent

参考 Matt Pocock 工程 skill 体系，补强 taskrail 在拆解、探索、拷问、架构设计与排障 5 个核心环节的软件工程方法论：

1. **`decompose.md`**：明确垂直切片（tracer bullet）优先、禁止按技术层水平硬切，并以「单个 fresh context window 能独立闭环」为拆分粒度上限。
2. **`explore.md`**：将项目根 `GLOSSARY.md` / `GLOSSARY-MAP.md` 纳入首批必读领域语言。
3. **`grill.md`**：面向用户的重大取舍采用前沿批量发问格式（`Q1/Q2 + 推荐`，一句话批量采纳），需查环境事实的分支后台派只读探索、只阻塞下游而不阻塞独立前沿。
4. **`design.md` & `design-detail.md`**：引入深模块（deep module）、接缝（seam）与测试面先行原则（可选按 `codebase-design` 深化接口）；ADR 仅在满足「难逆 + 无上下文会困惑 + 真实权衡」三条件时以 1–3 句极简格式落盘；术语变更按 `domain-modeling` 实时维护 `GLOSSARY.md`；在 `design-detail.md` 补充高风险/多解接口的 `Design It Twice` 并行探索模式。
5. **`diagnose.md`**：将「未建出 tight & red-capable 复现命令前不读代码猜原因」设为首要纪律，补齐 Minimise（最小化复现）→ 3–5 个可证伪排序假说 → `[DEBUG-xxxx]` 探针收尾全清 → 修复后重跑未缩小原场景与“缺接缝即架构发现”（软引用可选 `diagnosing-bugs`）。

非目标：不新增固定阶段、不删除已有 `trouble-grill` / `anti-lazy` 接线、不做 P3 文件合并瘦身、不改写历史 `patches/`。

## Conflict check

- 配套 patch：`skills/taskflow/patches/20261127-004500-p2-tdd-and-seam-execution/`（在 `execution-discipline.md` 补齐接缝处单测试垂直 TDD 节奏与 `replace, don't layer`）。
- 所有外部 Matt skill（`codebase-design`、`domain-modeling`、`diagnosing-bugs`、`grilling`、`grill-with-docs`）均采用反引号按名软引用，不增加跨 skill 相对路径硬依赖，并同步登记于仓级 `README.md`「外部依赖」。
- 保持 `SKILL.md <= 8192 B`、一层直链与正向表述约束不变。

## Rationale

taskrail 此前流程编排完整但软件设计与排障方法偏泛。通过把垂直切片、深模块接缝、前沿批量提问、红灯反馈回路与单测试 TDD 分别落在对应按需加载的 `references/` 中，既不增加常驻上下文负担，又能在命中对应环节时直接提升设计与代码质量。

## Files

- `skills/taskrail/references/decompose.md`：写入垂直切片（tracer bullet）优先与单 fresh context window 闭环粒度标尺。
- `skills/taskrail/references/explore.md`：首批知识读取纳入 `GLOSSARY.md` / `GLOSSARY-MAP.md`。
- `skills/taskrail/references/grill.md`：补充前沿批量提问格式与后台查事实不阻塞独立前沿规则。
- `skills/taskrail/references/design.md`：引入深模块/接缝/测试面先行、三条件极简 ADR、实时维护 `GLOSSARY.md` 及 `codebase-design` / `domain-modeling` 软指针。
- `skills/taskrail/references/design-detail.md`：新增「两次设计（Design It Twice）」并行接口探索方法。
- `skills/taskrail/references/diagnose.md`：内化 `tight & red-capable` 反馈回路硬闸、Minimise、3–5 排序假说、`[DEBUG-xxxx]` 探针清理与缺接缝发现，并软引用 `diagnosing-bugs`。
- `skills/taskrail/evals/cases.yaml`：新增垂直切片拆解、接缝深模块/Design It Twice 与红灯调试回路 3 条评估案例。
- `skills/taskrail/tests/test_neighbor_skill_contract.py`：新增 P2 工程内核契约守卫测试。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-004500-p2-matt-engineering-core/change.patch`
- `git diff --check -- skills/taskrail`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `make check-names` 与 `make check-style`
