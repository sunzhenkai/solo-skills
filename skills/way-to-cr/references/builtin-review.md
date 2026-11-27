# 内置代码审查（builtin 模式）

零额外依赖的日常首选方案：由当前 agent 直接基于 Git diff 与项目底线文件执行高信噪比代码审查，并在结束后回到主流程第 4 步统一分级与输出。

## 1. 独立视角建议

如果当前会话刚刚写完这批代码，优先建议**新开一个干净会话**或派一个**只读 subagent** 执行本清单，以避开作者盲区；若用户要求就地直接审，则严格以 diff 和源码证据为准，不依赖记忆中的“本来想怎么写”。

## 2. 读取项目底线与上下文

1. 根据主流程第 1 步 `reviewctl preview` 返回的 `guidelines`（如 `AGENTS.md`、`CLAUDE.md`、`.cursorrules`、`CONTRIBUTING.md`），先完整读取其中的代码规范、并发/资源/安全红线与禁止写法，作为本轮最高优先级检查项。
2. 若仓库根目录没有任何底线文件，可在报告结尾附一句轻量建议（例如“可在仓库根目录放一份极简 `AGENTS.md`，写 5–10 条并发、资源释放或安全底线，后续审查会自动对齐”），不要强行代写。

## 3. 纯只读获取 Diff

所有 Git 命令必须带 `--no-pager --no-ext-diff --no-textconv --no-color`，禁止修改工作区：

```bash
# default-branch / range / MR 模式（使用 preview 返回的 merge_base 与 to）
git --no-pager diff --no-ext-diff --no-textconv --no-color <merge_base>..<to> -- "<path>"

# commit 模式
git --no-pager show --no-ext-diff --no-textconv --no-color <commit> -- "<path>"

# uncommitted 模式（tracked）
git --no-pager diff --no-ext-diff --no-textconv --no-color HEAD -- "<path>"

# uncommitted 模式（untracked 新文件）
# 直接读取文件内容
```

大 diff 可配合 `--output=/tmp/way-to-cr-diff.patch` 写到仓库外阅读后删除。对高风险改动文件，按需读取完整函数、调用方与对应测试以确认上下文。

## 4. 七维审查清单

逐个审阅 `reviewable_files`（发现一个问题后继续审完所有文件，不提前停止）：

1. **正确性与边界条件**：空值/零值/越界、状态机漏分支、时区与精度、编码/字符集、幂等性。
2. **并发与资源释放**：锁粒度与死锁、竞态条件、goroutine/线程/连接/文件句柄/定时器泄漏、取消与超时传播。
3. **安全与认证/密钥**：注入（SQL/命令/路径穿越/XSS）、越权与鉴权缺失、硬编码密钥或敏感信息进日志。
4. **数据一致性与接口兼容**：事务边界、部分失败回滚、Schema/API 破坏性变更、向后兼容。
5. **错误处理与失败路径**：吞错、错误类型/错误码丢失、重试风暴、降级策略缺失。
6. **测试覆盖**：核心分支与回归场景是否有对应测试，断言是否真实有效（非空壳测试）。
7. **项目底线遵循**：是否违反 `AGENTS.md` / `CLAUDE.md` 中声明的团队/个人底线。

## 5. 高信噪比过滤与输出组装

- **每条 finding 必须满足**：真实存在于本次改动范围内、给出具体文件与行号（`start_line` / `end_line`）、说明具体触发条件与失效后果，并在有明确改法时给出最小修复建议。
- **直接丢弃**：纯个人偏好/排版吹毛求疵、未改动到的历史代码问题、没有代码证据支撑的猜测。
- 组装为统一 result JSON 写入 `/tmp/way-to-cr-result.json`：

```json
{
  "engine": "builtin",
  "status": "complete",
  "session_id": "builtin-<YYYYMMDD-HHMMSS>",
  "llm": {"provider": "session", "model": "current-session"},
  "message": "builtin review: <n> finding(s) across <m> file(s)",
  "summary": {"files_reviewed": 0, "comments": 0},
  "comments": [
    {
      "path": "src/example.py",
      "start_line": 10,
      "end_line": 15,
      "priority": "P1",
      "category": "bug",
      "content": "问题描述与触发条件",
      "existing_code": "原代码片段",
      "suggestion_code": "建议改法"
    }
  ],
  "warnings": []
}
```

## 6. 回到主流程

返回 `SKILL.md` 第 4 步：执行分级排序、对话总结、可选落盘（`reviewctl write`）与 MR/PR 评论确认门。
