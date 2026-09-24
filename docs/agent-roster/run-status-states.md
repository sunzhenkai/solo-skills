# `run_status.py` 状态判定说明

对象：`skills/agent-roster/scripts/run_status.py`（只读分析，未修改任何文件）。
输入是 `~/.cache/agent-roster/runs/<run-id>/` 下的三样东西：`run.ndjson`（事件流）、`status.json`（启动时记录的 endpoint/model/pid/started_at/timeout_seconds）、`pid`（进程号）。

## 0. 先看一件事：判定的实际优先级

`classify()` 是一条 if/elif 链（`run_status.py:125-142`），**顺序就是优先级**，与 docstring 从上到下列举的顺序不同：

| 序 | 状态 | 触发条件（行号） |
| --- | --- | --- |
| 1 | `not-started` | 无任何可解析事件（125） |
| 2 | `done` | `stopReason == "end_turn"` 且最终文本 > 0 字节（127） |
| 3 | `timed-out` | `now > started_at + timeout_seconds`（129） |
| 4 | `cancelled` | 事件流里出现取消（131） |
| 5 | `stuck`（形态版） | 有 id=0 的响应 且 事件数 ≤ 3 且 id=1 无响应（133） |
| 6 | `running` | pid 存活（135） |
| 7 | `truncated` | prompt 已发 且 没有终态响应（137） |
| 8 | `stuck`（兜底版） | id=1 始终没有响应（139） |
| 9 | `truncated` / `unknown` | prompt 发过但响应不是 end_turn/空文本 → truncated；否则 unknown（142） |

两个由此产生的、必须在读单个状态时记住的推论：

- **事件流形态压过进程存活**：第 5 条在第 6 条之前，所以一个 pid 还活着、但从未回答 `session/new` 的 run 判 `stuck` 而不是 `running`（这正是「受派方没起来」的意图）。
- **终态证据压过一切算术**：`done` 在 `timed-out`、`cancelled` 之前，所以一个跑完但事后才被发现「已超过 timeout」的 run 仍然判 `done`。

另外 `main()` 只解析路径（`run_status.py:176-180`）：给目录就用目录，否则拼到 `RUNS_ROOT` 下；两者都不存在时打印 `error: run 目录不存在` 并以 **2** 退出——不是状态，是「没这东西」。

---

## 1. `done`

**判定依据**（`run_status.py:127`）：三个条件同时成立。
1. 先从事件流里**动态发现** prompt 的请求 id：遍历所有事件，取最后一个 `method == "session/prompt"` 的 `id`（99-103）。
2. `result_for(events, prompt_id)` 取该 id 的**最后一个**带 `result`/`error` 的事件（45-50），得到 `final`；`final.result.stopReason == "end_turn"`。
3. `final_text_length(events) > 0`（53-61）：把所有 `params.update.sessionUpdate == "agent_message_chunk"` 且 `content.type == "text"` 的 `text` 长度累加。

**NDJSON 形态（最小例）**——这里 prompt 恰好在 id=2（未传 `--model` 时）：

```json
{"jsonrpc":"2.0","id":0,"result":{"protocolVersion":1}}
{"jsonrpc":"2.0","id":1,"result":{"sessionId":"s1"}}
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"s1","prompt":[{"type":"text","text":"reply with just: ok"}]}}
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s1","update":{"sessionUpdate":"agent_message_chunk","content":{"type":"text","text":"ok"}}}}
{"jsonrpc":"2.0","id":2,"result":{"stopReason":"end_turn"}}
```

传 `--model` 时 `set_config_option` 会占掉一个 id，prompt 的请求与响应整体后移到 id=3；因为脚本按事件自己的 id 匹配，判定结果不变。

**与相邻状态的区别**

