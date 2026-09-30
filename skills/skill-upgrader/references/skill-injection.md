---

## Self-evolution

本 Skill 从真实执行中积累经验，并按 Eval 验证改进。目录（均相对本 Skill 根目录）：

```text
<skill-dir>/
├── SKILL.md
├── examples/      # 经过验证的优秀执行案例
├── evals/         # 可验证成功标准（cases.yaml）
└── experience/    # 真实失败 / 成功 / 规律
```

自进化不改变上文已规定的目标、流程、工具用法、输出与约束。

- 执行复杂任务前先查 `examples/`，有相关成功案例就复用；没有就按正文执行，不编造案例。
- 任务完成前对照 `evals/cases.yaml` 验证关键输出；Eval 失败先修输出，不带着失败交卷。
- 完成后遇失败、用户纠正、明显成功或新的有效方法才写入 `experience/`：单次失败进 `failures/`，重复规律进 `patterns/`（至少两次同类证据）。不记 trivial 信息，不伪造条目，不写密钥 / 内部 URL / 凭据。
- 改生产正文：先出提案并经用户确认，再走 `skill-evolver`（`evolutions/`）或 `skill-upgrader` 的 `update` 模式（`patches/`）；禁止由单次失败直接改 `SKILL.md`。
