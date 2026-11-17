# push 前扫描密钥内容

- target: skills/commit-push
- mode: update
- patch: 20261118-014312-secret-scan-before-push
- risk: high
- status: proposed

## Intent

push 前增加一次内容级密钥扫描：有 `grepom` 时在仓库根用 `grepom push -- <参数>` 代替 `git push <参数>`，命中即拒推并报告规则 / 文件 / 行号；`grepom push -f` 只在用户针对具体命中确认误报后使用；没有 `grepom` 时照常推送并在收尾写明「未做密钥扫描」。非目标：暂存、提交说明、确认门禁与冲突处理不变；不新增硬依赖。

## Conflict check

none。`repo-manager` 的多仓 push 已要求 `grepom push`（`references/git-ops.md`「安全 push 与 secret scan」），单仓路径此前只按文件名排除，两条路径的防护等级不一致；本改动对齐。

## Rationale

文件名排除挡不住写进代码或配置的密钥，而单仓提交推送是最常用路径。`grepom push --help`（v0.1.13）：先扫当前目录，命中默认拒推；`-f` 表示忽略扫描结果，`--` 后参数透传给 `git push`。

## Files

- skills/commit-push/SKILL.md：安全默认句补一句；新增「push 前扫密钥」节；收尾告知是否扫描。
- skills/commit-push/tests/test_commit_push_contract.py：新增 `test_secret_scan_before_push`。

## Validation

- `python3 -m pytest skills/commit-push/tests -q`