- vs `running`：`running` 的证据只有一条——pid 存活，它不含任何「成了」的信息；`done` 的证据只有一条——终态响应 + 非空文本，它与 pid 是否存活无关（回收中的进程照样 `done`）。**不要用 pid 反推 done**：pid 没了可能是 done，也可能是 stuck。
- vs `truncated`（最危险的一对）：区别**只在最后一行**。有 `agent_message_chunk` 但没有 id=prompt_id 的 `RESULT`，或 `stopReason` 不是 `end_turn`，或 `stopReason == "end_turn"` 但文本长度为 0 —— 三种都是 `truncated`，不是 `done`。commit `c1ab61b` 之前把「看到文本块」当成功，正是这条误判。
- vs `timed-out`：`done` 排在前面（127 早于 129），所以**只要真的收完了，timeout 过期不会翻转成失败**。
- 兜底路径（104-110）：若 prompt 的 id 上找不到响应，任何 `result` 里带 `stopReason` 的事件都会被当作 `final`。好处是 id 布局变化时不至于误判成 truncated；代价是别的请求的 `stopReason` 也可能被吃进来——所以看 `--json` 输出里的 `stop_reason` 与 `final_text_length` 两者是否都合理，才宣布回收。

---

## 2. `stuck`

**判定依据**：两条路径，都围绕「`session/new` 没有响应」。
- 形态版（133）：`result_for(events, 0)` 非空（initialize 的 RESULT 落在 id=0）**且** `len(events) <= 3` **且** `result_for(events, 1)` 为空（id=1 的 session/new 无响应）。
- 兜底版（139）：走到这里说明没有终态、未超时、未取消、pid 已死、prompt 也没有「发了但没结果」的形态，只要 `session_result is None` 一律 `stuck`。

**NDJSON 形态（最小例）**——三事件，docstring 说的就是这一条：

```json
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1}}
{"jsonrpc":"2.0","id":0,"result":{"protocolVersion":1}}
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/tmp"}}
```

第三行是**请求**（有 `method`、无 `result`/`error`），`result_for` 不会把它当响应。

**与相邻状态的区别**

- vs `not-started`：`not-started` 是**一条可解析事件都没有**——命令大概率压根没跑起来（去看 `stderr.log` 和退出码）；`stuck` 是握手有回声但会话建不起来，属于「那台机器上的 agent 起来了但不响应」。处置方向也不同：`stuck` 明确**禁止**原地重试同一 Endpoint（149 行 action），要先探测再换候选。
- vs `truncated`：**分水岭是 `session_result` 与 `prompt_sent`**。`stuck` = 会话没建起来，任务连发都没发出去；`truncated` = 会话建好了、prompt 发了、活干了一半断了。前者是「受派方没起来」，后者是「产出是半成品」。把 stuck 当 truncated 去重发同一 Endpoint，等于对着一个根本没起来的进程再烧一次 timeout。
- vs `running`：如前述，形态版 `stuck` 优先级高于 `running`，pid 活着也能判 stuck。`delegate.py --wait`（`delegate.py:160-167`）要求 `state ∈ {done,stuck,truncated,cancelled}` **且** `not pid_alive` 才收手，所以一个 stuck 且进程还在的 run 会一路等到 deadline 才被 killpg——这是刻意用 timeout 兜底，不是漏判。

---

## 3. `cancelled`

**判定依据**（`run_status.py:113-117`）：事件流里出现过任一取消痕迹——
- `method == "session/cancel"`（通知，无 id），或
- `params.update.sessionUpdate == "session_cancelled"`。

不依赖 pid，也不依赖 `status.json`。

**NDJSON 形态（最小例）**：

```json
{"jsonrpc":"2.0","id":1,"result":{"sessionId":"s1"}}
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"s1","prompt":[{"type":"text","text":"…"}]}}
{"jsonrpc":"2.0","method":"session/cancel","params":{"sessionId":"s1"}}
```

**与相邻状态的区别**

