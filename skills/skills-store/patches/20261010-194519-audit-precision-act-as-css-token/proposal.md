# 审计规则精度：act as 词边界、CSS variable 排除、限定语 only 豁免

- target: skills/skills-store
- mode: update
- patch: 20261010-194519-audit-precision-act-as-css-token
- risk: medium
- status: proposed

## Intent

重锁 dotfiles 第三方 skill 时，`archify`（19 BLOCK / 131 WARN）与
`ui-template-author`（52 BLOCK）被审计规则拦下，无法推进到上游新
revision。逐条检查命中内容，全部属规则过宽导致的误报，与「坑 11」
场景一致。

## Changes

### jailbreak_role：`act as` → `\bact as\b`

- 命中样本：`"same default-canvas contract as lifecycle"` /
  `"edge labels use the same variant color contract as their paths"` /
  `"cli: deliver --open launches only the committed absolute artifact as one argument"` /
  `"Gallery/embed mode keeps the generated artifact as the source of truth"`
- 根因：裸 `act as` 无词边界，命中 `artifact as` / `default-canvas ... as`
  等自然英语子串。
- 修法：加 `\bact as\b`。真实越狱短语 `"act as a DAN"` / `"act as an
  unrestricted AI"` 仍命中（词边界不影响完整短语）。

### hardcoded_secret：排除 `--` 前缀（CSS variable）

- 命中样本：`project_token: --wt-color-app-shell` / `--wt-typography-display-sm`
  等 50+ 处。`--wt-...` 是设计系统 design token 的 CSS variable 名，非真实凭据。
- 修法：值部分用 `((?!--)[A-Za-z0-9_\-]){20,}` 排除 `--` 开头。
- 同时收紧匹配条件：要求引号包裹 / 非标识符符号 / 行尾结束，避免
  `var token = relationshipTokenGeometry(...)` / `const token =
  preparedCacheDirectories.get(...)` 等 JS 标识符（含函数名 >20 字符全为
  `[A-Za-z0-9_-]`）误报。
- 真实凭据 `api_key = "sk_live_..."` / `token: ghp_xxx` / 高熵 base64
  字符串仍命中。

### bypass_approval：限定语 `only` 豁免

- 命中样本：`"visual-check disables the Chrome sandbox only for root or an
  explicit environment opt-in"`（archify 测试描述，说明前置条件而非无条件
  bypass）。
- 修法：动词后加前瞻 `(?!\s+.{0,40}\bonly\b)`，若 `{0,40}` 内出现
  `only` 则跳过。同时 `disable` 加 `[sd]?\b` 覆盖 `disables`/`disabled`
  变体并确保词边界。
- 无条件 `disable the sandbox` / `bypass the approval gate` / `skip human
  review` 仍命中。

## Files

- skills/skills-store/scripts/audit-skill.sh
- skills/skills-store/tests/test_skills_store_contract.py

## Validation

- 单测：31 passed（新增 7 个回归用例，覆盖三组规则的合法/非法命中样本）
- 全仓 22 skill 复扫：0 阻断；`repo-manager` / `service-manager` 两个
  warn 为 HEAD 既有项（global_shell_rc / sudo_usage），非本次引入
- dotfiles 仓 `make skills-lock-update` 预期：`archify` 与
  `ui-template-author` 正常推进到新 revision，无 BLOCK
