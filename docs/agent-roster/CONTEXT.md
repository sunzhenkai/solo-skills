# Agent Roster

一个 agent 在决定「这件事该交给哪个 agent 做」时所处的问题域：登记有哪些 agent 可用、它们各自擅长什么，据此选人、派活、取回产出，并把值得记住的经验留下来。

## Language

**Host**（主机）:
一台可以运行 coding agent 的机器，以 ssh 别名作为身份。
_Avoid_: 机器, node, device（device 在既有台账里特指设备档案文件）

**Agent Kind**（agent 种类）:
一类 coding agent 的身份，如 codex、claude、cursor。
_Avoid_: provider, vendor, backend, agent（单说 agent 指代不明）

**Endpoint**（端点）:
某台 Host 上某个 Agent Kind 的一份可用实例，是名册的登记主键。
_Avoid_: runtime, instance, worker, agent 实例

**Roster**（名册）:
全部 Endpoint 及其画像的登记簿。
_Avoid_: 注册表, inventory, 清单

**Disposition**（任务倾向）:
对某个 Endpoint 擅长什么、在什么情况下会翻车的自然语言描述。
_Avoid_: 能力, capability, 评分, 权重

**Probe**（探测）:
对一个 Endpoint 客观可用性的一次机器验证，只回答装没装、起不起得来、登没登上。
_Avoid_: 健康检查, ping, 心跳

## 委派

**Orchestrator**（编排者）:
加载本能力、决定把事情交给谁并发起委派的那个 agent。
_Avoid_: 主 agent, caller, client（ACP 中 client 另有所指，方向相反）

**Delegation**（委派）:
编排者把一件事交给一个 Endpoint 执行、并取回结果的一次完整往返。
_Avoid_: task, job, 调用, 请求

**Handoff**（交接物）:
一次 Delegation 产出的、供后续 Delegation 或人类消费的工作成果。
_Avoid_: 输出, artifact, 产物

**Run**（运行痕迹）:
一次 Delegation 过程中产生的原始过程数据，派生、可丢弃、不供直接阅读。
_Avoid_: trace（另有所指）, 日志, 记录

## 学习

**Trace**（案例）:
一次 Delegation 留下的、写给未来选人决策看的记录，核心是当时为什么选它。
_Avoid_: 日志, log, 历史, Run

**Routing Rule**（路由规则）:
从累积的 Trace 中固化出来、可直接指导选人的成文规律。
_Avoid_: 策略, 算法, 打分, 权重

**Pattern**（通用规律）:
已经脱离具体 Host 与任务、对任何人都成立的经验结论。
_Avoid_: 最佳实践, 经验, 教训（后者指单条 Trace 里的结论）
