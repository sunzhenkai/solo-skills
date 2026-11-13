# 默认写入项目 docs/atlas

- target: skills/project-atlas
- mode: update
- patch: 20261113-090605-default-docs-atlas
- risk: medium
- status: proposed

## Intent

`atlasctl init` 未传 `--root` 时写入 `<source>/docs/atlas`；其他命令未传 `--root` 时读取当前项目根的 `docs/atlas`。显式 `--root` 继续覆盖默认值。

## Conflict check

保留现有 Atlas 布局、Archify 集成和显式路径兼容，只增加缺省落点，不改变已有 Atlas 的内容或校验规则。

## Rationale

与 wiki-data 的 `docs/wiki` 形成一致的项目文档约定；CLI 默认值与正文一致，可通过真实初始化和参数覆盖测试验证。

## Files

- `skills/project-atlas/SKILL.md`：使用 `docs/atlas` 默认路径与简化命令。
- `skills/project-atlas/scripts/atlasctl.py`：实现 init 和其他命令的默认根。
- `skills/project-atlas/tests/test_atlasctl.py`：覆盖默认 init 与显式覆盖。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：守卫文档路径约定。
- `skills/project-atlas/evals/cases.yaml`：声明默认落点。

## Validation

- `git apply --check --recount`。
- `python3 -m pytest skills/project-atlas/tests -q`。
- 真实 CLI 无 `--root` 初始化和检查。
- 全仓测试、名称与风格检查。
