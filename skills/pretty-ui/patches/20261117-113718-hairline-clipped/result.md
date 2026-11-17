# Result

- target: skills/pretty-ui
- mode: update
- patch: 20261117-113718-hairline-clipped
- risk: medium
- status: applied
- applied-at: 2026-11-17T11:47:00+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/pretty-ui/tests -q` → 58 passed；改前基线同为 58 passed
- privacy check: pass（无主机名、绝对路径、私有仓库内容）
- mode check: pass（update，未加 examples/evals/experience）

## Notes

- `SKILL.md` 8188 字节，守在上限 8192 内（改动前 8172，路由补句 +38，压缩同段一句腾位）。
- 量测片段改后在三个 fixture 上复跑：无裁剪 → `环被裁` 空；有裁剪 → 报 `div.pill 被裁左`、`div.card 被裁左右上下`；可滚动容器 → 空（豁免生效）。
- 判环口径：只取非 inset 阴影的第 4 个长度（spread）与 outline 宽+偏移，环境阴影（大 blur、无 spread）天然不计；被裁判定带 0.5px 容差。
- 未做：安装副本 `/home/wii/.agents/skills/pretty-ui` 仍缺 frontmatter `id: pretty-ui`，本地跑该副本的 pytest 仍会 1 failed。按协议未改安装位置；需走 dotfiles 仓 `make skills-lock-update` 下发。
- 未提交，未 push。
