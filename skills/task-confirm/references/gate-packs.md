# 交付类别门包（唯一真源）

本表回答「哪类交付、用哪套门、拿什么当基准、谁审、没覆盖怎么办」。taskrail / taskflow / task-explore 只**引用**本表，不另写第二份；新增交付类别或门时改本文件。

## 通则

1. **基准物** = 标准 / 契约定稿 / 冻结基线。**禁止把外部产品或参考实现当验收基准**；外部参照（风格、架构、交互）只作一次性输入被吸收；参照集仅用于「可指认件的差值」，不作地板判定。
2. **门包条目三分**：可自动化（落脚本、可复跑）· 运行态（须真实运行证据）· 主观（须指到参照集或项目自有标准的可指认件）。
3. **未覆盖即降级**：任一条目未验证、未提供证据 = 生产性降级，按 [quality-profile.md](quality-profile.md) 定级登记；不得以「看起来没问题」通过。
4. **执行器绑定**：命中「必载专家能力」的类别，评审 MUST 以 `mode=review` + 完整 `roles=` + 审阅边界结构化调用 `role-based-reviewer`；降级须写明不可用原因（见 SKILL.md「执行器绑定」）。

## Web UI

- **基准物**：无障碍标准（WCAG 2.2 AA 作地板）+ 交互启发式清单（Nielsen 类压缩版）+ **交付项目根已冻结的 `design-system/v1` Active Instance**（`design-system.yaml` 的 `status: frozen`，及 contract / binding / projection 三条 digest）+ Gallery / 冻结视觉基线（Gallery 证据或等价 current-build 截图）。Active Instance 由仓外 `ui-template-design` 产出（有参照源时可先 `ui-template-author` 再领养）；task* 只认指针与 digest，不在 `tasks/` 内复制 tokens / primitive 精确值。`ui-skills-root` 与零散 craft skill **不**替代 Active Instance。
- **Active Instance 档位门**（硬门，与基准物同级）：
  - **medium / complex**：进入 `approve` 冻结前必须已有 frozen Active Instance；缺失则停下，移交 `ui-template-design`（0–9 至 freeze），不得用散文式「组件约定」顶替。
  - **simple**：优先 frozen Active Instance；否则仅当「`ui-template-apply` adopt published package」且质量画像已登记并**确认**显式降级时方可放行；无降级登记不得放行。
- **必载专家能力**：`role-based-reviewer roles=design`（别名 `uiux`）。审阅边界 MUST 附 Active Instance 根路径、三条 digest、Gallery（或等价）证据指针。
- **可自动化门**（落仓库脚本；能跑 DS runtime 时优先下列命令，缺工具按「未覆盖即降级」登记）：
  - Active Instance：`check_active_instance.py validate <active-root> --kind active`（或项目约定等价）通过，且三条 digest 与 `design/contract.md` / driver 指针一致；
  - 设计约束扫描：`scan_design_constraints.py <output-root>`（或项目约定等价）通过；
  - token 纪律：diff 中不得新增硬编码色值 / 字号 / 字重 / 圆角 / 间距（须映射到 `core/tokens.yaml`）；
  - 无障碍：键盘可达、`:focus-visible` 存在、icon-only 有 `aria-label`、异步反馈走 `aria-live`、表单控件有关联 label；
  - 状态覆盖：数据区四态（loading / empty / error / success）、交互元素态（hover / focus / active / disabled）；
  - 结构断言：≥2 个视口的布局重组断言（不是等比缩放）。
- **运行态证据**：真实浏览器交互走查（关键流程）+ 关键面截图；UI 切片经 `ui-template-apply` 时优先用其 Phase 8 current-build 证据与 Gallery。工具不可用时写明替代方法与能力边界、重估覆盖度，缺口按「未覆盖即降级」登记。
- **主观项**：视觉层次 / 密度 / 排版节奏——须指到 Active Instance Gallery、tokens 或项目标准的可指认件，否则只记 Suggestion，不得据此判不通过。
- **实现委托**：业务页实现走仓外 `ui-template-apply`（消费 frozen Active Instance 或已确认的 adopt-only）；禁止无 Active Instance（且无已确认 adopt-only 降级）直接铺业务页。改 token / pattern / page-type → `ui-template-design` `iterate`，刷新 digest 后再继续 apply。

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
