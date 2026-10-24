# explore：建立可复用代码事实

## 目的
查清改点、调用链、依赖、约束和影响面，为后续路由提供证据。

## 进入条件
实现入口或现状不清、跨项目关系未知、旧证据失效，或 resume 发现事实冲突。

## 跳过条件
当前相关 commit 下已有覆盖本任务范围的事实与出处；明确小改只读目标处即可。

## 所需输入
目标、criterion、涉及仓库和已有 context/sources。

## 执行方法
1. 先读用户原话、workspace / 项目说明、目标模块与既有测试，再扩大到直接依赖；不全仓扫描。
2. 只读探索。面广可并行只读 worker，限定主题和范围。
3. 结论标 confirmed / assumed，记录 source_repo、commit、文件:行或命令；原始输出落证据文件。
4. 复用未失效结果，不因跨会话重读。

## 产出
`context/current.md` 的有效事实摘要、`context/sources.md` 的证据索引；决定写 decisions.md。

## 完成门
当前要决定的入口、直接依赖、约束和未知均有证据或显式假设，足以选择下一 reference。

## 退出与重入
原因不明转 diagnose，关键取舍转 grill，契约变化转 design，多交付转 decompose，否则 plan / execute。相关 commit 或范围改变才重入受影响部分。
