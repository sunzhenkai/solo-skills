# Agent Skill 诊断（`skill`）

角色文件：仅在本角色生效时加载（见 [preload-protocol](../preload-protocol.md)）；职责边界以 [role-vocabulary](../role-vocabulary.md) 为准。级别：🔴 Blocker / 🟡 Major（门 3 默认报）/ ⚪ 默认不报，拿不准降一级。审查对象是 Agent Skill 本身（`SKILL.md` / `references/` / `tests/`），不是业务代码。

## 优先锚点

目标 skill 的 `SKILL.md`（frontmatter + 正文）、`references/`（按需加载结构）、`tests/`（文本契约）、`evals/` 与 `examples/`（若有）、README 中的安装 / 触发说明、调用方 skill 的引用点。

跳过：`scripts/` 的逐行实现（代码缺陷 → engineer）；skill 该不该存在的价值论证（→ product）。

## 诊断方法（`mode=ask`）

- 触发面用样例说话：评 description 时先各举 1 个「应触发」与「不应触发」的用户表述，再对照现状。
- 以契约为真相源：正文承诺的 MUST / 禁止，先在 `tests/` 里找对应断言；没有断言的承诺按「契约缺口」处理。
- 改动建议落到机制：优先协议 / 门禁 / 契约层面的通用解，不为单一场景特例化。

## 核心检查清单

每条附命中判据；判据不满足则不报，不为凑数降级描述。

1. 🔴 description 触发面：过宽误触（普通问答被拉进流程）或过窄漏触（目标场景进不来）；缺「何时不用」。
   命中判据：给出一个具体用户表述，按当前 description 会错误触发或错误不触发。
2. 🔴 指令不可检查：正文要求的行为无判据、无落点，执行者无法自检（「注意质量」「保持简洁」式空话）。
   命中判据：指出一条指令，两个独立执行者会产生可分辨的不同行为，且文中无判定标准。
3. 🟡 术语 / 协议漂移：同一概念（阶段名、门禁、状态值、路径）在 SKILL.md 与 references 间表述不一致。
   命中判据：同一概念两处以上不同写法，且差异会影响行为判断。
4. 🟡 预加载失控：MUST 先读取清单过大、references 未按需加载、无文件预算。
   命中判据：默认路径加载的文件数 / 体量无上限约束，或所有场景加载同一批大文件。
5. 🟡 契约测试缺口：正文新增 MUST / 禁止 / 落点，`tests/` 无对应文本契约断言。
   命中判据：指出一条正文承诺在 `tests/` 中无任何断言覆盖。
6. 🟡 职责越界：内嵌了其他 skill 的职责且缺 redirect。
   命中判据：指出一段指令与某既有 skill 的 description 重叠，且文中未 redirect。
7. ⚪ 公开仓纪律：正文 / 示例含个人、凭据、内部 URL 痕迹；运行产物约定写进 skill 目录。
8. ⚪ 自进化纪律：正文诱导自动进化（如「失败后自动更新本文件」），绕过 skill-evolver 的显式触发。

## 不算问题

- **文风与措辞偏好**：表达口味不报；只有影响行为判定的歧义（判据 3）才报。
- **缺 `examples/` `evals/` `experience/`**：自进化结构是显式升级决策（skill-upgrader 的 self-upgrade），缺失本身不是缺陷。
- **「还能写得更详细」**：无量化判据的润色建议不报。
- **`scripts/` 的代码风格**：归 engineer 的约定一致性条目，不在本角色重复。

## 下游建议

`skill-creator` → 新建或大改 skill；`skill-upgrader` → 可审计 patch 更新正文 / 结构；`skill-evolver` → 按真实执行经验进化（仅显式触发）。

## 跨角色 redirect

- skill ↔ engineer（`scripts/`）：SKILL.md / references 的触发、协议与契约质量 → skill；scripts/ 代码缺陷与质量 → engineer
- skill ↔ qa（契约测试）：正文承诺与 tests/ 断言的对应缺口 → skill；通用可测性与回归策略 → qa
- skill ↔ product（存在价值）：skill 该不该存在、合并还是拆分 → product；已存在 skill 的质量诊断 → skill
