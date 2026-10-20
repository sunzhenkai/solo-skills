# task 系列深度复审落地（agent-roster）

taskflow 改为在 `worktrees/{task}` 里实施后，可写委派「工作目录干净」若按主工作树判断，会被用户手上的改动误挡。在门禁句后补一句：工作目录指受派方要写入的目录，在任务 worktree 里实施时只看该 worktree 是否干净。门禁句原样保留（tests/gate_lines.txt 锁定）。
