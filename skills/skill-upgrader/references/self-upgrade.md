# 模式：self-upgrade 细则与 Final Validation

## 模式：self-upgrade

最终目标：把静态 `SKILL.md` 升级成能从真实执行积累经验、并以 Eval 驱动改进的 Skill。**升级本身的文件写入也必须经 patch 应用**，不要直接 `mkdir`/写生产文件。

输入：

```text
my-skill/
└── SKILL.md
```

升级后：

```text
my-skill/
├── SKILL.md
├── examples/
├── evals/
├── experience/
└── patches/          # 本轮与后续审计记录（本模式创建的首轮 patch 即在此）
```

目录模板、Eval schema、注入正文见（均只读一层）：

- [layout.md](layout.md) — 复制清单
- [evals.md](evals.md) — 抽取规则与 schema
- [skill-injection.md](skill-injection.md) — 追加到目标 SKILL.md 的原文
- [examples-README.md](examples-README.md) / [evals-README.md](evals-README.md) / [experience-README.md](experience-README.md) / [cases.template.yaml](cases.template.yaml) — 复制源
- [patch-protocol.md](patch-protocol.md) — 本轮 patch 记录格式

### Preserve the original Skill

完整读取现有 `SKILL.md`（及其声明要读的 `references/` / `scripts/`）。不要为了自进化破坏原有行为；不要重写无关段落。

幂等：若 `examples/` `evals/` `experience/` 已存在，保留已有文件；只补缺失的 README / 空目录 / 注入段落。已有 `evals/cases.yaml` 不覆盖，只追加从原文抽出且尚未覆盖的 case。已有同等「Self-evolution」段落则不要再贴一份。

若三目录与注入均已齐全 → `decision: already-upgraded`，不写无意义空 patch。

### 组装内容（写入 change.patch）

1. **examples/** — 仅 README 与约定；无真实成功案例不编造。
2. **evals/** — `README.md` + `cases.yaml`；从原文抽可验证标准；优先确定性 Eval。
3. **experience/** — README + `failures/` `successes/` `patterns/`（空目录 `.gitkeep`）；不伪造历史。
4. **SKILL.md** — 末尾追加与 [skill-injection.md](skill-injection.md) 一致的正文（只替换 `<skill-dir>`）；不改写语气或删减门禁。

细节清单见 [layout.md](layout.md)。

### Evolution Criteria（写入目标后的行为约束）

Experience 进入 Skill 正文前须：可复用、有证据、能改善结果、不破坏已有能力、可通过 Eval。一次性特例只留 Experience。

实际改生产正文：经验驱动走本 skill 的 `evolve` 模式（`evolutions/`）；显式修订走 `update` 模式（`patches/`）。禁止单次失败直接改 `SKILL.md`。

---

## Final Validation（self-upgrade）

```text
[ ] 原始 Skill 能力未丢失
[ ] examples/ 已建立
[ ] evals/ 已建立
[ ] experience/ 已建立
[ ] Eval 能覆盖核心能力
[ ] 没有伪造历史经验
[ ] Skill 知道如何读取 examples
[ ] Skill 知道如何运行/参考 evals
[ ] Skill 知道什么时候记录 experience
[ ] Skill 不会因为单次失败修改自己
[ ] 本轮改动经由 patches/ 应用且 result 已写
```

任一项未完成则补齐或 `failed`，不要声称已升级。
