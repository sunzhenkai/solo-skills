# task 系列深度复审落地（task-intent）

- 「何时跳过」拿 `skip` 档当条件，但档位在 wizard 第 4 步才定：改成开头「先定做多少」，按原话是否一句话说清改动来判断，并合并原第 9 行「小改直接进入下一步」的矛盾说法。
- 「不可跳过」改成正向的「守住这几条」。
- human 纠偏写明停下等用户说对；由 wizard 调用时复述和 plan 要点合成一条消息。
- goal 代审改指针到 taskrail confirm-protocol「另一个模型审」，派不出的处理只在那里。
- intent.md：goal 意图涉及线上 / 不可逆时照常确认、动作执行前再停；多轮不收敛按 user-report「卡住」停；修正 user-report 相对链接（原 `../taskrail` 少一层）。
- evals：清晰小改、goal 派审、不可逆动作三条按新规则改写；契约测试同步。
