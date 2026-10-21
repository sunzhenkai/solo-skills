# eval 里的视觉方向读取对象改指 pretty-ui 的 direction.md

- target: skills/taskflow
- mode: update
- patch: 20261021-200926-pretty-ui-direction
- risk: low
- status: proposed

## Intent

pretty-ui 同轮重写（`skills/pretty-ui/patches/20261021-200926-fuse-oil-ui-refactoring-ui/`），删除了 `references/frontend-design/REFERENCE.md`。taskflow 的 eval 里有一条期望写着“实现者先读该文件”，改为读 `pretty-ui/references/direction.md`。

非目标：taskflow 正文与入口门不变。

## Conflict check

只改 `evals/cases.yaml` 中一条 must 的文字，不影响结构检查与其他 case。

## Rationale

保持 eval 描述与仓内实际文件一致，避免评审者照着不存在的路径核对。

## Files

- `skills/taskflow/evals/cases.yaml`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills tests -q`
