# 台账并发写入

多会话 / 多 agent 写同一 workspace 时读。

1. TASK 状态、done 门与 INDEX 更新只用 `scripts/task_state.py`；脚本持 workspace 锁并原子替换，INDEX 随时可重建。
2. 父 TASK 和协调 checkbox 只由父编排者写；子 TASK 只由对应子任务编排者写；worker 返回结论与证据，不并发改父文件。
3. decisions / history 追加前重读最大编号和文件尾部；发现他人新内容先合并，不覆盖。相互矛盾的认知写带日期的更正与 superseded 关系。
4. 同任务同仓代码写操作串行；不同子任务或仓库才可并行。git worktree 准备使用 prepare_worktree.py 的注册表和锁。
5. 发现部分写入、路径冲突或身份不明时先 reconcile；不删除、不 reset、不用旧快照覆盖新文件。
