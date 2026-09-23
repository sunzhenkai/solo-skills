# eval — 20260923-acpx-model-id

- 回归：`evals/cases.yaml` 的 `model-is-contract-field` 要求「acpx 命令带 --model、decision.md 记录 model、未给出时不加空旗标」——候选稿保留全部三点（仅改旗标位置），不破坏该用例。其余用例（decision-before-execution / read-only-by-default 等）不涉及被改小节，无影响。本会话完整成功路径（routing → decision → smoke → 委派 → trace）在新规则下逐步可走通，无步骤被打断。
- 模式：原失败两类——①`--model`/`--cwd` 写在子命令后被拒（cursor 与 codex 各一次）；②`--model` id 口径猜错被拒（cursor 用 CLI id、codex 用参数化 id 各一次）。候选稿第 1 条规则直接消除①；第 2 条已知口径 + smoke 验证消除②，且 smoke 在本会话实测有效（模型 id 经 initialize 响应确认后才发正式任务）。
- 契约：仓库自带 evals 为确定性/LLM 判例清单（无自动 runner），按指令级对照执行，未编造分数。
- 副作用：不触碰触发条件、权限档位、安装门禁与降级规则；候选文本只含公开 CLI 形态示例，无主机名/项目/密钥。
- 结论：pass
