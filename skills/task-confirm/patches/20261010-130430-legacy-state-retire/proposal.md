# Proposal：遗留状态机迁入 legacy（Wave 3）

## Intent

D5：state-machine / state-file 迁入 `references/legacy/`；live 正文标明勿作进度真源；脚本与测试改路径。

## Mode / Risk

`update` / `low`–`medium`

## Validation

`python3 -m pytest skills/task-confirm/tests -q`
