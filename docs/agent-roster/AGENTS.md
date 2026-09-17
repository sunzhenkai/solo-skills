# AGENTS.md

本仓库的工作约定。

## 仓库定位

本仓库是公开的，**只放机制，不放数据**。名册、案例、路由规则、运行痕迹全部存放在使用者的私有位置，由 `~/.config/agent-roster/config.yaml` 指出。

写任何文件前先自查：这行内容里有没有主机名、内网地址、项目名、真实任务描述？有就不属于这里。

## 结构

- `skills/agent-roster/`：能力正文，公开分发的部分。
- `skills/agent-roster/references/`：格式与契约文档，被 `SKILL.md` 按需引用。
- `skills/agent-roster/scripts/`：只依赖 Python 3 标准库，不引入第三方依赖。
- `skills/agent-roster/experience/patterns/`：脱敏后的通用规律。具体案例不进这里。
- `docs/adr/`：关键决策。`CONTEXT.md`：术语表，只放术语，不放实现细节。

## 运行时只读

skill 安装到各 agent 目录是**字节复制**而非软链，运行时往 skill 目录写东西只会写进镜像，并在下次同步时被覆盖。所以：

- 运行时产生的一切（案例、台账、探测状态）落在仓库之外。
- `experience/patterns/` 的修改只能在源仓库做，然后重新同步。

## 修改能力正文

改 `SKILL.md` 走 `$skill-upgrader`，走 `patches/` 审计，不要直接编辑绕过。

## 语言

面向使用者的文档用简体中文。命令名、路径、代码、状态值与既成术语（ACP、Endpoint、Delegation 等）保持原文。
