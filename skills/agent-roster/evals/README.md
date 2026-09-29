# Evals

`cases.yaml` 里是本能力的成功标准，每条都能独立判 pass / fail。

没有自动 runner：执行时由 agent 对照 `cases.yaml` 逐条核对。`judge: deterministic` 的条目应该能靠看文件和命令记录判定，`judge: llm` 的需要读上下文判断。

改动 `SKILL.md` 后应先过一遍这里，尤其是 `kind: core` 和 `kind: regression` 的条目——它们对应的是几条不变量，回归了就说明改错了方向。

新增条目跟着真实发现走：某次执行暴露了没覆盖到的边界，才补一条。不要为了凑数预先写满。
