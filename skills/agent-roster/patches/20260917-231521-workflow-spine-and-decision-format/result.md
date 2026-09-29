# Result

- target: skills/agent-roster
- mode: update
- patch: 20260917-231521-workflow-spine-and-decision-format
- risk: medium
- status: applied
- applied-at: 2026-09-17T23:20:00+08:00

## Validation

- `git apply --check --recount`: pass
- `git apply --recount`: pass
- `git diff --check`: pass
- frontmatter: `name: agent-roster` 未变，与目录名一致
- 引用路径: `references/endpoint-schema.md`、`references/trace-format.md`、`references/delegation-contract.md`、`../../CONTEXT.md`、`../../docs/adr/0003-*.md` 均存在
- 生产文件中已无第二处 `mkdir -p "$run_dir"`（仅历史 patch 记录中出现，属预期）
- privacy check: pass（无家目录、主机名、项目名、凭据）
- mode check: pass（`update`，未新建 `examples/` `evals/` `experience/`，未注入自进化正文）
- SKILL.md 长度: 156 行

## Notes

本轮修掉的实际 bug：路由要求「在执行之前」把决策写进 `~/.cache/agent-roster/runs/<run-id>/decision.md`，而建目录与 `<run-id>` 构造只存在于 `delegation-contract.md` 的委派命令中。按正文顺序执行会写入不存在的目录。现建目录移至路由第 4 步，契约复用 `$run_id`。

未执行的请求部分（附理由）：使用者原本还要求注入自进化正文（`examples/` / `evals/` 的使用时机）。实测安装副本仅含 `SKILL.md`、`references/`、`scripts/`、`examples/`，`evals/`、`experience/`、`patches/` 不在运行位置，注入「运行时参考 evals / 记录 experience」等于写一条执行不了的指令；`examples/` 虽分发但为空，按禁止伪造历史的约束也不引导去读。故只把目录可见性这一客观事实写进「数据在哪」，并顺带修正不变量里「创作目录甚至不会被复制过去」的失准表述（`examples/` 实际会被复制）。若将来积累了可脱敏的真实案例，再单开一轮补 `examples/` 的读取时机。

未做 sync / commit / push。
