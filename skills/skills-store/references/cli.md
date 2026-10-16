# npx skills 命令速查

参数以 `npx skills --help`（及 `npx skills <command> --help`）为准；本页只记环境里查不到的约定与坑。

## 环境查不到的坑

- **作用域写法不对称**：`add` / `remove` 用 `-g` 表示全局、不加即项目；`update` 必须显式带 `-p`（项目）或 `-g`（全局），裸 `npx skills update` 会进入交互询问。
- **`--all`** 等价 `--skill '*' --agent '*' -y`：批量且免确认，按 SKILL.md 对每个 skill 子目录分别审计。
- **`use`** 只读生成 prompt、不写 skills 目录；用户随后要安装时照常走审计。
- **`--list` / `-l`** 只列仓库内 skill 不安装，适合在审计前定位子目录。
- 非交互环境（CI / 明确指令）加 `-y`，避免卡在确认提示。
- `<source>` 可为 `owner/repo`、GitHub/GitLab URL、git URL、本地路径或仓库内某 skill 的 tree URL。

## 常用命令

```bash
npx skills find <keyword> [--owner <github-owner>]
npx skills add <owner/repo> --list                      # 只列不装

npx skills add <source> -s <skill-name> -y              # 项目
npx skills add <source> -s <skill-name> -g -a cursor -y # 全局 + 指定 agent

npx skills list            # 项目；全局用 ls -g；--json 机读
npx skills remove <skill-name> [-g] [-a <agent>] -y
npx skills update [<skill-name>] -p -y                  # 项目
npx skills update [<skill-name>] -g -y                  # 全局
npx skills use <owner/repo>@<skill-name>
```

常用 `--agent` 名：`cursor`、`codex`、`opencode`、`kiro-cli`、`pi`、`zcode`；完整列表见 `--help` 或上游 README。

## 用户说法 → 动作

| 用户意图 | 动作 |
|----------|------|
| 「搜 typescript 相关 skill」 | `npx skills find typescript` |
| 「装到当前项目」 | 临时克隆 → 审计 → `npx skills add <src> -s <name> -y` |
| 「全局安装给 cursor」 | 临时克隆 → 审计 → `npx skills add <src> -s <name> -g -a cursor -y` |
| 「删掉全局的 xxx」 | `npx skills remove xxx -g -y` |
| 「更新当前目录的 skills」 | 对新版本审计 → `npx skills update -p -y` |
