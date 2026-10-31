# result

## 状态

applied（2026-10-31）

## 验证摘要

- 单测：`python3 -m pytest tests/test_skills_store_contract.py -q` → 35 passed
  （新增 `test_bypass_approval_negation_passes`、`test_act_as_prose_passes`）
- 既有守卫用例未回退：`test_bypass_approval_unconditional_still_blocks`
  （含 `disables the sandbox without any approval`）、
  `test_bypass_approval_only_qualifier_passes`、`test_act_as_dan_still_blocks`、
  `test_no_restrictions_still_blocks`、`test_ssh_config_passes_but_senv_now_blocks`
- 真实上游文件复核：把新 revision 的 `archify/explainer/sources.mjs` 与
  `taste-skill/scripts/draw.mjs` 放进临时 skill 目录审计 → 通过（exit 0）
- dotfiles 重锁（第四轮，c0d8ead）：`sources=3 blocked=1`——`archify`、`taste-skill` 推进；
  `changed_content=3`（archify / skills-store / taste-skill），`make registry validate` 通过
- `senv-cli` 仍阻断，属既定策略，不在本 patch 范围

## 后续

- `senv-cli` 需要在 `solo-kingdom/senv` 的 skill 目录补 `.audit-allow`
  （`credential_paths|<相对路径>|<命中行 ERE>`），属另一个仓的改动
