# Result：Web UI 实现前经 ui-kit 分派

## Outcome
Web UI 交付先由 ui-kit 选择通用或模板主路线。通用路线保留 Active Instance 与 pretty-ui two-pass；模板路线以 lock 和像素保真证明体系一致，交接可写 `无（ui-template）`。运行态和独立 design 评审门不变。

## Verification
- 路由与链接契约包含非 React、ui-template lock、像素保真和新交接值。
- 全仓：620 passed, 3 skipped, 2 subtests passed；跨 skill 链接解析通过。