- vs `timed-out`（易混）：`timed-out` 是**纯算术**（119-123），只看 `status.json` 的 `started_at + timeout_seconds` 与 `now`，完全不看事件流；`cancelled` 是**流里有主动取消的记录**。`timed-out` 排在前面（129 早于 131），所以「timeout 到期 + 流里带 session/cancel」判 `timed-out`。实际路径也分开：`delegate.py` 的超时收尸走 `kill_run` / killpg（`delegate.py:43-62`、`169-176`），是**信号**，不产生 ACP 取消事件；`session/cancel` 通常来自 acpx 自身或人工发起的取消。
- vs `truncated`：两者都是「没有终态就断了」。区别是有没有**意图证据**——`cancelled` 说明有人/有代码明确要求停，截断点可定位，可以据此决定重发还是换人（148 行 action）；`truncated` 什么都没留下，只能按「缩小范围重发一次」推定处置。
- 一个反直觉的口子：`done` 排在 `cancelled` 前面。若受派方先给出 `end_turn` 再被取消，仍判 `done`——这时该核对 `final_text_length` 与任务是否相称，而不是只看状态字。

---

## 4. `truncated`

**判定依据**：三个落点，共同语义是「发过 prompt，但没拿到可用的终态」。
- 主路径（137）：`prompt_sent`（事件流里有 `session/prompt` 请求，99-103）**且** `final is None`（既没在该 id 上找到 `result`/`error`，也没有任何带 `stopReason` 的兜底响应）；且 pid 不存活。
- 末路兜底（142）：`prompt_sent` 为真但 `final` 存在却不合格——即 `stopReason` 不是 `end_turn`（例如 max_tokens、refusal），或 `stopReason == "end_turn"` 而文本长度为 0，**或 prompt 的 id 上收到的是一个 JSON-RPC `error` 响应**（`result_for` 把 error 也认作终态，104 行）。

**NDJSON 形态（最小例）**——有 update 流、无 RESULT，且 `status.json` 里 pid 已退出、timeout 未到期：

```json
{"jsonrpc":"2.0","id":1,"result":{"sessionId":"s1"}}
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"s1","prompt":[{"type":"text","text":"…"}]}}
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s1","update":{"sessionUpdate":"agent_message_chunk","content":{"type":"text","text":"我先分析一下这个仓库的结构…"}}}}
```

**与相邻状态的区别**

- vs `stuck`（最容易被当成同一件事）：看 `final_text_length` 和 `events` 数量就分开了——`stuck` 是**会话建立阶段断掉、零产出**（`final_text_length: 0`，事件停在握手），`truncated` 是**会话建立成功、prompt 已发、有中间文本但没有终态**。处置额度也不同：`truncated` 允许对同一 Endpoint 重发一次（151 行），`stuck` 一次都不该重发。
- vs `done`：见上，只差终态那一行；`truncated` 的产出**不能收**——`collect_handoff.py` 只对 `done` 放行（`references/delegation-contract.md:27`），这使 truncated 成为一个「必须承认失败」的状态，而不是「差不多成功了」。
- vs `running`：同一条事件流，pid 活着判 `running`（先等），pid 死了才落 `truncated`。所以 `running` 是 truncated 的未定稿：**不要在进程还在时宣布半成品**，脚本自己也这么处理（135 在 137 之前）。
- 隐藏的翻转：docstring 里「有 update 流」这一条件在代码里**没有实现**——代码不要求存在 `session/update`。只发了 prompt 就断、一个字节产出都没有的流，同样判 `truncated`。

---

## 5. `timed-out`

**判定依据**（`run_status.py:119-123`）：`status.json` 里 `started_at` 与 `timeout_seconds` **都是数字**，且 `now > started_at + timeout_seconds`。`now` 可由 `classify(run_dir, now=…)` 注入（64-65），`main()` 走默认 `time.time()`。它不要求进程死亡，也不看事件流内容。

**形态**：NDJSON 没有专属指纹——同一份流，`status.json` 决定它是不是 timed-out。最小对照：

```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"s1","prompt":[{"type":"text","text":"…"}]}}
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s1","update":{"sessionUpdate":"agent_message_chunk","content":{"type":"text","text":"仍在写…"}}}}
```

配上 `status.json`：

```json
{"endpoint":"local/codex","model":"SomeModel","pid":41233,"started_at":1758680000.0,"timeout_seconds":600}
```

