# 跟随 pretty-view-html 改名为 pretty-ui

- target: skills/taskflow
- mode: update
- patch: 20261021-195142-pretty-ui-rename
- risk: low
- status: proposed

## Intent

`pretty-view-html` 同轮改名为 `pretty-ui`。把 `evals/cases.yaml` 的 `aesthetic-visual-direction` case 里的参考路径改成新路径。

非目标：case 的判定内容不变。

## Conflict check

none

## Rationale

只改路径字符串，与 taskrail `done.md` 的新链接一致。

## Files

- `skills/taskflow/evals/cases.yaml`：`aesthetic-visual-direction` 的路径

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 -m pytest skills/taskflow/tests tests -q`
