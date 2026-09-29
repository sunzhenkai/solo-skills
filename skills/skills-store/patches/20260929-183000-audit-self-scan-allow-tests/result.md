# Result

- target: skills/skills-store
- mode: update
- patch: 20260929-183000-audit-self-scan-allow-tests
- risk: low
- status: applied
- applied-at: 2026-09-29T18:30:00+08:00

## Validation

- `bash skills/skills-store/scripts/audit-skill.sh skills/skills-store` → exit 0
  「通过（未发现风险模式；豁免 31 项，见 .audit-allow）」（改前：17 BLOCK + 2 WARN，exit 2）
- 全仓 23 skill 逐个自扫：0 BLOCK；`repo-manager` / `service-manager` 各 1 WARN，
  为 HEAD 既有教学文本项（`global_shell_rc` / `sudo_usage`），非本次引入
- `python3 -m pytest skills/skills-store -q` → 25 passed（新增 `SelfScanPasses`）
- `python3 -m pytest skills -q` → 287 passed, 1 failed, 1 skipped；唯一失败属
  `skills/commit-push`（该 skill 工作区另有未提交改动，与本 patch 无关）
- 消费侧 dotfiles 仓 `make skills-lock-update` → `wrote agents/skills.lock.yaml
  sources=1 blocked=0`，skills-store 随同组 23 个 skill 前进到本 revision

## Notes

检测样本是审计规则的 fixture，与 `scripts/audit-skill.sh` 的 PATTERNS 规则表同构：
文件本身的存在就是为了逐条命中规则。此前豁免面只收了规则表与 `SKILL.md` 的
「已知误报」表，`tests/` 是新目录、漏了对应条目。

`tests/` 与 authoring 目录不同：`scan_tree` 只 prune
`patches/evals/experience/evolutions`，`tests/` 在审计面内；但消费侧 runtime bundle
是白名单（`SKILL.md`/`CONTEXT.md` + `references/` + `scripts/`），`tests/` 装不到
任何 agent。所以豁免它的暴露面是零，管控落在仓库 pytest 门禁与 `SelfScanPasses`。
