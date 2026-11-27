# Open Code Review 细则（ocr 模式）

本文件承接 `ocr`（`@alibaba-group/open-code-review`）引擎的前置校验、参数映射、模型记忆与失败分流，执行后回到主流程第 4 步。

## 1. 前置检查

```bash
which ocr && ocr --version || echo "NOT INSTALLED"
ocr llm test
```

- 未安装：按上游文档征得用户同意后安装，或改选 `builtin` / `claude` / `codex`。
- 运行中 `--format` 报 `unknown flag`：说明 CLI 低于 v1.9.0，提示升级 `npm i -g @alibaba-group/open-code-review`。
- `ocr llm test` 只验证**默认配置**。单次覆盖 provider/model 时先用 `ocr llm providers` 核对名称，凭据须已配好（报错即停请用户配置，禁止编造 API key）。
- `ocr llm test` 失败时停下，让用户在以下路径中选择：
  1. 配置 LLM 后重跑；
  2. 走 [references/delegate-mode.md](delegate-mode.md)（OCR delegate 模式：复用当前 agent 订阅额度，无需额外 API key）；
  3. 切换为 `builtin` / `claude` / `codex` 引擎。

## 2. 模型选择与记忆复用

- 通过 `ocr llm providers` 与 `reviewctl probe --engine ocr` 获取可用 provider 与已保存的 `provider`/`model`。
- 用户选定后执行 `reviewctl prefs set --engine ocr --provider <provider> --model <model>` 记住；下次自动复用，直到用户指定新 `provider=`/`model=` 或说「换模型」。

## 3. 预览与执行命令

1. 预览文件列表确认：`ocr review --preview`（追加下方范围 flag）。
2. 正式执行：

```bash
ocr review --audience agent --format json --repo <git_root_abs> -o /tmp/ocr.json 2>/tmp/ocr.err
```

范围 flag 按 mode 追加：

| mode | 追加范围 flag |
|---|---|
| `uncommitted` | （无，默认工作区） |
| `commit` | `-c <hash>` |
| `default-branch` / MR / PR | `--from <from> --to <to>` |

常用可选参数：
- LLM 覆盖：`--provider <name> --model <name>`（单次覆盖，不写回 `ocr config`）
- 背景信息：`-b <一句话>` / `-B <md路径>`
- 深度与范围控制：`--effort low|medium|high`、`--exclude '**/generated/*,**/testdata/*'`、`--max-tokens-budget <n>`
- 中断续跑：`--resume <session-id>`（`ocr session list` 可查）
- 离线 HTML 回放：`ocr session export <session-id>`（含源码摘录，按仓库同等保密）

## 4. 结果规范化

先检查 exit code 与 `/tmp/ocr.err`；JSON 中 `status=skipped` 视为无审查对象，不是失败。确保结果 JSON 包含 `"engine": "ocr"` 并保存到 `/tmp/way-to-cr-result.json`（`reviewctl write` 会从 `llm.{provider,model}` 读取真实后端），随后回到 `SKILL.md` 第 4 步分级、输出总结与可选落盘。
