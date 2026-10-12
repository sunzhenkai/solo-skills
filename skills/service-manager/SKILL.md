---
id: service-manager
name: service-manager
description: 项目服务管理：从 Makefile、package.json、docker-compose 等探索服务启动方式，统一执行 list / start / stop / restart / status / logs。按项目隔离缓存与日志；安全停止（进程组优先）；缺 name 默认询问。完成后给出改动范围、影响面与服务访问方式总结。在启动、停止、查看项目服务时使用。
---

# 服务管理

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文，不要逐词硬翻。

管理当前项目的服务生命周期。单一 skill，通过 phase（`list` / `start` / `stop` / `restart` / `status` / `logs`）分派行为，不拆 skill 族。

## 项目根

- **项目根**：从当前工作目录向上找，优先含 `.git` 的目录；否则含 `Makefile` / `package.json` / `docker-compose.yml` / `compose.yaml` / `.service-manager.md` 的最近目录；都找不到则以 cwd 为根，并在输出中说明。
- 只管理该项目根之内的服务；`.service-manager.md` 写在项目根；缓存 key 用**项目根绝对路径**的 md5。
- monorepo 子目录调用时：若用户明确指向子包，以该子包为项目根；否则用仓库根并在 list 中区分各服务 `cwd`。

## 两层信息

两层信息（缓存 vs `.service-manager.md`）、信息缓存、`.service-manager.md` 模板与 Profiles & Recipes：**读写服务信息前先读** [references/info-file.md](references/info-file.md)。

## 开发/测试启动约定

热更新入口、监听 `0.0.0.0`、discover、身份匹配（原生进程）与运行状态判定：**start / discover / status 前先读** [references/start-conventions.md](references/start-conventions.md)。

## 阶段

用户消息中的第一个词（或语义）决定 phase；缺省为 `list`。各 phase（list / start / stop / restart / status / logs）的步骤见 [references/commands.md](references/commands.md)，进入 phase 时只读对应小节。

## 完成后总结

任一 phase 结束（成功或可报告失败）后，在主输出之后给总结：

1. **改动范围**：触达服务、动作、是否更新缓存或 `.service-manager.md`。只读无写入 →「无运行态变更」。
2. **影响面**：端口占用/释放、前置依赖、对其它服务影响；无则「无」。
3. **服务访问方式**：对 running/starting 给出入口。本机优先 `http://127.0.0.1:<port>`（或文档中的 path/HTTPS）；若已确认监听 `0.0.0.0`，可补充局域网可用 `http://<主机IP>:<port>`；仅绑本机则如实写；未知 →「待确认」；失败 →「不可用」并指日志。

**只读 phase**（`list` / `status` / `logs`）：三项仍要出现，但改动范围用固定短句「无运行态变更」，影响面无则「无」，避免复述整表；访问方式只列已知入口。突变 phase（`start` / `stop` / `restart`）写满具体服务名与端口变化。

## 安全与边界

- 只管理项目根内服务；命令在对应 `cwd` 执行。
- **绝不** kill 无关进程；身份不匹配或仅端口冲突时停下来问用户。
- 不默认按端口强杀；需用户明确授权。
- 需要 sudo / 改 systemd：说明并先征得同意。
- 缓存损坏 → 直接重新 discover。
- `.service-manager.md` 禁止密钥明文；可写「见 `.env` / 某环境变量名」。

---

## Self-evolution

本 Skill 具备经验积累、评估与持续进化能力。目录（均相对本 Skill 根目录）：

```text
<skill-dir>/
├── SKILL.md
├── examples/      # 经过验证的优秀执行案例
├── evals/         # 可验证成功标准
└── experience/    # 真实失败 / 成功 / 规律
```

不要为了自进化而破坏上文已规定的目标、流程、工具用法、输出与约束。没有真实案例时不要编造 `examples/` 条目。

### Examples

执行复杂任务前：检查 `examples/`；有相关案例则优先复用；没有则按上文正常执行。

### Evaluation

任务完成前对照相关 `evals/`（见 `evals/cases.yaml`）。优先确定性 Eval；失败则先修输出再交卷。

### Experience

仅在失败、用户纠正、明显成功、新方法或可复用经验时写入 `experience/`。不记 trivial；不伪造；不写密钥/内部 URL。单次失败 → `failures/`；规律需至少两次证据 → `patterns/`。

### Evolution

仅当 Experience 暴露可复用稳定模式时才改本 Skill。禁止单次失败直接改 `SKILL.md`。

实际更新生产 `SKILL.md` 时：

1. 不要直接覆盖原文；记录 version / change / reason / evidence / evaluation。有 Git 则优先靠 Git diff 留历史。
2. 若改动来自**真实执行经验**：优先委托 `skill-upgrader` 的 `evolve` 模式（`evolutions/` → 验证 → 晋升），不要本 Skill 自己改生产稿。
3. 若只是结构/规则的显式修订且环境有 `skill-upgrader`：走其 `update` 模式（`<skill-dir>/patches/`），仍须先提案再应用。
4. 未展示 Proposal 并获得用户确认前，不改生产 Skill。
