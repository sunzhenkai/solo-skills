# eval — 20260924-run-status

- 回归：controlled-delegation 轮的规则全部保留（timeout 必填 / PID 监控 / 禁 pgrep -f / 完成判定看产物），仅在第 2 条后插入脚本条目、第 5 条补「脚本判为 truncated」一句；evals/cases.yaml 各判例不涉及被改小节，无影响。冒烟门禁与已知口径未动。
- 模式：脚本对 6 态逐一验证——真实 done 案例（同会话成功的 19983 事件委派，final_text 12390B）判 done；真实复用目录暴露 bug 后修正（id=2 存在权限请求中间响应，result_for 改取末个响应）；合成 stuck（3 事件冻结）/ truncated（有流无终态、含同 id 中间响应）/ cancelled / timed-out 全部判对。上轮的失败模式（3 事件冻结被当运行中、半成品被当成功）在新工具下分别输出 stuck / truncated 并给出处置指引。
- 契约：脚本是纯 stdlib 确定性实现，无自然语言解析；对 evals/cases.yaml 的判例（decision-before-execution 等）零影响。无自动 runner，按指令级对照 + 真实样本实测，未编造分数。
- 副作用：委派启动多写一个 status.json（新增约定，不扩权限）；状态判定收敛到脚本，收窄人肉误判面；不触碰触发条件、权限档位、安装门禁与降级规则；无密钥/内部 URL/项目名。
- 结论：pass
