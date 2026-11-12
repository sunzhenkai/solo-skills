# archive

已从 `skills/` 下线、不再安装的 skill。生产内容与历史 `patches/` / `evolutions/` 原样保留在 `archive/skills/<id>/`，便于查阅与恢复。

这里不进 `npx skills` / `npx skills add` 的发现路径，也不跑测试与风格检查。

## 恢复

1. `git mv archive/skills/<id> skills/<id>`
2. 在根 `README.md` 的 skill 表补回该行
3. 从本文件条目表删掉该行
4. 跑 `python3 -m pytest skills/<id>/tests -q`、`make check-style`、`make check-names`

## 条目

| 名称 | 下线原因 |
|------|----------|
| `project-spec-mirror` | 按用户要求下线归档（2026-11-12）；spec 镜像场景暂由 `wiki-data` 与 OpenSpec 流程承接 |
