# 禁止 grepom push 用 || git push 回退

- target: skills/commit-push
- mode: update
- patch: 20261124-151600-no-fallback-on-grepom-push
- risk: low
- status: applied

## Intent

在「push 前扫密钥」中明确要求先用 `command -v grepom >/dev/null 2>&1` 探测工具存在性，禁止写成 `grepom push || git push`，避免将 `grepom` 扫描拦截（非 0 退出码）误判为命令不存在而绕过闸门直接 `git push`。

## Files

- `skills/commit-push/SKILL.md`
- `skills/commit-push/tests/test_commit_push_contract.py`
