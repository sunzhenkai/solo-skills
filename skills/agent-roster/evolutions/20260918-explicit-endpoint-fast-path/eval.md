# Evaluation

## Regression

- 候选稿相对生产稿只有 4 行新增、0 行删除，既有硬规则没有被改写。
- 对照 `evals/cases.yaml` 的 10 条 case 逐项检查：
  - `decision-before-execution`：主流程第 2 步仍在第 3 步之前；快速路径只允许压缩字段，不移动顺序。
  - `no-data-in-repo`：数据位置与运行时只读规则未动。
  - `read-only-by-default`：权限两档未动。
  - `empty-routing-rules`：快速路径仍读 `routing.md`，为空时仍跳过、不编规则。
  - `trace-threshold`、`promotion-threshold`：留痕与固化门禁未动。
  - `probe-distinguishes-failures`：探测规则未动。
  - `no-scoring`：未引入评分或枚举分类。
  - `no-self-delegation`：编排者不得自任的正文与门禁未动。
  - `gate-freezes-the-goal`：acpx 安装门禁与暂停规则未动。
- 结论：既有成功路径不受新增规则的阻断。

## Pattern

- 原问题场景：使用者明确指定唯一 Endpoint，但在本次 llmwiki 任务的前 5 次委派中，执行方仍可能读取 7 份 Endpoint 画像、3 份 references 和相关 Trace，合计约 2.5 万字符的结构化文档，再写 7 千余字节 decision.md。
- 候选指令：明确指定唯一 Endpoint 且任务线性时，只读 `routing.md`、该 Endpoint 画像和相关 Trace；references 按步骤加载，不预读全部。
- 对原问题的覆盖检查：该场景下不会再枚举无关 Endpoint；`endpoint-schema.md` 只有写画像时读取，`trace-format.md` 只有写 Trace 时读取，`delegation-contract.md` 只在执行委派前读取。
- 保留检查：该路径仍要求委派前写 `decision.md`、仍保留 acpx/权限/回收/留痕门禁；缺失或不可用时回到完整路由。

## Contract

- 无自动 runner；`evals/cases.yaml` 仍是指令级判据，因此没有编造分数。
- `SKILL.md` frontmatter `name` 保持不变。
- 生产稿 148 行 / 10,957 字符，候选稿 156 行 / 11,574 字符；新增 4 行，约 +617 字符。
- `diff` 无空白错误；候选没有新增主机名、绝对家目录、内部 URL 或凭据。
- 结论：合同检查通过。

## Side Effects

- 快速路径只在“明确指定唯一 Endpoint + 线性任务”时生效，没有扩大触发范围。
- 没有删除任何安全门禁，也没有放宽读写权限、Trace 门槛或固化确认要求。
- 完整路由仍是默认路径；只有需要自行选人时才要求走它。
- 结论：副作用范围低，符合 Proposal 的 `risk: medium`。

## Conclusion

`pass`。候选稿可进入 promote 决策，但按 `skill-evolver` 门禁，必须等使用者确认候选 diff 后才覆盖生产稿。
