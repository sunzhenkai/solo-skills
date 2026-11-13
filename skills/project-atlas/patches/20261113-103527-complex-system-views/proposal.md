# 复杂系统多视角 Atlas

- target: skills/project-atlas
- mode: update
- patch: 20261113-103527-complex-system-views
- risk: medium
- status: proposed

## Intent

让 Atlas 在保留领域三层下钻的基础上，以跨领域主链路、运行时架构、数据状态和横切机制解释复杂系统；提供一份虚构的程序化广告系统示例。非目标：生成目标结构方案、自动推断业务语义或覆盖所有广告产品细节。

## Conflict check

现有 CLI 只接受 `index.md` 与 `domains/` 页面，需同步扩展页面加载、层级、导航与面包屑；`archify`、源码映射和静态构建契约保持兼容。一次性代码问答仍归 `code-explore`，跨项目知识仍归 `wiki-data`。

## Rationale

复杂系统的业务链路横跨领域，单一领域树无法同时承载端到端流程、架构依赖和数据一致性。多视图共享同一套页面元数据、导航和验证机制，可用现有端到端测试与契约测试验证。

## Files

- `skills/project-atlas/SKILL.md`：固定结构、建立顺序与完成门。
- `skills/project-atlas/references/layout.md`：系统视图职责、内容模板与导航契约。
- `skills/project-atlas/references/maintenance.md`：代码变化到系统视图的复核路由。
- `skills/project-atlas/scripts/atlasctl.py`：加载、校验、构建四类系统视图。
- `skills/project-atlas/tests/test_atlasctl.py`：系统视图端到端回归。
- `skills/project-atlas/tests/test_project_atlas_contract.py`：多视角与示例契约。
- `skills/project-atlas/evals/cases.yaml`：复杂系统阅读理解案例。
- `skills/project-atlas/examples/programmatic-advertising.md`：虚构广告系统 Atlas 示例。

## Validation

- 在仓库根运行 `git apply --check --recount`。
- 应用后运行 `git diff --check -- skills/project-atlas`。
- 运行 `python3 -m pytest skills/project-atlas/tests -q`。
- 运行 `make check-names`、`make check-style` 与 `python3 -m pytest skills -q`。
- 核对示例使用虚构通用内容，不含真实公司、项目、主机或凭据。
