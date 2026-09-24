# Role 默认 Endpoint

一个文件：`<data_root>/agents/roles.yaml`。对照表里是具体 Endpoint，和名册一样放在私有数据里，不进本仓库。

只认下面这种行，不认任意 YAML。`#` 开头是注释。右侧空着表示这个 Role 还没配。

```text
<role-id>: <host>/<kind>
```

`<role-id>` 小写字母开头，其余为小写字母、数字或连字符。一行一个，行尾不写注释。

约定 id 的含义见仓库根 `CONTEXT.md`。名字可以另加。调用方不点名，这些 id 就不参与这次选人：

- `developer`
- `planner`
- `reviewer`
- `code-reviewer`
- `designer`

`scripts/resolve_role.py <role-id>` 的判定：

- 右侧有 Endpoint，`<data_root>/agents/<host>/<kind>.md` 存在，且该画像「探测状态」最后一条不含 `❌` 或 `⚠` → `verdict: use`（exit 0）
- 没配、没有这个 id、或文件不存在 → `verdict: ask`，`reason: unbound`（exit 1）
- Endpoint 写了，但名册里没有这份画像 → `verdict: ask`，`reason: missing`（exit 1）
- 画像在，但探测状态最后一条含 `❌` 或 `⚠` → `verdict: ask`，`reason: down`（exit 1）

exit 1 是「要问人」，不是脚本故障。exit 2 才是对照表或参数坏了。

`--write <role-id> <host>/<kind>` 改这个文件里的一行。只接受名册里已有画像的 Endpoint。何时允许调用，见 `SKILL.md` 的「角色」一节。
