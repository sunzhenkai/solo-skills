# agent-roster

一份给 agent 用的能力：**记住手边有哪些 coding agent、各自擅长什么，然后有依据地把活派出去**。

比如让 claude 定计划、codex 评审、kiro 实施——难点不在于怎么调起它们（ACP 生态已经解决了），而在于**凭什么认为这件事该给它做**，以及这个判断能不能随着用下去而变准。

## 它做什么

- **名册（Roster）**：登记「哪台机器上有哪个 agent」，记录版本、可用状态与任务倾向。
- **路由**：接到任务时读名册、读历史案例，选出该派给谁，并在执行前写下选择理由。
- **委派**：按只读 / 可写两档权限把任务派出去，回收产出，把交接物落到指定位置。
- **案例**：只在有教训时留痕。攒够同类证据后，由人确认把规律固化成路由规则。

## 它不做什么

- 不实现被委派 agent 自身的能力。
- 不给 agent 打分排序，理由见 [ADR 0002](./docs/adr/0002-no-scoring-only-cases.md)。
- 第一版**不跨机执行**：远端 Endpoint 可以登记，但派活只在本机。数据模型按跨机设计，留待后续。
- 不在本仓库存放任何真实数据，理由见 [ADR 0001](./docs/adr/0001-ledger-lives-outside-this-repo.md)。

## 安装

```bash
npx skills add sunzhenkai/agent-roster -s agent-roster -g -y
```

外部 skill 装之前先做安全审计。

## 配置

数据放在使用者自己的私有位置，本仓库不假设它在哪：

```yaml
# ~/.config/agent-roster/config.yaml
data_root: ~/path/to/your/private/data-repo
```

名册与案例会落在 `<data_root>/agents/` 下，格式见
[endpoint-schema.md](./skills/agent-roster/references/endpoint-schema.md) 与
[trace-format.md](./skills/agent-roster/references/trace-format.md)。

## 探测本机有哪些 agent

```bash
python3 skills/agent-roster/scripts/probe_endpoints.py             # 装没装、什么版本
python3 skills/agent-roster/scripts/probe_endpoints.py --level 2   # 再确认 ACP 适配器握得上手
python3 skills/agent-roster/scripts/probe_endpoints.py --render    # 输出可粘贴的台账状态块
```

只依赖 Python 3 标准库。L2 直接对适配器说 ACP（stdio 上的 JSON-RPC），不需要额外装客户端。

## 执行层

默认用 [acpx](https://acpx.sh)——ACP 的无头命令行客户端，会话管理、权限策略、结构化事件流都是现成的。但 skill 只依赖一层适配契约（Endpoint + prompt + 工作目录 + 权限 → 结构化结果），换执行器只改
[delegation-contract.md](./skills/agent-roster/references/delegation-contract.md)。

## 相关文档

- [CONTEXT.md](./CONTEXT.md)：术语表。读代码或文档遇到 Endpoint、Delegation、Trace 这些词先看这里。
- [docs/adr/](./docs/adr/)：关键决策与被否决的方案。
- [SKILL.md](./skills/agent-roster/SKILL.md)：能力正文。

## License

MIT
