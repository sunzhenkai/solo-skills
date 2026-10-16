---
id: skills-store
name: skills-store
description: "用 npx skills（vercel-labs/skills）搜索、安装、移除、更新 Agent Skills，外部 skill 安装前做安全审计。用户提及 skills store、技能商店、安装或搜索 skill、npx skills、skills.sh 时使用。"
---

# 技能商店

面向用户的输出默认使用简体中文。命令名、路径、代码、状态值与既成术语保持原文。

通过 [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI 管理 Agent Skills，入口 `npx skills`（无需全局安装），发现目录 https://skills.sh/ 。命令、参数与用户说法→动作映射见 [references/cli.md](references/cli.md)，参数以 `npx skills --help` 为准。

## 作用域

安装、移除、更新都要落在明确的作用域上：用户说了就照用户的；没说时先问清项目还是全局（这是写入位置，猜错要返工）。

| 作用域 | 含义 | 标志 |
|--------|------|------|
| **项目**（当前目录） | 写入当前项目 `./<agent>/skills/`，可随仓库共享 | 不加 `-g`；update 用 `-p` |
| **全局** | 写入用户目录 `~/.../skills/`，跨项目可用 | `-g` / `--global` |

执行前用一句话复述作用域，例如「将安装到**当前项目**」。非交互环境加 `-y`。

## 硬性规则：外部 Skill 安全审计

**凡来源非本仓库 `skills/` 的安装与更新，一律先审计、再安装。**

| 场景 | 是否审计 |
|------|----------|
| `npx skills add` 远程仓库 / URL | **必须** |
| `npx skills add` 本地路径（非本仓库真相源） | **必须** |
| `npx skills update` | **必须**（对新版本重新审计） |
| 本仓库 `skills/` 经 sync 分发 | 已由仓库维护，无需重复审计 |
| `find` / `list` / `use`（不安装） | 不审计 |

审计脚本（与本 SKILL.md 同目录）：

```bash
# 项目内 skill 自带脚本
SKILL_ROOT="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]:-$0}")")")"
AUDIT="$SKILL_ROOT/scripts/audit-skill.sh"

# 或按安装位置：
# 项目: .cursor/skills/skills-store/scripts/audit-skill.sh
# 全局: ~/.cursor/skills/skills-store/scripts/audit-skill.sh
```

### 安装前工作流（先临时拉取 → 审计 → 再正式安装）

```
1. 确认作用域（项目 / 全局）与 skill 名称
2. 拉取到临时目录（不写入 agent skills 目录）
3. 对目标 skill 目录运行 audit-skill.sh
4. 按审计结论：阻断 / 警告待确认 / 通过
5. 通过或用户确认后，执行 npx skills add
6. 删除临时目录，list 核对
```

#### 步骤 2：临时拉取

```bash
AUDIT_DIR="$(mktemp -d /tmp/skills-audit.XXXXXX)"
trap 'rm -rf "$AUDIT_DIR"' EXIT

# owner/repo 或 GitHub URL → 浅克隆
git clone --depth 1 "https://github.com/<owner>/<repo>.git" "$AUDIT_DIR/src"

# 若 source 已是本地目录
# cp -a /path/to/repo "$AUDIT_DIR/src"

# 列出仓库内 skill（辅助定位子目录）
npx skills add <source> --list
```

定位待审目录 `<skill-path>`：

- 单 skill 仓库：通常为 `$AUDIT_DIR/src` 或 `$AUDIT_DIR/src/<skill-name>/`
- 多 skill 仓库：含 `SKILL.md` 的子目录，与 `--list` 输出一致
- 用 `find "$AUDIT_DIR/src" -name SKILL.md` 辅助

#### 步骤 3–4：审计与处置

```bash
bash "$AUDIT" "$AUDIT_DIR/src/<skill-path>"
# 可选 JSON：bash "$AUDIT" "$AUDIT_DIR/src/<skill-path>" --json
```

| 退出码 | 含义 | Agent 行为 |
|--------|------|--------------|
| `0` | 通过 | 继续安装 |
| `1` | 有警告 | **暂停**，向用户展示 findings，**必须**获得明确同意（如「仍要安装」） |
| `2` | 有阻断项 | **停止安装**；逐条复核（见下），说明原因，建议换来源或自行审查后改本地安装 |

向用户报告审计摘要时给规则名、文件、行号与截断片段；可能含密钥的完整匹配内容只留在本地。

**复核通道（阻断项）**：脚本靠关键词正则命中，判不出上下文，误报是常态。`exit 2` 时 **MUST** 打开每处命中读原文，逐条给出「真风险 / 误报」的判断与依据，再交用户决定。判为误报时，等用户针对该条明确豁免后再继续安装。规则集保持原样放行：**禁止**为了给某个 skill 放行而删规则或放宽关键词——那只会让下一个 skill 漏检；过宽 token、误把纯文本当二进制这类精度修复，另走本 Skill 的更新流程（skill-upgrader）。已知误报对照 [references/known-false-positives.md](references/known-false-positives.md)。

**审计范围与豁免**：审计面=安装面。`patches/`、`evals/`、`experience/`、`evolutions/` 是 authoring 数据、不进 runtime bundle，不扫描。被审 skill 可在根下放 `.audit-allow` 豁免自指文本（skill 文档逐字讲解规则样例、审计工具自身源码必然自命中）：每行 `规则|相对路径|snippet 的 ERE`，规则与路径可写 `*`，snippet 字段为 `*` 表示该路径全豁免；只豁免逐字命中行，豁免项以计数展示。`.audit-allow` 随 skill 内容 hash 入锁，改动可审计。豁免只收编自指文本，新内容一律照常上报。

**`-s '*'` / `--all` 批量安装**：应对**每个** skill 子目录分别审计；任一阻断则整批中止，除非用户明确只要通过项。

用户说「跳过安全检查 / 强制安装」时：仍执行审计并展示结果。警告级可由用户明确承担风险后放行；阻断级**不接受**这类笼统口令，必须先逐条复核、给出误报依据，再由用户针对具体条目明确豁免。

#### 步骤 5：正式安装

审计通过（或用户已逐条豁免）且作用域已确认后，按 [references/cli.md](references/cli.md) 执行 `npx skills add`，装完 `list` 核对。`update` 同样先对上游新版本重新审计；`remove` 同样带作用域。

## 与本仓库 agents 同步的关系

本仓库共享 skills 真相源在 `skills/`，由 dotfiles 编目（`dotf agents -c`）同步到共享的 `~/.agents/skills/`。

- **skills-store 安装的第三方 skill** 落在各 agent 的 project/global skills 目录，**不**自动进入 `skills/`。
- 要纳入本仓库统一真相源：先审计通过，再拷贝或改写到 `skills/<id>/`，然后 sync。
- `~/.agents/skills/` 由 sync 生成，改动回源仓 `skills/` 再同步。

## 执行清单（做完的标志）

```
- [ ] 已确认操作：find / add / list / remove / update / use
- [ ] add / update 外部来源：已临时拉取并完成 audit-skill.sh
- [ ] 阻断项已拒绝或逐条豁免；警告项已获用户明确确认
- [ ] add / remove / update 已明确：项目 或 全局
- [ ] 需要时已指定 -a <agent> 与 -s <skill>；非交互加 -y
- [ ] 临时目录已清理；执行后 list 核对并告知用户路径含义
```

经验沉淀与正文演进走 `skill-upgrader`。
