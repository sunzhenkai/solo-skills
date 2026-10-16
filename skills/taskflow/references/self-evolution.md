# 自进化（不在运行路径上）

执行任务时不必读本文件。维护 skill 时用：

- `examples/`：经过验证的执行案例；`evals/cases.yaml`：声明式验收案例；`experience/`：真实失败（`failures/`）/ 成功 / 规律（`patterns/`，至少两次同类证据）。
- 遇到失败、用户纠正、明显成功或新的有效方法才记 experience；不记琐事、不伪造、不写密钥 / 内部 URL / 凭据。
- 改生产正文先出提案经用户确认，再走 `skill-upgrader`（`update` → `patches/`，`evolve` → `evolutions/`）；不因单次失败直接改 `SKILL.md`。
