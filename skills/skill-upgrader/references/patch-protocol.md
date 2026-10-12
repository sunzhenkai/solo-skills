# Patch Protocol

本协议定义 `skill-upgrader` 生成的更新记录。所有 diff 路径相对**包含目标 Skill 的 Git 仓库根**；记录目录落在目标 Skill 内。

## 目录

```text
<skill-dir>/patches/<YYYYMMDD-HHMMSS>-<slug>/
├── proposal.md
├── change.patch
└── result.md
```

`<skill-dir>` 是含有待改 `SKILL.md` 的目录（任意仓库中的任意 Skill）。

## proposal.md

```markdown
# <简短标题>

- target: <skill-dir>
- mode: update | self-upgrade
- patch: <YYYYMMDD-HHMMSS>-<slug>
- risk: low | medium | high
- status: proposed

## Intent

<要改变的模型行为、触发场景和非目标；须与 mode 一致>

## Conflict check

<与现有内容及其他 Skill 职责的冲突；没有则写 none>

## Rationale

<为什么该更新合理且可验证>

## Files

- <将修改的、相对仓库根的路径及原因>

## Validation

- <应用前检查>
- <应用后测试或确定性检查>
```

`status` 在 proposal 中保持 `proposed`，最终状态写入 `result.md`，不要回写历史提案。

## change.patch

使用 Git 可接受的 unified diff。示例：

```diff
diff --git a/skills/example/SKILL.md b/skills/example/SKILL.md
index 1111111..2222222 100644
--- a/skills/example/SKILL.md
+++ b/skills/example/SKILL.md
@@ -10,3 +10,4 @@
 Existing instruction.
+New general instruction.
```

要求：

1. 在包含目标 Skill 的仓库根可被 `git apply --check --recount` 校验。
2. `a/`、`b/` 后使用相对该仓库根的完整路径，且前缀为该 `<skill-dir>/`。
3. 只修改同一目标 Skill 的生产内容（含 `self-upgrade` 新增的 examples/evals/experience）。
4. 不包含 `patches/` 历史记录、agent 镜像目录、绝对路径或临时文件。
5. 不依赖已应用但未记录的手工编辑。
6. 找不到 Git 仓库根时不得伪造 apply；停止并交由用户处理。

## result.md

```markdown
# Result

- target: <skill-dir>
- mode: update | self-upgrade
- patch: <YYYYMMDD-HHMMSS>-<slug>
- risk: low | medium | high
- status: applied | failed
- applied-at: <ISO 8601 timestamp or n/a>

## Validation

- `git apply --check --recount`: pass | fail
- `git diff --check`: pass | fail | not-run
- target tests: <命令与结果，或 not-available>
- privacy check: pass | fail
- mode check: pass | fail

## Notes

<实际结果、失败原因或与 proposal 的偏差；没有则写 none>
```

## 状态规则

- `proposed`：patch 已生成，尚未应用或正在等待确认。
- `applied`：patch 已成功应用且验证通过。
- `failed`：应用或验证失败；停止继续修改生产内容。

已生成的 patch 目录是审计记录。若 proposed patch 尚未应用，可以在同一目录修正 `change.patch`；一旦应用尝试已经发生，不再改写该目录，后续修复创建新 patch。

## 目录规则（原 SKILL.md「Patch 目录协议」）

每轮在**目标 Skill 目录**下创建新目录（不是本 skill 自己的目录，除非目标就是本 skill）：

目录结构见上「目录」。

- `<slug>`：小写英文、数字和连字符，概括单一改动目的。
- 目录必须全新；不得覆盖、改写或删除历史 patch 目录。
- `<skill-dir>/patches/` 不存在（如历史已按仓库维护决定清理，改由 Git 追溯）时按需创建（`mkdir -p`），不得因缺目录中止。
- `change.patch` 为 unified diff；路径相对**包含该 Skill 的 Git 仓库根**，且只触及该 `<skill-dir>/` 下生产内容。
- patch 可增删改 `SKILL.md`、`references/`、`scripts/`、`assets/`、测试及 `self-upgrade` 所需的 `examples/` `evals/` `experience/`，但**不得**修改任何已有 `patches/` 历史记录。

定位仓库根：从 `<skill-dir>` 向上找 Git 根。找不到 Git 根则停止并说明无法安全 `git apply`，不要改用直接写文件绕过。

生产稿定位：以含 `SKILL.md` 的目录为准。不要改用户主目录或其它工具同步生成的安装副本，除非用户明确要求改安装位置。

---
