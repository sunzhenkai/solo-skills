# 统一 project-explore 测试文件名

- target: skills/project-explore
- mode: update
- patch: 20261113-215500-project-explore-test-names
- risk: low
- status: proposed

## Intent

将两个测试文件从 test_code_explore_*.py 改名为 test_project_explore_*.py，清除活跃配套中的旧 skill 命名；测试内容不变。

## Conflict check

仅文件改名，pytest/unittest 发现规则保持不变。历史 patches 不改写。

## Rationale

目录、frontmatter、eval 与测试文件名统一后，活跃内容不再暴露旧名称。

## Files

- skills/project-explore/tests/test_code_explore_contract.py → test_project_explore_contract.py。
- skills/project-explore/tests/test_code_explore_gate_lock.py → test_project_explore_gate_lock.py。

## Validation

- 在临时 Git 仓机械生成 rename diff，git apply --check --recount。
- 应用后运行 git diff --check 和 project-explore 测试。