timeout 未到期 + pid 在 → `running`；到期 → `timed-out`。事件流**一行都没变**。

**与相邻状态的区别**

- vs `cancelled`：见第 3 节。一个是外部时钟算出来的，一个是流里有记录的。
- vs `truncated`：判据来源不同——`timed-out` 只来自 `status.json` 的算术，`truncated` 只来自事件流缺终态。同一条未完成的流，`now` 过没过线决定报哪个。这层区别有实际意义：timed-out 说明「**我们的预算用完了**」（可拿部分产出缩小范围重发一次），truncated 说明「**对面自己断了**」。
- 静默失效要当心：`status.json` 缺失、JSON 解析失败（71-75 会退化成 `{}`）、或两个字段缺任何一个、或写成字符串（如 `"600"`），`timed_out` 永远是 `False`，超时永远判不出来——只能退化到 `running` 或 `truncated`。这就是 `delegate.py` 把 `--timeout` 设为必填、并在缺参时报错（`delegate.py:89-92`）的原因。

---

## 6. `running`

**判定依据**（`run_status.py:135`）：`pid_alive`。pid 来源有优先级——先读 `pid` 文件（77-82），再被 `status.json` 的 `pid` 覆盖（83），即 `status.json > pid 文件`。存活判定用 `os.kill(pid, 0)`（85-93）：`ProcessLookupError` → 死；`PermissionError` → 活（进程属于别人）。

前置条件更重要：`running` 排在 `not-started / done / timed-out / cancelled / stuck(形态) `之后（125-133），所以它是「**pid 还在，且没有任何比它更强的证据**」。

**NDJSON 形态**：与 `truncated` 的形态**完全一样**（prompt 已发 + update 流），差别只在进程表：

```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"s1","prompt":[{"type":"text","text":"…"}]}}
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s1","update":{"sessionUpdate":"agent_message_chunk","content":{"type":"text","text":"先读一下 run_status.py…"}}}}
```

`pid` 文件里那个进程还活着、`status.json` 的 timeout 还没到期 → `running`。

**与相邻状态的区别**

- vs `truncated`：**同一份流，进程死活是唯一分水岭**。这也是脚本不能只读 NDJSON 的原因。
- vs `done`：`running` 不预测结局。它对应的 action 是「等下一轮复查」（150 行），既不是成功也不是失败。
- vs `stuck`：形态版 stuck（133）会**抢在** running 前面——挂在 `session/new` 上的活进程判 stuck，不给你继续等的借口。
- 「体积不涨怎么办」不在脚本里：`classify()` 每次只报当前 `ndjson_bytes`（96、161），不存历史、不比较。docstring 第 13 行「体积多次复查不涨按 stuck/truncated 处置」是把**跨次调用的动作**写在了单次判定的说明里；实现上由调用方（或 `retry_check.py` 的「ndjson 停涨」一项）负责，脚本本身不产出这个结论。

---

## 7. `not-started`

**判定依据**（`run_status.py:125`）：`not events`。`events` 来自 `load_events()`（30-42）：文件不存在 → 空列表；文件存在但按行解析、**跳过空行与 `JSONDecodeError` 行**（读文本还带 `errors="replace"`）。

**NDJSON 形态**：没有形态——`run.ndjson` 不存在，或存在但没有任何一行是合法 JSON。`--json` 输出里的指纹是 `events: 0`，而 `ndjson_bytes` 可能是 0 也可能大于 0。

```json
error: unknown option --model
```

（整文件只有这一行非 JSON 文本 → 事件数 0。这是从代码推出的可能性，不是实测记录：`references/delegation-contract.md:42` 说全局旗标写错位置会「报 unknown option 或打印帮助退出」，这类文本落到 stdout 就是上图这个形状。）

**与相邻状态的区别**

