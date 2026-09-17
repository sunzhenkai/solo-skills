# 委派适配契约

本 skill 不绑定具体执行器。所有委派都表达成下面这组输入输出，默认由 `acpx` 实现；换执行器只改本文件，不改 `SKILL.md`。

## 契约

**输入**

| 字段 | 说明 |
| --- | --- |
| `endpoint` | Host + Agent Kind，如 `local/codex`。第一版只支持本机 |
| `prompt` | 交给受派方的完整任务描述 |
| `cwd` | 工作目录 |
| `permission` | `read-only`（默认）或 `write` |
| `handoff` | 期望产出落到哪个路径。只读委派下由发起方落盘 |
| `timeout` | 超时上限，超过即判 timeout 并终止 |

**输出**

| 字段 | 说明 |
| --- | --- |
| `status` | `completed` / `failed` / `timeout` |
| `summary` | 结果摘要文本 |
| `handoff_paths` | 实际写出的交接物路径 |
| `run_dir` | `~/.cache/agent-roster/runs/<run-id>/` |

## 默认实现：acpx

`acpx` 是 ACP（Agent Client Protocol）的无头命令行客户端，一条命令打通各家 coding agent，自带会话管理、权限策略与结构化事件流。

```bash
run_dir=~/.cache/agent-roster/runs/$(date +%Y%m%d-%H%M%S)-<slug>
mkdir -p "$run_dir"

acpx --format json <kind> exec "<prompt>" \
  --cwd "<工作目录>" \
  --approve-reads \
  > "$run_dir/run.ndjson" 2> "$run_dir/stderr.log"
```

- `--format json` 输出 NDJSON 事件流，`session/update` 事件里带工具调用、思考与 diff，不需要从终端色码里刮内容。
- 权限档位映射：只读用 `--approve-reads`（acpx 默认），可写用 `--approve-all`。
- `exec` 是一次性调用，不保存上下文；需要多轮时才用会话（`acpx <kind> sessions new` + `-s <名字>`）。

acpx 仍处于 alpha，命令表面会变。执行前若不确定，以 `acpx --help` 与 `acpx <kind> --help` 为准，不要照抄本文件里的参数。

## 已知的 Agent Kind 与适配器

| Kind | ACP 命令 |
| --- | --- |
| `claude` | `npx -y @agentclientprotocol/claude-agent-acp` |
| `codex` | `npx -y @agentclientprotocol/codex-acp` |
| `gemini` | `gemini --acp` |
| `cursor` | `cursor-agent acp` |
| `opencode` | `npx -y opencode-ai acp` |
| `qwen` | `qwen --acp` |
| `kiro` | `kiro-cli-chat acp` |
| `copilot` | `copilot --acp --stdio` |
| `pi` | `npx pi-acp` |

## 不用 acpx 时的降级

直接对适配器命令说 ACP（stdio 上的 JSON-RPC 2.0）：`initialize` → `session/new` → `session/prompt`，自行处理权限请求与取消。`scripts/probe_endpoints.py` 的 L2 探测就是这么做的，可以作为最小参考。

代价是会话持久化、队列、崩溃重连都要自己实现——这正是第一版选择站在 acpx 之上的原因。
