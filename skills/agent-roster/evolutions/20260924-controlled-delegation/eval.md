# eval — 20260924-controlled-delegation

- 回归：`evals/cases.yaml` 逐条对照——`decision-before-execution`（冒烟门禁不触碰 decision 顺序，本会话实证 decision.md 先于执行落盘仍成立）、`no-data-in-repo`（候选文本只含公开 CLI/适配器行为，无主机名/项目名/内部 URL/密钥）、`read-only-by-default`、`empty-routing-rules`、`model-is-contract-field`（--model 仍是根级旗标、未给出不加旗标，候选未改动该段）均不受影响。成功路径逐步走查：routing → decision → （新增）无 L3 记录则冒烟 → 受控执行（timeout + PID）→ 回收 → trace，各步可走通且新增步骤可跳过条件明确（有 L3 记录时）。
- 模式：本轮三类真实失败逐条映射——①适配器认证口径错误（等价变量名不被读取）：冒烟门禁第 1 次调用即暴露，不用烧一次正式任务；②不传模型落默认模型 503：同上，冒烟响应即可确认模型生效；③漏 timeout + pgrep -f 自匹配 5 小时假等待：受控执行 1–3 条直接禁止。L2 ok 但 L3 连续失败的那类非确定性失败，冒烟不能预防（如实不声称），但受控执行把发现时间从小时级压到 timeout 级。
- 契约：仓库 evals 为判例清单（无自动 runner），按指令级对照执行，未编造分数；新增规则均为可执行判定（有/无 L3 记录、pid 文件存在、ps -p 退出码），非「注意/尽量」式表述。
- 副作用：新增一道前置步骤（冒烟）——触发范围**收窄**失败面而非扩大权限；不删除任何既有安全/门禁规则；降级路径未动。smoke 有少量 token 成本（一句 prompt），换来正式任务失败成本的消除。
- 结论：pass
