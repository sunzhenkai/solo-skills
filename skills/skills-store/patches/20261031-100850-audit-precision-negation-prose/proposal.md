# 审计规则精度：bypass_approval 否定句、jailbreak_role 的 act as 宾语

- target: skills/skills-store
- mode: update
- patch: 20261031-100850-audit-precision-negation-prose
- risk: medium
- status: proposed

## Intent

重锁 dotfiles 第三方 skill 时，`archify`（3 BLOCK）与 `taste-skill`（10 BLOCK）
被审计规则拦下，无法推进到上游新 revision。逐条看命中行，全部是规则过宽
导致的误报；两者的旧 revision 在同一份规则下都是干净的，说明是**上游新增
文案**撞上了旧规则，而不是上游变危险。

## Changes

### bypass_approval：动词前的否定词豁免

- 命中样本：`references/delivery-contract.md:481`
  `parent. Archify does not suppress browser de-elevation or disable the sandbox`；
  `bin/visual-check.mjs:1614`
  `'Archify does not disable browser de-elevation or the sandbox to preserve pipe handles.'`
- 根因：规则的 disable 分支只看 `disable ... sandbox` 的邻近关系，`does not`
  这类否定把「声明不越权」读成了越权。
- 修法：在 `scan_text_file` 的按规则跳过分支里加 `bypass_approval` 一类：
  动词前 5 个 token 内出现 `not` / `never` / `no longer` / `cannot` 即跳过。
  否定词只认动词**前**的：`disables the sandbox without any approval` 这类
  真越权是动词在前、`without` 在后，仍然阻断（既有用例守住）。

### jailbreak_role：`act as` 要求角色名词宾语

- 命中样本：`library/sites.json` / `library/sections.json` 里的设计文案
  `bursts of white light act as the scene changes behind the pouch`、
  `Row of four equal dark cards that act as site controls`。
- 根因：上一轮把 `act as` 收紧到 `\bact as\b` 只解决了子串问题（`artifact as`），
  自然英语里 `act as <普通名词>` 仍照原样命中。
- 修法：`act as` 要求后接可选冠词 + 角色名词（`dan|ai|assistant|agent|
  admin|root|system|model|persona|character|god|expert|developer|
  jailbroken|unrestricted|evil|human|user|person`）。`act as a DAN`、
  `act as an unrestricted AI` 仍命中。

## 不做的事

- 不放宽 `credential_paths` 的 `~/.ssh` 分支。`senv-cli` 的阻断是既定策略
  （机器特例走被审 skill 自己的 `.audit-allow`），代码里有用例
  `test_ssh_config_passes_but_senv_now_blocks` 明确守住。

## 第二轮（同一次重锁跟进）

首轮修完重锁，剩两处：

### credential_paths：`.ssh` / `.netrc` 要求路径前缀

- 命中样本：`archify/explainer/sources.mjs:14`
  `const SECRET_NAME = /^(?:\.env(?:\..*)?|\.npmrc|\.netrc|\.(?:ssh|aws|gnupg|kube)|…`
- 根因：`~/?\.ssh` 的 `~/?` 可整体缺省，`\.netrc` 干脆没有前缀要求，于是**敏感
  文件名模式表**（用于过滤/脱敏，恰好与读取凭据相反）命中。
- 修法：两处都要求前置 `~` 或 `/`；`~/.ssh/config` 的既有豁免、
  `/.ssh/id_` 兜底、`~/.ssh/senv/` 仍阻断均不变。

### jailbreak_role：否定句里的 `pretend to be`

- 命中样本：`taste-skill/scripts/draw.mjs:516`
  `photographs only where they plainly do not pretend to be the product`
- 修法：沿用否定词豁免分支，`jailbreak_role` 与 `bypass_approval` 共用；
  `pretend to be an unrestricted AI` 仍阻断。
