# Eval — 20260924-adapter-argv-drift

对照**现有行为**验候选稿，四项独立跑过。沙箱：把候选按真名复制进临时目录
（前缀命名会让 `from _roster import` / `from run_status import` 导不到，这是候选目录的
固有形态，不是缺陷）。

## 回归（按现行契约的成功路径走一遍，确认没被新规则打断）

- 探测 10 个 kind 全跑：七个既有 kind 的 L1 判定与改动前一致
  （claude/codex/cursor/opencode/qwen/kiro/pi ✅，gemini/copilot 未安装），新增 `qoder` 探到 1.1.62。
  输出结构是**纯增量**（`cli_name` / `adapter_bin` / `acpx_argv` / `argv_gap`），旧字段未动，
  `--render` 与 `--write` 两条出口都跑通。
- `delegate.py` 的 kind 路径 dry-run 与生产逐字节相同：
  `acpx --cwd /tmp --format json --approve-reads --model M1 codex exec hello`。
  新规则只在 `--agent` 出现时改变命令形状，不传 `--agent` 时代码走 else 分支＝原逻辑。
- 契约新增内容全部落在「已知的 Agent Kind 与适配器」节内，未改动 `exec`／权限映射／
  冒烟门禁任何一条既有规则；SKILL.md 正文不改（委派节本就整体指向该 reference）。

## 模式（原先失败的那类问题，按新指令能否避免）

- **真漂移被确定性抓到**：候选探测对 `qoder` 输出
  `⚠ acpx 内置 argv 指向 qodercli，本机不在 PATH；CLI 实际是 qodercn → 走 acpx config agents.qoder.argv 覆盖，或 delegate.py --agent`。
  这正是当日「L1 ✅ + L2 ✅ 但委派以 command-not-found 失败」的那个组合——现在在探测阶段就暴露，
  不必等到读 dist 文件。
- **不误报真没装的**：gemini / copilot（本机确实未安装）不出 `argv_gap`。
  条件收紧为「CLI 解析到了名字，而 acpx 要 spawn 的名字不在 PATH」；npx / pnpm / uvx 这类包运行器
  不参与二进制名比对（它们 argv[0] 恒在，真适配器名在后面的元素里，且带 `${...}` 模板，比对无意义）。
- **端到端**：候选 `delegate.py --agent "qodercn --acp" --smoke --wait` 在真实环境跑通，
  状态判定 `done`（`stop_reason: end_turn`，final_text=`ok`），
  `collect_handoff.py` 正常回收（并给出 2 字符 suspicious 警告——冒烟本就该短），
  `retry_check.py` 对该 run 判 `retry-blocked`（因 done），四项检查无报错。
- **config 覆盖这条路**：在执行器 config 里登记 `agents.qoder.argv` 后 `acpx qoder exec` 被证实
  能拉起适配器（initialize 正常返回），对内置 kind 同样生效。该验证在临时 HOME 下做，
  因而停在 `session/new: Authentication required`——这条恰好反过来印证了契约里新增的
  「委派不要改 HOME」。真实 HOME 下写入 config 属于使用者环境改动，未擅自落笔。

## 契约（脚本自带测试的跑测试；没有则指令级对照）

- **候选稿自身缺陷一处，已在此步抓到并修**：「不要改 `HOME`」那段被两次编辑各插一遍，
  成了重复段。用「全文排序找重复行」复核（排除表格分隔符这类合法重复）后确认为 10 增 / 0 删。
  教训：分两次 Edit 往相邻位置插同一段文字，必须做一次全文重复行检查。
- `python3 -m py_compile` 两个候选脚本通过。
- `evals/cases.yaml` 候选稿 YAML 可解析，16 条（原 14 + 新 2）。
- 校验逻辑：`--agent` 时不再要求 `--kind`；两者都不给仍报 `缺必填参数: --kind`（旧行为保留）。
- 正则实测修正一处：acpx dist 里对象键**不带引号**（`argv: [...]`），候选稿按
  `["\']?argv["\']?` 匹配并保留 `command:` 字符串形态回退——首版按 `"argv"` 写，实测 `acpx_argv: null`，
  即「读不到」而非「读错」，属安全失败但等于没实现，故改掉后重测。

## 副作用

- 权限面：未新增任何自动批准；`--agent` 与 `--kind` 共用同一套 `--approve-reads`/`--approve-all` 映射。
- 破坏性操作：探测脚本只多读 `npm root -g` 与 dist 文本，不写；`--write` 回填逻辑未改。
- 命令形状：`status.json` 的 `kind` 在 `--agent` 形态下改记适配器二进制名（`qodercn`），
  使 `retry_check.py` 的残留进程 marker 仍然有效——记整串旗标会永远匹配不上，制造「无残留」假干净。
  同时新增 `agent` 字段保留原始旗标。
- `cmd.sh` 落盘从 `" ".join` 换成 `shlex.join`：这是 Proposal 之外的一处附带修正，
  由本次改动直接引入（`--agent "qodercn --acp"` 在裸 join 下写出的 cmd.sh 复制回去会被重切成
  另一个命令）。kind 路径的输出不变。
- 已知残留（本轮不做）：`smoke_gate.py` 给的冒烟命令模板固定 `--kind <kind>`，
  对需要 `--agent` 的 kind 会打印一条跑不通的命令。契约已说明处置，但建议命令本身仍会误导——
  留作下一次小修，与本模式不同因。

## 结论

**pass**。回归无破坏，目标失败模式在探测与委派两处都被确定性拦下，端到端实跑一次通过。
唯一超范围的一条是 `cmd.sh` 的 shlex 修正，已在上文与 proposal.yaml 中显式登记。
