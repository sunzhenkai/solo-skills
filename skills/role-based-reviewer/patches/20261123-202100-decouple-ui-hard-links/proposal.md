# 解除 role-based-reviewer 对 ui-kit 与 pretty-ui 的相对路径硬依赖

- target: skills/role-based-reviewer
- mode: update
- patch: 20261123-202100-decouple-ui-hard-links
- risk: medium
- status: proposed

## Intent

将 `references/roles/design.md` 中指向 `pretty-ui`/`ui-kit` 的相对链接改为反引号可选文件锚点 + 未安装降级说明，使后端/通用岗位评审可单独安装 `role-based-reviewer`。

## Conflict check

配套修改：README「依赖组」、taskrail（20261123-202000-decouple-ui-hard-links）。

## Rationale

design 只是 10 个岗位之一，不应通过相对路径硬链接强制所有 role-based-reviewer 安装者捆绑整套 UI skill。

## Files

- `skills/role-based-reviewer/references/roles/design.md`：pretty-ui/ui-kit 相对链接改为可选锚点与降级说明
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`：更新断言为可选跨 skill 锚点存在性并禁止相对硬链接

## Validation

- `git apply --check --recount skills/role-based-reviewer/patches/20261123-202100-decouple-ui-hard-links/change.patch`
- `python3 -m unittest discover -s skills/role-based-reviewer/tests -p 'test_*.py'`
- `make check-style && make check-names`
