# decision — 20260924-delegate-entrypoint

promote

理由：
- 提案由本次全面测试（MiniMax-M3 × 五适配器 × 20 run）直接驱动：每个 proposed_change 项
  都有对应实测失败/踩坑证据（见 eval.md 与 agent-data trace 20260924-minimax-m3-five-agent-delegation-test）。
- run_status.py 的 id 硬编码是确定性 bug（成功被误判 truncated），修复后历史 run 重判正确。
- 候选 diff 与 proposal 一致：新增 delegate.py、修 run_status.py、契约 +1 条与口径重写、
  SKILL.md 一句指针、evals +1 case，无夹带。

后续：commit 由编排者执行；push 属线上动作，需用户单独确认。