- vs `stuck`：`not-started` 是**协议层没开始说话**（连 `initialize` 都没落盘），根因大概率在发起方——命令行拼错、`acpx` 不在 PATH、认证变量没注入；`stuck` 是**协议开始了但没走完握手**，根因在受派方。两者 action 不同：not-started 让你去查 stderr 与退出码（145 行），stuck 让你去探测并换候选（149 行）。
- vs `running`：pid 活着但零事件 → 仍判 `not-started`（125 排在 135 之前）。一个「启动了进程却一个字都不往 stdout 写」的 run 在这个脚本眼里不是 running——这通常是对的，因为 `--format json` 的 acpx 一开始说话就该有事件。
- 顺带：`ndjson_bytes > 0` 而 `events == 0` 这个组合，是「CLI 打印帮助/报错就退出」的签名；`--json` 输出把 `ndjson_bytes` 和 `events` 同时给出，就是为了让人看见这个不一致（`run_status.py:188`）。

---

## 8. docstring 与代码实现不一致的地方

docstring 是 `run_status.py:2-16`。逐条对照：

| docstring | 代码 | 结论 |
| --- | --- | --- |
| 11 行 `truncated`：「无 **RESULT(id=2)**」 | 无 id=2 概念；条件是 `prompt_sent and final is None`，`prompt_id` 从 `session/prompt` 事件动态读（99-104），再兜底扫 `stopReason`（106-110） | **硬编码 id 残留，与实际逻辑矛盾**。这正是第 6-8 行自己警告的问题：prompt 的 id 不固定，传 `--model` 时落在 3。commit `e25bb10` 修的是代码，docstring 的这一行没跟上 |
| 5-8 行 `done`：「必须按 session/prompt 事件的实际 id 匹配，不能硬编码」 | 与代码一致，且代码还多做了一步「任何带 stopReason 的 RESULT」兜底 | 一致（代码更宽） |
| 9 行 `stuck`：「**恰好**停在 initialize/RESULT/session/new **三事件**，无 RESULT(id=1)」 | 133 行确实是这条（≤3 事件 + id=0 有响应 + id=1 无响应），但 139 行还有一条**不看事件数**的兜底 `session_result is None → stuck`（例如只有 1 个 initialize 请求、或 id=0 也没响应的任意长度流） | **不完备**：docstring 只描述了两种 stuck 里的一种 |
| 9/11 行沿用「id=0 是 initialize、id=1 是 session/new」的位置假设 | 97-98 行 `result_for(events, 0)` / `result_for(events, 1)` 是**全脚本仅存的两处硬编码 id** | 与 done 那段「id 不可硬编码」的告诫自相矛盾：修好的是 prompt 路径，握手路径仍靠位置约定。顺带一提，`probe_endpoints.py:66-74` 自己发 raw ACP 时 `initialize` 用的是 **id=1**——两套编号口径并存，谁照抄谁翻车 |
| 12 行 `timed-out`：「status.json 记录的 timeout 已到期且未 done」 | 一致；但隐含前提是 `status.json` 存在且两个字段是数字（122），否则静默 `False` | 一致（缺前提说明） |
| 13 行 `running`：「pid 存活（先等再判；**体积多次复查不涨**按 stuck/truncated 处置）」 | 代码单次判定、不存历史、不比较体积；且 running 排在形态版 stuck 之后 | **半不一致**：括号里是跨次调用规则与优先级，脚本未实现 |
| 14 行 `not-started`：「**无 run.ndjson**」 | `not events`——文件存在但为空、或全是不可解析行，同样 `not-started` | 代码更宽（通常更有用，见第 7 节） |
| 10 行 `cancelled`：「出现 `session/cancel`」 | 还接受 `sessionUpdate == "session_cancelled"` 通知（113-117） | 代码更宽 |
| 未列 `unknown` | 142 行 else 分支可产出 `unknown`，152 行也有它的 action | **docstring 缺一个状态** |
| 未提 | prompt 的 id 上收到 `error` 响应时，`stop_reason` 为 `None`、`final` 非空，最终落到 142 判 `truncated`（第 4 节） | **没有 error 态**，协议层报错被并入半成品 |

