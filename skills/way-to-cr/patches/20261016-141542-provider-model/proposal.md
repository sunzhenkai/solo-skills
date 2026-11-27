# solo-code-review 支持指定 provider + model（单次覆盖）

- target: skills/solo-code-review
- mode: update
- patch: 20261016-141542-provider-model
- risk: medium
- status: proposed

## Intent

用户要求：支持指定模型+供应商，未指定则使用现有配置；「指定 agent」经确认即 OCR 的 provider（LLM 后端），统一走 `ocr review --provider/--model` 透传，不引入 agent-roster 委派。

1. **调用签名**：新增可选参数 `provider=<name>`、`model=<name>`。
2. **前置**：说明 `ocr llm test` 只验证默认配置（无 --provider/--model 参数）；指定组合用 `ocr llm providers` 核对名称，凭据须已在 `ocr config` 或环境变量中配好（单次覆盖不传凭据），跑 review 报错即停下请用户配置，禁止编造 API key。
3. **跑 ocr**：用户指定时追加 `--provider <name> --model <name>`；未指定不加 flag，沿用现有配置。
4. **落盘**：`reviewctl write` 从 ocr JSON 的 `llm.{provider,model}`（v1.12.9 实测存在）读出实际后端，渲染进 review.md 的 Meta 段「- LLM：`provider` / `model`」；delegate 模式 JSON 无该字段则不渲染。
5. **delegate 澄清**：references/delegate-mode.md 加一句——delegate 模式 `--provider/--model` 不适用（审查用当前 agent 的模型）。
6. **体量**：MR/PR 步骤细则下沉到新增 references/mr-mode.md（SKILL.md 保留一句门禁要点+指针），守 8KB 指导线。
7. **配套**：tests/test_reviewctl.py 增 llm 渲染用例（含 delegate JSON 不渲染断言）；tests/test_skill_contract.py 增 provider/model 契约断言、fetch-only 断言改锚 mr-mode.md；evals/cases.yaml 增 provider-model-override case。

非目标：不做跨 agent 委派编排；不持久化 provider/model（不改用户的 ocr config）。

## Conflict check

- 与主流程无冲突：范围确认门、fetch-only、评论确认门、产物布局全部不动；MR/PR 细则只是位置下沉。
- 与 delegate 轮无冲突：delegate 模式本来就无 OCR 侧 LLM，本轮明确 provider/model 在该模式不适用。
- check-style 引用链规则：SKILL.md 直链 mr-mode.md / delegate-mode.md，两个 references 之间不互链，仍是一层。

## Rationale

- `--provider/--model` 为 v1.12.9 实测存在的单次覆盖 flag（`ocr review --help`：「Select a configured provider and model for this run only」）。
- `ocr llm test` 无这两个参数为本机实测；内置 provider 清单可用 `ocr llm providers` 查询（实测 26 个）。
- ocr JSON 顶层 `llm` 字段实测存在：{"provider": "minimax", "model": "MiniMax-M3"}（/tmp/ocr-verify.json，本机真实运行产物）。
- 凭据不入命令行：沿用本 skill 既有 GITLAB_TOKEN 纪律，与「禁止编造 API key」一致。

## Files

- skills/solo-code-review/SKILL.md — 调用签名、前置、跑 ocr、落盘说明；MR/PR 段收成指针
- skills/solo-code-review/references/mr-mode.md — 新增，MR/PR 步骤细则（原文下沉+provider 透传一句）
- skills/solo-code-review/references/delegate-mode.md — 加 provider/model 不适用说明
- skills/solo-code-review/scripts/reviewctl.py — render_full 渲染 llm.{provider,model}
- skills/solo-code-review/tests/test_reviewctl.py — 增 llm 渲染/不渲染用例
- skills/solo-code-review/tests/test_skill_contract.py — 增 provider/model 断言，fetch-only 改锚 MR
- skills/solo-code-review/evals/cases.yaml — 追加 provider-model-override

## Validation

- 应用前：git apply --check --recount 通过；b 树 pytest 37 passed；SKILL.md 8184 B ≤ 8192；禁令词 5 处（0.6/KB）
- 应用后：pytest skills/solo-code-review/tests 全绿；python3 -m pytest skills -q 全仓通过；make check-style / check-names 无告警
