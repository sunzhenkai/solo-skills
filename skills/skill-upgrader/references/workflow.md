# 工作流（update / self-upgrade 共用）

## 工作流（两模式共用）

复制并勾选：

```text
Progress:
- [ ] 模式门禁（update | self-upgrade | evolve→evolve.md | abort→create）
- [ ] 定位并完整读取现有 SKILL.md
- [ ] 前置判断（意图 / 冲突 / 合理性）
- [ ] 写 proposal.md（尚未改生产文件）
- [ ] 判定风险并准备 change.patch
- [ ] git apply --check
- [ ] 风险门禁确认（medium/high）
- [ ] git apply + 验证
- [ ] 写 result.md
```

### 1. 模式门禁与定位

锁定模式与 `<skill-dir>`。目标不存在或名称不唯一时先询问。

### 2. 提案

先完成前置判断，再写本轮 `proposal.md`。一次 patch 只解决一个内聚问题；`self-upgrade` 可将「补齐三目录 + 注入」视为同一内聚问题，但不要夹带无关正文重写。

### 3. 风险

| 风险 | 典型改动 | 应用门禁 |
|------|----------|----------|
| `low` | 错别字、链接、示例、不改变行为的澄清；幂等补齐空 README/`.gitkeep` | patch 校验通过后可直接应用 |
| `medium` | 工作流、输出契约、多文件行为；标准 `self-upgrade`（追加注入 + 建目录） | 展示摘要与 diff，获得用户明确确认 |
| `high` | 触发条件、权限、副作用、安全门禁、删除能力、大范围重写 | 展示风险与 diff，获得用户明确确认 |

不确定时提高一级。用户已明确批准**具体改动内容**可视为已通过对应门禁；笼统的「优化一下」不算批准中高风险 diff。标准 `self-upgrade` 默认至少 `medium`。

### 4. 先写 patch

创建本轮 patch 目录与 `proposal.md`，再编写 `change.patch`。此时不得编辑目标生产文件。

patch 必须：只含 proposal 声明的改动；上下文足以精确应用；新文件用 `/dev/null`；不含 patch 目录自身、临时文件或同步镜像。

生成 `change.patch` 用机械方式，不手写 hunk：把原文与改后内容各放一份副本（如 `<tmp>/a/<rel>`、`<tmp>/b/<rel>`），在副本根目录执行 `git diff --no-index a/<rel> b/<rel>`，再把路径前缀 `a/a/`→`a/`、`b/b/`→`b/` 规整为仓库根相对路径。

手写 hunk 的四个已知失败（每个都让 `git apply` 直接拒收，报错只给行号，排查耗时）：hunk 头计数与 body 不符、hunk 体内有空行、diff 头缺 `+++` 行、hunk 末行是 `+`/`-` 而非上下文行——`git apply` 默认要求上下文行（实测：只带尾部上下文即可通过，缺尾部上下文的一律 patch does not apply），零上下文须 `--unidiff-zero`，不要用。

### 5. 校验与门禁

在 Git 仓库根执行：

```bash
git apply --check --recount "<skill-dir>/patches/<patch-id>/change.patch"
```

校验失败时只修 `change.patch`，不得绕过或直接改生产文件。通过后按风险等级执行确认门禁。

### 6. 应用与验证

```bash
git apply --recount "<skill-dir>/patches/<patch-id>/change.patch"
git diff --check -- "<skill-dir>"
```

核对：实际 diff 与 proposal/`change.patch` 一致；`SKILL.md` frontmatter 合法且 `name` 与目录名一致；引用路径存在；无隐私泄露；未改镜像目录或历史 `patches/`。

改到被别处引用的规则时，grep 一遍读者（唯一真源 / 执行侧 phase 文档 / 模板 / 其他 Skill），同轮一并更新，避免悬空引用；目标 Skill 自带契约测试时，同轮补一条守卫断言——别把「测试没红」当成「规则已守卫」。

`git diff --check` 只对改动的生产文件跑：patch 文件里的空上下文行必然被报成 trailing whitespace，那不是生产文件的问题。

`self-upgrade` 另跑下方「Final Validation」。`update` 则跑目标 Skill 自带的相关测试或确定性检查（若有）。

### 7. 写结果

写 `result.md`。失败则 `status: failed`，保留证据并停止；修复必须**新** patch 目录。

不要自动 sync、commit 或 push。

---
