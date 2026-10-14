# 交付类别门包（唯一真源）

本表回答「哪类交付、用哪套门、拿什么当基准、谁审、没覆盖怎么办」。taskrail / taskflow / task-explore 只**引用**本表，不另写第二份；新增交付类别或门时改本文件。

## 通则

1. **基准物** = 标准 / 契约定稿 / 冻结基线。**禁止把外部产品或参考实现当验收基准**；外部参照（风格、架构、交互）只作一次性输入被吸收；参照集仅用于「可指认件的差值」，不作地板判定。
2. **门包条目三分**：可自动化（落脚本、可复跑）· 运行态（须真实运行证据）· 主观（须指到参照集或项目自有标准的可指认件）。
3. **未覆盖即降级**：任一条目未验证、未提供证据 = 生产性降级，按 [quality-profile.md](quality-profile.md) 定级登记；不得以「看起来没问题」通过。
4. **执行器绑定**：命中「必载专家能力」的类别，评审 MUST 以 `mode=review` + 完整 `roles=` + 审阅边界结构化调用 `role-based-reviewer`；降级须写明不可用原因（见 SKILL.md「执行器绑定」）。

## Web UI

- **基准物**：无障碍标准（WCAG 2.2 AA 作地板）+ 交互启发式清单（Nielsen 类压缩版）+ **交付项目根已冻结的 `design-system/v1` Active Instance**（`design-system.yaml` 的 `status: frozen`，及 contract / binding / projection 三条 digest）+ Gallery / 冻结视觉基线（Gallery 证据或等价 current-build 截图）。Active Instance 由 task* 的 design 阶段在交付仓内建立并 freeze（有参照源时先从参照源提炼 tokens / primitive）；task* 只认指针与 digest，不在 `tasks/` 内复制 tokens / primitive 精确值。`ui-skills-root` 与零散 craft skill **不**替代 Active Instance。
- **Active Instance 档位门**（与基准物同级；按档调度，保任务速度）：
  - **medium / complex**：进入 `approve` 冻结前必须已有 frozen Active Instance；缺失则停下，回 design 阶段建立 Active Instance 至 freeze，不得用散文式「组件约定」顶替。
  - **simple**：优先 frozen Active Instance；否则「adopt-only：沿用交付仓已有组件库 / 样式体系」且质量画像已登记并**确认**显式降级即可放行；无降级登记不得放行。adopt-only **豁免** Active Instance，并按下方「档位调度」豁免重型证据门。
- **必载专家能力**（按档）：
  - **medium / complex**：`role-based-reviewer roles=design`（别名 `uiux`）。审阅边界 MUST 附 Active Instance 根路径、三条 digest、Gallery（或等价）证据指针。
  - **simple**：不强制 `roles=design`；实现者自检 quality floor（破坏性确认、键盘可达、focus 可见）即可。需要时再点名 design 角色，且该角色只扫 floor（见 `role-based-reviewer` design 角色「调用范围与速度」）。
- **可自动化门**（落仓库脚本；能跑 DS runtime 时优先下列命令，缺工具按「未覆盖即降级」登记）：
  - Active Instance：项目约定的 Active Instance 校验（`design-system.yaml` 为 `status: frozen`、三条 digest 可复算）通过，且三条 digest 与 `design/contract.md` / driver 指针一致；
  - 设计约束扫描：`scan_design_constraints.py <output-root>`（或项目约定等价）通过；
  - token 纪律：完成时共享色、字、间距在 `core/tokens.yaml`。代表页实现过程中的暂存值在回写前保留在该页；完成时仍留在页面里的共享值视为未完成。
  - 无障碍：键盘可达、`:focus-visible` 存在、icon-only 有 `aria-label`、异步反馈走 `aria-live`、表单控件有关联 label；
  - 状态覆盖：数据区四态（loading / empty / error / success）、交互元素态（hover / focus / active / disabled）；
  - 结构断言：≥2 个视口的布局重组断言（不是等比缩放）。
