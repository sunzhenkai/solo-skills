# wiki-data：spec 镜像指针改指归档位置

- target: `skills/wiki-data`
- 触发：`project-spec-mirror` 下线并移入 `archive/skills/project-spec-mirror/`（2026-11-12）
- 改动：`SKILL.md` 非目标里的边界句仍点名 `project-spec-mirror`，但该 skill 已不在 `skills/` 下、也不再随安装下发；改为指向归档位置，读者不至于去找一个装不上的 skill。

## 验收

- `grep -rn "project-spec-mirror" skills/` 的命中都带归档说明，无「交给 project-spec-mirror」式失效指引。
- `python3 -m pytest skills/wiki-data/tests -q` 通过（契约测试断言仍含该 id 字符串）。
- `make check-style`、`make check-names` 通过。

## 不做

- 不改 wiki-data 的职责边界本身，也不恢复 spec 镜像能力。
- 不动已归档 skill 的内容与其历史 patch。
