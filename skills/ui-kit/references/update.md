# 升级模板

项目锁定的风格包与版本在 `ui-template.lock.json`。升级 = 把模板仓 checkout 到目标 tag，再用它的安装脚本对项目执行升级。

## 1. 先看状态

```bash
python3 <kit>/skills/ui-template-apply/scripts/install_registry.py --project . --status
```

| 状态 | 含义 | 升级时 |
| --- | --- | --- |
| `upstream` | 项目没改，模板改了 | 覆盖 |
| `local` | 项目改了，模板没改 | 保留 |
| `merge` | `theme.css` 两边都改了 | 自动三方合并 |
| `conflict` | 模板文件两边都改了 | 不动，手工合并 |
| `new` | 新版本新增的文件 | 写入 |

## 2. 升级

```bash
python3 <kit>/skills/ui-template-apply/scripts/install_registry.py --project . --upgrade
npm install   # 对照脚本打印的依赖补齐 package.json
```

- 主题三方合并：项目改过的白名单 token 保留项目值；项目没改过的取新包值；项目改过的非白名单 token 被丢弃并打印 `DROPPED`。仍要保留就改回去并记入 `theme_deviations`。
- `CONFLICT`：手工合并后执行 `install_registry.py --project . --resolve <文件>`，再记入 `local_edits`。该文件退出保真保证，考虑回馈模板仓。

## 3. 收尾

按 verify.md 跑完整验收；在 DESIGN.md「验收记录」写新版本号和结果。
