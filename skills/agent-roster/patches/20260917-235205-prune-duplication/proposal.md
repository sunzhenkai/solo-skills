# 按 writing-for-agents 去重与瘦身 SKILL.md 正文

- target: skills/agent-roster
- mode: update
- patch: 20260917-235205-prune-duplication
- risk: high
- status: proposed

## Intent

用 writing-for-agents 的三把尺（single source of truth、no-op 裁剪、context pointer 精简）压缩正文，让每条规则只有一个权威出处，行为本身不变。

目标改动：

1. `## 不变量` 从 10 条压到 4 条，并改换职责：不再是正文规则的第二份副本，而是「执行途中逐条自查」的清单，只留 patch 历史里真实被绕过过的四条（理由先写后执行、编排者不得自任、`acpx` 门禁与目标冻结、固化攒够必提案且需确认）。删掉的 6 条中有 3 条在正文说得较弱，补强到各自出处（见下）。
2. 删除 spine 后面复述 spine 的两句；只保留一句顺序不变量声明。
3. 删除「委派」节内联的契约输入/输出字段表。它是 `references/delegation-contract.md` 权威表的二手摘要，而 agent 要发出委派必然要读那份 reference，摘要不省一次读取。
4. 删除「换掉执行器不应改动本文件」——同一句已写在 `delegation-contract.md` 开头，且是给维护者而非运行期 agent 的话。
5. 删除探测器分工那段的「照搬设备台账」论证与「保留最近 1–2 条」，二者都由 `references/endpoint-schema.md` 权威表述；保留一句「Disposition 归人维护」并加上指针。
6. 「相关」里 `$skill-upgrader` 那条压成一句，不再重复「固化」节已经写清的两条去向。
7. frontmatter `description` 去掉「也不把名册与案例写进本仓库」——它不是触发条件，是正文内容，却要为此付出每轮常驻 token。
8. 若干句合并去掉衔接冗余（路由 1/2/4/5 项）。

非目标：不改流程顺序、不改门禁强度、不改权限模型、不动 `references/`、`scripts/`、`evals/`，不引入自进化结构。

## Conflict check

精简 `## 不变量` 触及安全门禁的呈现方式，逐条核对去向后确认规则本身全部保留：

| 原不变量 | 保留位置 | 处理 |
| --- | --- | --- |
| 名册/案例/路由/Run 不进本仓库 | 「数据在哪」首句 | 移出清单，原句并入首句（补强） |
| `routing.md` 不许凭想象写满 | 「路由」第 1 项 | 移出清单，补入「退化成硬编码分支」的理由（补强） |
| 本仓库运行时只读 | 「数据在哪」末段 | 移出清单，合并「连复制都不会发生」（补强） |
| 名册里没有的 Endpoint 就是不存在 | 「路由」第 5 项 | 移出清单，原句并入（补强） |
| 委派失败不靠重跑碰运气 | 「失败、超时与返工」 | 移出清单，正文已有且更细，未改 |
| 门禁阻塞冻结任务目标 | 「委派」第 3 项 + 自查清单第 3 条 | 并入 `acpx` 那条自查项 |
| 选择理由先写后执行 | spine 第 2 步 +「路由」第 4 项 + 自查清单 | 留在清单 |
| 编排者不得自任 | 「委派」自任段 + 自查清单 | 留在清单 |
| `acpx` 安装门禁三态 | 「委派」1–4 项 + 自查清单 | 留在清单 |
| 固化攒够必须提案 + 需使用者确认 | 「固化」动作段与末句 + 自查清单 | 留在清单 |

与其他 Skill 职责无冲突。`$skill-upgrader` 的引用关系保持不变。

## Rationale

正文 161 行里约 22 行是同义复述，其中「不变量」一节几乎整节复述。复述的代价不是 token，是漂移：`patches/20260917-220312` 与 `20260917-230721` 两轮修门禁时，正文和不变量表两处都得改，漏一处就自相矛盾。

保留 4 条自查项是一次有意的取舍：这四条在 patch 历史里真实被绕过过，重复陈述换来的强化值得那点漂移风险；其余 6 条没有这个证据，回到单一出处。清单改写成「执行途中逐条自查」，与正文段落职责不同，不再是同一句话说两遍。

可验证：改动全部是删除与合并，没有新增行为；`evals/cases.yaml` 的期望不涉及被删段落的措辞。

## Files

- `skills/agent-roster/SKILL.md` — 唯一被修改文件，161 行 → 148 行。

## Validation

- 应用前：`git apply --check --recount` 通过。
- 应用前：逐条核对上表 10 条不变量在正文均有出处。
- 应用后：`git diff --check` 通过；frontmatter `name` 仍为 `agent-roster`；正文内 4 个相对链接（`references/endpoint-schema.md`、`references/trace-format.md`、`references/delegation-contract.md`、`docs/adr/0003-*`、`CONTEXT.md`）指向的文件均存在。
- 应用后：无主机名、绝对家目录、项目名等隐私内容新增。
