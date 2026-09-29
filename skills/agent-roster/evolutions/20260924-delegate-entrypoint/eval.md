# eval — 20260924-delegate-entrypoint

- 回归：evals/cases.yaml 全部 10 条原 case 逐条对照——四条不变量（decision-before-execution / no-data-in-repo / read-only-by-default / acpx 门禁）原文未动；契约仅新增第 0 条与口径扩写，未触碰冒烟门禁、降级进入条件、权限档位语义。无影响。
- 模式：新 case prompt-result-by-event-id 用真实 run 验证——20260924-150044-smoke-codex（含 set_config_option，prompt RESULT 在 id=3）修复前判 truncated、修复后判 done；同批 claude run 同样翻转。五适配器 20 次 run 全量过 run_status.py 无 unknown（除真实的失败 run 按其指纹判 stuck/truncated）。
- 契约：delegate.py 纯 stdlib、零第三方依赖；不解析自然语言；判定逻辑复用 run_status.classify；命令形态（全局旗标在子命令前、--model 在 acpx 与 kind 之间）与契约一致，dry-run 输出可对照。无自动 runner，按指令级对照 + 真实样本实测，未编造分数。
- 副作用：入口脚本把「先 decision.md 后启动」从流程约定变成代码保证（写盘在 Popen 之前）；不扩权限、不触碰密钥；提案与变更文件副本同目录，可审计。
- 结论：pass
