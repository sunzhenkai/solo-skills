# 点名的 Role 直接用它的默认 Endpoint，这不是打分

使用者可以给一个 Role 指定默认 Endpoint。派活时点了这个 Role、又没写 Endpoint，就用那个默认，不再走 Trace 和 Routing Rule。Role 和 Endpoint 都没点时，选人仍按 [ADR 0002](./0002-no-scoring-only-cases.md)：读案例和成文规则，由人判断，不打分。

这样拆是因为两件事不是一种。Role 是使用者事先点的名，和当场写明 Endpoint 同一级。ADR 0002 否掉的是把活切成格子、再按格子给 Endpoint 打分排序。五个约定名字只是词汇，调用方不点名，系统就不把这次活归进任何一格。

点了 Role 但没有能用的默认 Endpoint（没配、不在名册、起不来）时停下来问这次用哪个，不改去查 Trace 或 Routing Rule。这次按回答派活，再问要不要把该 Endpoint 记成这个 Role 的默认。使用者明确同意才写入。只指定这次用谁，不改默认。

## Considered Options

- **有案例证据时路由优先**：否掉。默认 Endpoint 是使用者已经做过的选择，不该被旧案例盖掉。
- **解析出来仍等人在菜单里再点一次**：否掉。没写 Endpoint 时就要用上这个默认。
- **从任务正文推断该用哪个 Role**：否掉。那就是 ADR 0002 拒绝的格子。
- **这次答了谁就把谁写成默认**：否掉。临时替手和长期默认不是一句话。没听到明确同意，不改对照表。

## Consequences

Role 到 Endpoint 的对照含有具体 Endpoint，按 [ADR 0001](./0001-ledger-lives-outside-this-repo.md) 放在使用者的私有数据里。公开词汇表只记 Role 是什么、五个约定名字各指哪类活。

没点 Role 时，这条决策不改变现有选人方式。
