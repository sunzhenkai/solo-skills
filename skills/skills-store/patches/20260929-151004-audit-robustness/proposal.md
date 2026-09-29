# 审计脚本健壮性：fail-open 消除、JSON 合法化、扫描面补洞、个人豁免出共享集

- target: skills/skills-store
- mode: update
- patch: 20260929-151004-audit-robustness
- risk: medium
- status: proposed

## Intent

review（2026-09-29，glm-5.3 版）实证四个问题：

1. 全部规则依赖 grep -P（PCRE），BSD grep 等无 PCRE 环境下 `|| true`
   吞错 → 规则静默零命中 → exit 0「通过」。安全工具 fail-open。
2. --json 用 printf %q（shell 引用）拼 JSON，snippet 含空格/中文即非法。
3. 无扩展名文本文件（如 scripts/setup）既不进文本扫描，二进制扫描又只认
   ELF/Mach-O/PE32，完全逃逸审计面。
4. credential_paths 硬编码排除 ~/.ssh/senv/ 是为个人私有工具开的永久口子，
   违反「机器特例不进共享规则集」自家原则。

## Changes

1. 入口探测 grep -P 可用性，不可用报错 exit 2（显式失败，不放行）。
2. --json 改走 python3（标准库 json）序列化，FINDINGS 经 tab/管道分隔传入。
3. scan_tree 对非文本扩展名文件按 MIME 判定：非二进制一律进文本扫描；
   .audit-allow 本身是豁免配置（hash 入锁、非 skill 内容），排除避免自指。
4. 移除 senv 豁免，个人环境特例改由被审 skill 的 .audit-allow 承接；
   SKILL.md 误报表同步。另修 SKILL.md 两处断链/私仓引用（sync.sh、
   dotfiles skills-archive 路径）。

## Files

- skills/skills-store/scripts/audit-skill.sh
- skills/skills-store/SKILL.md

## Validation

- 全仓 22 skill 复扫：0 阻断；repo-manager / service-manager 两个 warn 为
  HEAD 既有项（global_shell_rc / sudo_usage 教学内容），非本次引入
- --json 经 python json.load 验证合法
- python3 -m pytest skills -q 全绿
