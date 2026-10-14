# task* 术语表（唯一真源）

taskrail / task-explore / taskflow 共用。其他文件出现下列术语时按本表理解，只链接本表，不另写定义；与 [contract.md](contract.md) 冲突时以 contract.md 为准并回改本表。

## 任务与阶段

| 术语 | 含义 | 不要写成 |
|------|------|----------|
| 完成判据（`criterion`） | 一条可检查的话，判断任务是否做完；原文逐字传递 | 目标、objective |
| 交付标准 | 判据之外、本任务应有的交付面要求，每条可检查；没有写「无」 | 质量目标 |
| 档位（`tier`） | simple / medium / complex，由 wizard 判定，下游不重判 | 完成程度 |
| `phase` | 契约封闭枚举 `wizard \| explore \| design \| approve \| propose \| apply \| archive \| done`；命令名不得写入 | — |
| `handed-off` | `TASK.md.status`：已交接 taskflow，任务仍在 `ongoing/`，之后进度只认 checkbox | 归档 |
| 交接载荷 | `TASK.md`「## 交接」节：判据原文、交付类别、适用门包、契约指针（Web UI 含三条 digest）；`check_handoff.py` 只认它 | 口头交接 |
| driver | OpenSpec change `{task}-driver`，只编排子 change；子 change 为 `{task}-<slice>` | 第二份任务账本 |

## 确认与审阅

| 术语 | 含义 |
|------|------|
| 完成程度 | 审阅返回的高 / 中 / 低；只有「高」且无未消 P0/P1 才收敛 |
| 退出点 | 必须停下、把决定交回人的条件（见 [confirm-protocol.md](confirm-protocol.md)） |
| 授权 | 用户明确接受某条退出点已点名的动作；单独「继续」不算 |
| 门包 | 交付类别（Web UI / 服务 / 数据 / 部署密钥 / 文档 Skill）对应的可自动化门 + 运行态证据 + 主观项 + 必载专家能力，真源 [gate-packs.md](gate-packs.md) |
| 未覆盖即降级 | 门包条目或判据任一项未验证 = 生产性降级，须登记，不得以「看起来没问题」放行 |

## 质量画像与降级状态

| 状态 | 谁能写 | 含义 |
|------|--------|------|
| `pending` | 执行者登记 | 未确认；A 类（缩判据或交付面）挂 `pending` 即停 |
| `provisional` | 审阅收敛（仅 B 类） | 临时确认，须到用户在场点追认，完成门不认 |
| `confirmed` | 只有用户 | 点名接受、全部确认或在场追认 |

评审意见 disposition 只取两值：`fixed`（已修）/ `accepted-recorded`（接受并记录理由）。Blocker / Major 无 disposition 不得收敛。字段细则见 [quality-profile.md](quality-profile.md)。

## Web UI

| 术语 | 含义 | 不要混用 |
|------|------|----------|
| Active Instance | 交付项目根 `design-system/v1` 下的设计系统实例，由 task* 的 design 阶段在交付仓内建立并 freeze | 组件约定、样式说明 |
| freeze / frozen | Active Instance 的 `status: frozen`：契约已冻结，apply 只消费不改 core | 定稿 |
| 三条 digest | contract / binding / projection 三个摘要；写入 `design/contract.md` 与 driver，用来判断是否漂移 | 版本号 |
| adopt-only | simple 档无 Active Instance 时直接沿用交付仓已有组件库 / 样式体系；须登记并确认显式降级，豁免 Active Instance，并按 gate-packs 档位调度豁免重型证据门（`ui_evidence_check` / design 评审改为 SHOULD） | — |
| 代表页 | 一条主流程的代表页面：按代表页 two-pass 方法先实现并修订，其余表面从它长出 | 旗舰切片（并行层面的概念，代表页是其 UI 产物） |
| 旗舰切片 | 命中门包时先单独派出的首个切片，做到全量并过评审后才并行 | — |
| Gallery | 交付仓内的组件 / 页面展示页证据；只证明系统未漂，不替代 `ui_evidence_check` | 截图证据 |
| `ui_evidence_check` | [`scripts/ui_evidence_check.py`](../scripts/ui_evidence_check.py)：多视口截图 + axe WCAG 2.2 AA + 焦点走查 + 四态，出 `report.json`；完成门只认它 exit 0 | 自评 |
