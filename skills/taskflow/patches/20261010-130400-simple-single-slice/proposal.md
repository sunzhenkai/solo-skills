# Proposal：simple 单切片约定（Wave 2）

## Intent

D1 配套：上游 `tier: simple` 时 taskflow 实施段默认单切片，进度仍只认 checkbox。

## Mode / Risk

`update` / `low`

## Validation

`python3 -m pytest skills/taskflow/tests -q`
