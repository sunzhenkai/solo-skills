# 委派适配契约

本 skill 不绑定具体执行器。所有委派都表达成下面这组输入输出，默认由 `acpx` 实现；换执行器只改本文件，不改 `SKILL.md`。

## 契约

**输入**

| 字段 | 说明 |
| --- | --- |
| `endpoint` | Host + Agent Kind，如 `local/codex`。第一版只支持本机 |
| `model` | 本次使用的模型 id。调用方给出则原样传给执行器；未给出则省略，用 Endpoint 默认 |
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

准备委派时若 `acpx` 不在 PATH：停下这件事，默认提议安装（以 https://acpx.sh 的当前方式为准，常见为 `npm i -g acpx`），并等使用者回答。未获确认不得安装；未获**明确拒绝**不得降级——沉默、追问、话题转移都不算拒绝。等待期间也不得改由编排者自己动手，那不叫降级，是跳过委派。拒绝后先提示「功能受限」再走降级，不要把降级说成完整替代。

```bash
run_dir=~/.cache/agent-roster/runs/"$run_id"   # 路由阶段已建好，decision.md 就在里面

acpx --cwd "<工作目录>" --format json --approve-reads <kind> exec "<prompt>" \
  > "$run_dir/run.ndjson" 2> "$run_dir/stderr.log"
```

`--cwd`、`--format`、`--approve-reads`、`--approve-all`、`--model` 等都是 **acpx 根级全局旗标**，必须写在 `<kind>` 之前；写在子命令之后会报 unknown option 或打印帮助退出。

调用方给出了 `model` 时，在 acpx 与 `<kind>` 之间加 `--model "<id>"`；未给出则不要加这个旗标。id 形态因适配器而异，广告列表与 CLI `--help` 都不可靠：

- 已知口径：`cursor-agent acp` 用广告列表里的参数化完整 id（如 `grok-4.7[context=256k,reasoning_effort=high,fast=true]`）；`codex-acp` 用裸模型名（如 `glm-5.3-flash`），传参数化形态会被拒；`claude-agent-acp` 用裸模型名且**不广告任何模型列表**（session/new 无 models 字段，无法按广告验证），只认 `ANTHROPIC_API_KEY` 环境变量（不读 `ANTHROPIC_AUTH_TOKEN`，也不读 CLI settings 里的等价变量），不传 `--model` 会落到适配器默认模型——自建网关无该渠道即报 503。
- **冒烟门禁**：该 Endpoint+模型组合没有 L3 成功记录（画像「探测状态」或本仓库 trace）时，正式委派前必须先发一句 smoke prompt（如 `reply with just: ok`）验证认证、登录态与模型解析，确认响应正常后再发正式任务。L1/L2 探测通过**不构成**跳过冒烟的理由——认证口径、模型解析、会话建立只有 L3 能暴露。冒烟失败按「受派方没起来」处置。

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

## 受控执行（正式委派必须满足）

1. **timeout 必填**：契约字段 `timeout` 不是文档摆设。长任务用外层 `timeout <seconds>` 或执行器等价旗标兜底；未设 timeout 的失败只能靠人肉发现。
2. **PID 监控**：后台委派在启动时记录 PID（`echo $! > run-dir/pid`），之后只用 `ps -p "$(cat run-dir/pid)"` 判断存活。
3. **禁用 `pgrep -f` 关键字匹配做存活判断**：轮询命令自身的命令行就含该关键字，`pgrep -f` 每次都命中自己，会无限误报「仍在运行」（实测造成小时级假等待）。同理适用于任何 `ps aux | grep <关键字>` 判断。
4. **完成判定看产物，不看中间输出**：有事件流时先确认最终文本长度与 stopReason，再宣布成功；半截输出（只有计划宣告、无最终产物）按失败处置。

## 不用 acpx 时的降级

**进入条件**：本次委派的使用者已**明确拒绝**安装 `acpx`，且下面的受限清单已经说清。两条缺一就不要往下照抄命令——回到 `SKILL.md` 的门禁，先把委派停住。上一次委派走过降级，不是本次的进入条件。

降级不是对等路径。编排者直接对适配器命令说 ACP（stdio 上的 JSON-RPC 2.0）：`initialize` → `session/new` → `session/prompt`，自行处理权限请求与取消。`scripts/probe_endpoints.py` 的 L2 探测只做到 `initialize` 就断开，不是完整委派客户端。

**仍可走通**：一次性发出 prompt、取回文本、写成 Handoff。

**功能受限**（拒绝安装后必须向使用者说清这些再继续）：

- 会话持久化、排队、崩溃重连没有实现
- 只读 / 可写两档权限没有现成旗标，要自己接 `session/request_permission`
- 结构化事件流、超时终止要自己落到 Run 目录
- 失败时难以区分是受派方问题还是编排者没把协议走完

这正是第一版把 `acpx` 安装作为默认选项的原因。
