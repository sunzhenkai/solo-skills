# result

## 状态

applied（2026-11-23）

## 验证摘要

- 单测：`python3 -m pytest tests/test_skills_store_contract.py -q` → 45 passed
  （新增 6 例：`test_hardcoded_secret_identifier_suffix_passes`、
  `test_hardcoded_secret_env_var_still_blocks`、
  `test_fixture_secret_values_warn_not_block`、
  `test_real_bearer_in_test_file_still_blocks`、
  `test_injection_fixture_literal_warns_not_blocks`、
  `test_injection_prose_in_test_file_still_blocks`）
- 既有守卫未回退：39 例全通过，含 `test_hardcoded_secret_blocks`、
  `test_mit_license_boilerplate_not_jailbreak`、`test_no_restrictions_still_blocks`、
  `SelfScanPasses`（skills-store 自身仍过审计）
- 用 archify 新 revision 的 5 条命中行构造临时 skill 目录重跑：
  `indentToken` 两行 → 通过（exit 0）；fixture token / Bearer 两行 +
  注入夹具一行 → 0 阻断 3 警告（exit 1）；SKILL.md 正文里的注入措辞 →
  仍 critical（exit 2）
