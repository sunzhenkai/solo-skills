# Decision — 20260924-adapter-argv-drift

decision: **promote**（2026-09-24，使用者确认「确认晋升」）

已满足：
- Proposal 已展示并获确认（范围＝文档 1+2 与脚本 3+4，使用者答「3+4 一起改」）
- Evaluate = pass（见 eval.md）
- 候选 diff 与附带修正（cmd.sh 改用 shlex.join）一并获确认

晋升动作（已执行）：
1. `references/delegation-contract.md` ← 候选稿 ✅
2. `scripts/probe_endpoints.py` ← 候选稿 ✅
3. `scripts/delegate.py` ← 候选稿 ✅
4. `evals/cases.yaml` ← 候选稿（+2 条 regression）✅
5. SKILL.md 正文**未改**（本模式落在 reference）
6. `~/.agents/skills/` 镜像需重新同步才在运行时生效——由使用者执行，未擅自 sync/commit

未一并处置（使用者未表态，留待后续）：
- ~~往真实 `~/.acpx/config.json` 写 `agents.qoder.argv`~~ → **已落**（使用者随后批准）：
  覆盖生效，`acpx qoder exec` 冒烟 `done`；`~/.acpx/config.json` 只含该一条覆盖，无其它键
- `smoke_gate.py` 的冒烟命令模板仍固定 `--kind`，对需 `--agent` 的 kind 会给出跑不通的建议
- 生产稿 `delegate.py` docstring/help 里既有示例含真实主机名，与 AGENTS.md「本仓库不放主机名」冲突
  （非本轮引入，候选稿原样复制）

## 晋升后补丁（同日，落 config 时暴露）

主路径落地后复跑探测，发现本轮新增的 `argv_gap` **对已覆盖的 kind 持续误报**：
它只读 acpx 内置 dist registry（仍是旧名），读不到 config 覆盖，于是对已经修好的事报警、
还建议「去 config 覆盖」。修法：新增 `acpx_effective_argv()`，以 `acpx config show` 的
`agents.<kind>.argv` 为生效值、dist registry 退回兜底。双向复验：
有覆盖 → 不报；`HOME` 指向空配置（无覆盖）→ 重新报出旧名。

教训形态：**契约里写下的「主路径」必须是探测代码读取的那一份状态**，否则工具会追着已经采纳的建议不放。
本轮提案时只想到「读 registry 才知道漂移」，没想到「读了 registry 就不知道已修」。
