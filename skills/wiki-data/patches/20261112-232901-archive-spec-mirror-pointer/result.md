# 结果

- 改动：`skills/wiki-data/SKILL.md` 非目标一句，spec 镜像的边界从「交给 `project-spec-mirror`」改为指向 `archive/skills/`。
- 同轮相关改动（不在本 patch 内）：`project-spec-mirror` 整个目录 `git mv` 到 `archive/skills/project-spec-mirror/`；根 `README.md` 删表行、说明段补归档约定；新增 `archive/README.md`。

## 验证

- `python3 -m pytest skills -q` — 511 passed, 3 skipped（归档目录不再收集其 60 余项契约测试）。
- `make check-style` — 0 告警。
- `make check-names` — 无 denylist 命中（10 个词；扫描范围 `skills docs tests scripts README.md AGENTS.md Makefile`，不含 `archive/`）。
- `skills/wiki-data/tests` 里的 `assertIn("project-spec-mirror", self.skill)` 未改仍通过，因为句子里保留了 id。

## 遗留

- `archive/` 不在 `check_no_project_names.py` 与 `check_output_style.py` 的扫描范围；归档内容保持归档前的状态，后续若要改归档 skill 正文，泄漏扫描需手动带路径跑：`python3 scripts/check_no_project_names.py archive`。
