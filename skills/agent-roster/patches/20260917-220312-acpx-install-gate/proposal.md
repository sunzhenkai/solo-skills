# acpx 安装作为委派默认选项，拒绝则提示受限

- target: skills/agent-roster
- mode: update
- patch: 20260917-220312-acpx-install-gate
- risk: medium
- status: proposed

## Intent

改变编排者在 `acpx` 缺失时的行为：准备委派时默认提议安装，必须先向使用者确认；拒绝安装则先明确提示委派功能受限，才允许走直连 ACP 降级。禁止静默安装，禁止把降级说成与默认执行器对等。

非目标：不实现新的降级客户端；不改探测脚本；不把安装命令写死到除契约以外的地方。

## Conflict check

与「本 skill 不绑定具体执行器」不冲突：默认实现仍是 `acpx`，换执行器仍只改契约文件。与 L2 探测不冲突：探测继续直连适配器，不依赖 `acpx`。门禁只在准备委派时触发。

## Rationale

委派是闭环核心动作。直连 ACP 只能覆盖一次性往返，会话、排队、崩溃重连、权限档位与结构化事件都没有现成实现。先前把降级写成可随时走的对等路径，会让编排者在未告知使用者的情况下把核心动作放到半成品腿上。安装需确认，是因为往使用者机器写全局 CLI 属于副作用，不能静默执行。

## Files

- `skills/agent-roster/SKILL.md`：委派步骤加上安装门禁；不变量补一条。
- `skills/agent-roster/references/delegation-contract.md`：默认实现补确认安装；降级段改为「仍可走通 / 功能受限」。

## Validation

- `git apply --check --recount` 通过。
- 应用后：`SKILL.md` 委派段含确认安装与拒绝后提示；契约降级段含「功能受限」清单；frontmatter `name` 仍为 `agent-roster`。
