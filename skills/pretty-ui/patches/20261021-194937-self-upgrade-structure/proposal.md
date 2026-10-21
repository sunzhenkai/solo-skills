# 补齐自进化结构（examples / evals / experience）

- target: skills/pretty-view-html
- mode: self-upgrade
- patch: 20261021-194937-self-upgrade-structure
- risk: medium
- status: proposed

## Intent

按仓库约定「结构缺失先走 skill-upgrader 一次性升级结构」，为本 skill 补齐 `examples/`、`evals/`、`experience/`，并在 SKILL.md 末尾追加一句自进化指针。`tests/` 里原有的两份虚构源稿和手工提示词本质是评测素材：源稿移到 `evals/fixtures/`，提示词改写成 `evals/cases.yaml` 里的 case；`tests/` 腾空，留给下一轮的契约测试。

非目标：不改工作流、视觉规则、文件组织和完成检查；不改名（改名在下一轮单独做）；不编造案例或经验。

## Conflict check

none。`tests/.gitignore` 忽略的 `golden/` 是生成产物目录，按仓库「运行产物落仓库之外」的约定，生成结果改写到 skill 目录之外，不再需要这条忽略规则。

## Rationale

cases 全部从现有 SKILL.md 与 `references/organization.md`、`references/visual-components.md` 抽取：默认输出目录、事实保真、默认单页、同主题需确认、相对链接基准（对应历史补丁 index-relative-links 的事故）、同名不覆盖、图解嵌入且可离线、静态页基础属性。每条都能按产物文件独立判定。

## Files

- `skills/pretty-view-html/SKILL.md`：末尾追加自进化指针
- `skills/pretty-view-html/examples/README.md`：新增（无真实案例，只放约定）
- `skills/pretty-view-html/evals/README.md`、`evals/cases.yaml`：新增
- `skills/pretty-view-html/evals/fixtures/{beacon-ttl,marine-life}/SOURCE.md`：从 `tests/fixtures/` 移入
- `skills/pretty-view-html/experience/README.md` 与三个 `.gitkeep`：新增
- `skills/pretty-view-html/tests/.gitignore`、`tests/prompt.txt`：删除

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/pretty-view-html`；`python3 -m pytest tests -q`（含 evals 结构检查）；`make check-style`
