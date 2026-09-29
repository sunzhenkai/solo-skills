# 自扫豁免补 tests/ 检测样本，并加 self-scan 门禁

- target: skills/skills-store
- mode: update
- patch: 20260929-183000-audit-self-scan-allow-tests
- risk: low
- status: applied

## Intent

`609ebe5` 引入 `tests/test_skills_store_contract.py`（检测样本 fixture）后，skills-store
对自己的 `audit-skill.sh` 扫不过：17 BLOCK + 2 WARN，规则为 `destructive_rm_root`、
`credential_paths`、`jailbreak_role`、`hardcoded_secret`、`eval_external`（另两条
warning 同文件同性质）。全部命中都在该测试文件内，其余文件 0 命中。

消费侧后果：本仓的 lock 更新器以「被锁 revision 自带的 audit-skill.sh + 自带
`.audit-allow`」为审计真相，skills-store 因此每轮重锁都 `keep @ 旧 revision`，
把整把锁的 blocked 计数长期挂住。

## Changes

1. `.audit-allow` 新增第 3 类自指内容说明，并加一条整文件豁免
   `*|tests/test_skills_store_contract.py|*`——与既有
   `*|scripts/audit-skill.sh|*` 同构。豁免理由不止「自指」：`tests/` 不在消费侧
   runtime bundle 白名单内（`agents/runtime.yaml` 只发 `SKILL.md`/`CONTEXT.md` +
   `references/` + `scripts/`），检测样本随 skill 发布不到任何 agent。真实管控是
   仓库门禁 `python3 -m pytest skills -q`，与被豁免文件里的断言同生死。
2. `tests/test_skills_store_contract.py` 新增 `SelfScanPasses`：实跑
   `audit-skill.sh` 扫 skills-store 自身，断言无 `[BLOCK]` 且 exit 0。
   下次再加检测样本而漏更新豁免面时，本仓 pytest 先炸，而不是把阻断抛给消费侧锁。

未采用的方案：逐行锚点豁免（5 条规则 × 19 处，每加一个 fixture 都要补一行，
正是本次漏补的成因）；把 fixture 挪到 `tests/` 之外（对消费侧无收益，只把
自指问题换个目录）。

## Files

- skills/skills-store/.audit-allow
- skills/skills-store/tests/test_skills_store_contract.py

## Validation

- `bash skills/skills-store/scripts/audit-skill.sh skills/skills-store` →
  exit 0，「通过（未发现风险模式；豁免 31 项，见 .audit-allow）」
- 全仓 23 个 skill 逐个自扫：0 BLOCK；仅 repo-manager / service-manager 各 1 WARN
  （既有教学文本项，非本次引入）
- `python3 -m pytest skills/skills-store -q` → 25 passed
- `python3 -m pytest skills -q` → 287 passed, 1 failed, 1 skipped；唯一失败是
  `skills/commit-push`（该 skill 工作区另有未提交改动，与本 patch 无关）
