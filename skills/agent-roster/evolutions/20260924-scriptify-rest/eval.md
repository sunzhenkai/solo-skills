# eval — 20260924-scriptify-rest

- 回归：evals/cases.yaml 全部 14 条（11 旧 + 3 新）逐条对照。四条 core 不变量原文未动：
  decision-before-execution（delegate.py 写盘仍在 Popen 之前，实测 mtime decision.md < run.ndjson）；
  no-data-in-repo（六个脚本只读 data_root、写 ~/.cache；git status 无数据文件）；
  read-only-by-default 与 acpx 门禁未触碰。既有 4 条 regression（含上轮 prompt-result-by-event-id）
  涉及的判定逻辑未改。
- 模式（全部真实样本实测，非合成）：
  smoke_gate：example-host/codex+MiniMax-M3 → skip（命中画像 L3 行与今日 trace）；deepseek-v4 → required 并给出命令。
  retry_check：done run（smoke-codex）→ 第 4 项 ❌ retry-blocked；失败 run（smoke-opencode）→ 四项全过 retry-allowed。
  collect_handoff：done run 写出 handoff 并回填 status.json handoff_paths；timed-out run 拒绝（exit 1）；
  未闭合 <think> 全文在 think 内时不误删（退回原文）。
  probe --write：真实回填 example-host/codex.md——首轮暴露缺陷（新 L1 行挤掉 L3 冒烟依据记录），
  修正为 L3 永不被挤掉后复测通过。
  promotion_check：真实 traces → 无达门槛（正确）；合成两条同理由 trace → 检出并打印提案草稿（双向验证）。
  delegate --kill：ProcessLookupError 分支（进程已退）与 SIGTERM→SIGKILL 分支（合成进程组）均实测。
- 契约：六脚本纯 stdlib；retry_check 的 /proc 扫描在非 Linux 自动跳过（由其余三项兜底）；
  无自然语言判定进入写路径；提案与写入确认权仍归人。无自动 runner，未编造分数。
- 副作用：脚本数 3→9，SKILL.md 正文净增两句指针；探测回填从「只报告」变为「可写回」，
  但写入段格式被 schema 冻结且只动机器段——风险已约束。
- 结论：pass