- **运行态证据（按档调度）**：[`scripts/ui_evidence_check.py`](../scripts/ui_evidence_check.py)
  - **complex（硬门）**：对关键路由跑出 `evidence/ui/<run>/report.json` + PNG，且 exit 0：≥2 视口（必含 1280x800 与 375x812）、axe-core WCAG 2.2 AA 无 serious / critical、键盘 Tab 焦点顺序与焦点可见、manifest 声明的 loading / empty / error / success 四态逐一截图（不适用须在 manifest `not_applicable` 写理由）。manifest 随交付仓保存、可复跑；代码变更后旧 report 作废重跑。playwright / axe-core 缺失时脚本 exit 2 阻断，或经用户确认登记 A 类降级。
  - **medium（硬门，可精简）**：同脚本 exit 0，但允许精简 manifest——关键路由 ≥1、视口至少 1280x800（移动视口 SHOULD）、四态可批量 `not_applicable` 并写一句理由。current-build 截图与 Gallery 是补充。
  - **simple（SHOULD，非硬门）**：不强制跑 `ui_evidence_check`；未跑时在质量画像登记 **B 类**显式降级即可放行（不得静默跳过不登记）。quality floor（破坏性确认、键盘可达、focus 可见）由实现者自检写入验证记录。
- **design 评审文件（按档）**：
  - **medium / complex（硬门）**：评审者（≠ 实现者）基于 report 与截图写评审文件，frontmatter 含 `roles: design`、`reviewer`、`implementer`、`report: <report.json 路径>`，正文逐条 findings + disposition；`ui_evidence_check.py --validate-review <file>` 须 exit 0。
  - **simple**：不强制 design 评审文件；有 report 时仍可选用 `--validate-review`。
- **主观项**：视觉层次 / 密度 / 排版节奏——medium/complex 由 design 评审文件基于截图逐条判定；simple 不强制。代表页源码修订记录是过程记录，**不单独构成完成证据**——自述不算证据。Gallery 与 digest 只证明系统未漂。
- **实现方法（按档）**：
  - **medium / complex**：业务页实现消费 frozen Active Instance。先按代表页 two-pass（先定 design thesis 与壳层，初稿后再修订一轮）实现并修订一条主流程代表页，其余表面从该页长出。无 Active Instance 时先建立再写页面。改共享 token / pattern / page-type → 回 design 修订 Active Instance 并重新 freeze。
  - **simple / adopt-only**：不强制代表页 two-pass 与 Gallery；直接改业务页，遵守既有组件库 / 样式体系即可。

## 服务 / 后端

- **基准物**：接口契约（schema / 协议）+ 既有错误语义与状态码约定。
- **必载专家能力**：`role-based-reviewer roles=engineer`（涉及并发 / 持久化 / 迁移时加对照面）。
- **可自动化门**：契约测试（请求 / 响应形状）、类型检查、依赖边界检查、迁移幂等与重放可复跑。
- **运行态证据**：真实进程启动 + 关键路径端到端（含失败路径）；负载 / 并发假设按画像「规模与运行假设」验证，不验证则登记降级。
- **主观项**：不适用（以契约与可观测性判定）。

## 数据 / 口径

- **基准物**：口径定义（指标含义 / 时间窗 / 维度）+ schema / 血缘约定。
- **必载专家能力**：`role-based-reviewer roles=data,engineer`。
- **可自动化门**：schema 校验、幂等 / 重放、口径单测（样例输入 → 期望口径值）。
- **运行态证据**：受控样本或真实数据源上的端到端；取不到数据时登记降级。
- **主观项**：不适用。

## 部署 / 密钥

- **基准物**：最小权限 + 回滚路径 + 密钥不落盘 / 不入仓库。
- **必载专家能力**：`role-based-reviewer roles=sre`（按需 + `ops`）。
- **可自动化门**：配置校验、密钥扫描、依赖 / 镜像来源检查、回滚脚本可执行性。
- **运行态证据**：本地或预发演练；禁止以生产作为首次验证。
- **主观项**：不适用。

## 文档 / Skill

- **基准物**：结构规范 + 契约测试（文本锁）+ 引用完整性。
- **必载专家能力**：`role-based-reviewer roles=skill`（按需 + `product`）。
- **可自动化门**：结构校验、引用 / 链接存在性、契约测试**含决策用例**。
- **运行态证据**：文档类不强制；Skill 类须有决策 / 路由用例覆盖。
- **主观项**：可读性按项目标准，逐条指认。

## 与评审执行器的绑定

| 交付类别 | 必载评审 | 异源要求 |
|---|---|---|
| Web UI | `role-based-reviewer roles=design` | 复杂档 SHOULD 异源（`model=` 或 `endpoint=`） |
| 服务 / 后端 | `roles=engineer`（+ 并发 / 持久化对照面） | 同上 |
| 数据 / 口径 | `roles=data,engineer` | 同上 |
| 部署 / 密钥 | `roles=sre`（按需 + `ops`） | 同上 |
| 文档 / Skill | `roles=skill`（按需 + `product`） | 同上 |

未按本表加载而退普通 subagent：须写明不可用原因并记入评审意见路径，否则按退出点「评审降级未记录」不放行。
