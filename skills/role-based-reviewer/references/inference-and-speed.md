# 视角推断、耗时优化与调用示例

从 SKILL.md 原句下沉（内容未改）；未指定 `roles` 需推断、大目标 review、或需要调用样例时读本文件。

## 调用示例

- `{{slash:role-based-reviewer}} roles=algo 排序分为何掉量`
- `{{slash:role-based-reviewer}} roles=engineer,sre mode=review 服务与部署变更`
- `{{slash:role-based-reviewer}} mode=review`：未指定 `roles` 时默认 engineer（受门 2）

- 工作流调用：`roles=product,design,engineer mode=review` 并随附完成判据 / 质量画像 / 显式降级 / 审与不审范围（不增删角色、不反问）
- 异源评审调用：`roles=design mode=review model=<与实现不同的模型>`；跨端点：`roles=product,design,engineer mode=review endpoint=<host>/<kind>`

## 视角推断（受门 2 约束）

用户显式指定的 `roles` 优先，不再增删；调用方按自身规则传入的固定 `roles` 等同显式指定，同样不增删。下列推断只在既无用户点名、也无调用方传入时进行：

- **默认只 engineer**。不要默认带 qa / product / design。
- 额外角色要有问题或 diff **主体**上的强信号，不是「文件列表里出现过」：
  - 审查目标就是测试/可测性 → + **qa**
  - 目标就是 UI 视觉/交互/无障碍（不是顺便改了样式）→ + **design**（即 uiux）
  - 目标就是需求/方案文档 → + **product**
  - 可选角色（`algo` / `data` / `sre` / `ops` / `biz` / `skill`）不推断，只在用户点名或调用方传入时生效。
- 推断结果将超过 2 个角色：停下来问，不猜。已传入的 `roles` 属指定而非推断，不在「先问」之列。
- 项目里没有对应域（无模型、无数仓、无对外对接）时，对应角色直接不加。

推断结果写在报告开头（启用了哪些、为什么）；用户纠正后以用户为准。

## 耗时优化（大目标必读）

- **先摸规模**：`git status --short`、`git diff --stat` 或目录文件清单，再决定读多少
- 大目标 **按模块分组** 理解意图，只对核心文件抽样精读；lockfile / 生成物 / vendor / 大资源不读内容
- 每个角色只盯本职高价值问题，不要逐行复述代码，不要为求全打开几十个文件
- 支持 subagent 时，可按角色并行派发（模型默认继承调用方，显式 `model=` 时从其值；跨端点用 `endpoint=` 走 agent-roster），各自返回分级结论后汇总去重；派发策略见「流程」第 4 步