其它纯代码层面的坑（docstring 与代码都没提，读实现时值得知道）：

- `final_text_length`（53-61）假设 `update.content` 是**对象**；若某适配器把 `content` 发成数组，`content.get("type")` 会 `AttributeError`，脚本抛栈而不是给状态。同理 `result: null` 会让 111 行的 `.get("result", {})` 变成 `None.get(...)` 而崩。
- `pid` 只在**本机**有意义（85-93）。名册里跨机 Endpoint 的 pid 在本地 `os.kill` 上必然 `ProcessLookupError` → 恒判「不存活」，running/timed-out 的语义随之失真。
- `status.json` 的 `pid` 若写成 `null`，83 行 `status.get("pid", pid)` 会用 `null` **覆盖**掉 `pid` 文件里的正确值。

## 9. 为什么不能用 `pgrep` 或肉眼读事件流替代

**`pgrep -f` 的自匹配**（`references/delegation-contract.md:78` 明令禁止，实测造成小时级假等待）：轮询命令自己的 argv 就含被找的关键字，`pgrep -f <run-id|slug|acpx …>` 每次都命中自己那一行 → 永远「仍在运行」→ 永远不进 truncated/stuck 分支。`ps aux | grep` 同理。脚本走的是另一条路：**只信启动时记下来的 pid**（`status.json` 优先，`pid` 文件次之），用 `os.kill(pid, 0)` 问内核（85-93），不做任何字符串匹配。`delegate.py --kill` 也是同一口径——按记录的 pid `killpg` 整个进程组，`delegate.py:44` 的注释直接写着「只信记录，不用 pgrep -f」。

**`pgrep` 只能回答「有没有进程」，回答不了「这件事成了没」**：
- `done` 的证据在事件流里（`stopReason == "end_turn"` + 非空文本），`ps` 看不见；
- `running` 与 `truncated` 是**同一份 NDJSON 在进程死前/死后两种状态**，`ps` 只能给你前一半；
- `stuck` 与 `running` 是**同一个活进程的两种状态**（133 压过 135），光看存活会把「压根没起来的受派方」误当成「还在努力」，进而做出错误处置（继续等 vs 立刻换人）；
- `timed-out` 压根不需要进程信息，它是 `status.json` 的算术。

**肉眼读 NDJSON 会踩的三个具体雷**：
1. **同一个 id 出现多次**：`session/request_permission` 等服务端→客户端请求复用 id，中途能看到同 id 的 `outcome:selected` 之类响应。`result_for`（45-50）因此**反向扫到最后一个**才认；人眼顺着读容易把第一个同 id 响应当成终态。
2. **id 不固定**：`--model` 会让 `set_config_option` 占掉一个 id，prompt 的响应从 id=2 移到 id=3。硬编码「看 id=2」就会把一个成功 run 读成 truncated——`c1ab61b` → `e25bb10` 这一对 commit 修的就是它，实测把 `20260924-150044-smoke-codex` 等 run 从 truncated 翻成 done。
3. **末行是半截 JSON 是常态**：进程被 kill 或管道切断时最后一行常不完整。`load_events`（34-41）逐行 `strip`、跳空行、`JSONDecodeError` 静默跳过，坏尾不影响前面事件的判定；人眼则会因为「屏幕上明明有 agent_message_chunk 文本」把半成品读成结果。这正是 `references/delegation-contract.md:79`「完成判定看产物，不看中间输出」要脚本化的理由。

**还有工程性的一条：判定只有一份实现。** `delegate.py:29` 直接 `from run_status import classify`，`--wait` 的退出条件（`delegate.py:160-167`）、`retry_check.py` 的「失败已归类」、`collect_handoff.py` 的「只对 `done` 放行」共用同一个 `classify()`。肉眼看流每个读者口径都不同，且无法在轮询循环里自动化；脚本输出既是 `state` 也是 `action`（144-153），把「判成什么」和「接下来做什么」绑成一次调用的结果——这是 `pgrep` 加人眼给不出的确定性。
