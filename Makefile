# 外部 skill 依赖一键安装。
#
# 本仓六个 skill 依赖的仓外 skill（梳理见 README「外部依赖」）：
#   - openspec-explore / openspec-propose / openspec-apply-change / openspec-archive-change
#       由 @fission-ai/openspec CLI 生成，不发布为独立 skill 包
#   - grilling / grill-with-docs / domain-modeling   来自 mattpocock/skills
#   - agent-roster                                    来自 sunzhenkai/agent-roster（执行依赖 acpx 二进制）
#   - skill-upgrader / commit-push                    来自 sunzhenkai/dotfiles
#
# 若你已用 dotfiles 编目（`dotf agents -c`），无需本 Makefile——它已覆盖上述全部来源。
# 本 Makefile 是给不在 dotf 环境里的用户的独立安装路径，目标目录同为 ~/.agents/skills。

SKILLS_DIR ?= $(HOME)/.agents/skills

MATT_SKILLS   := grilling grill-with-docs domain-modeling
DOTFILES_SKILLS := skill-upgrader commit-push
OPENSPEC_SKILLS := openspec-explore openspec-propose openspec-apply-change openspec-archive-change

# taskflow / task-wizard / delivery-loop / task-explore / agent-roster-flow 依赖的全部外部 skill
EXTERNAL := $(MATT_SKILLS) $(OPENSPEC_SKILLS) agent-roster $(DOTFILES_SKILLS)

.PHONY: help install-deps install-matt install-openspec install-agent-roster install-dotfiles install-acpx check-deps

help:
	@echo "make install-deps      安装全部外部 skill 依赖（openspec-* + grilling 系列 + agent-roster + skill-upgrader/commit-push）"
	@echo "make install-matt      只装 grilling / grill-with-docs / domain-modeling"
	@echo "make install-openspec  只生成并安装 openspec-* 四件套（经 npx @fission-ai/openspec）"
	@echo "make install-agent-roster  只装 agent-roster"
	@echo "make install-dotfiles  只装 skill-upgrader / commit-push"
	@echo "make install-acpx      agent-roster 的执行依赖 acpx：检测缺失并给出安装入口"
	@echo "make check-deps        检查外部依赖是否就绪（缺项非零退出）"

install-deps: install-matt install-openspec install-agent-roster install-dotfiles
	@$(MAKE) --no-print-directory check-deps

install-matt:
	@mkdir -p $(SKILLS_DIR)
	npx -y skills add mattpocock/skills -g -y $(addprefix -s ,$(MATT_SKILLS))

install-openspec:
	@mkdir -p $(SKILLS_DIR)
	@tmp=$$(mktemp -d); \
	npx -y @fission-ai/openspec@latest init --tools agents --no-animation "$$tmp/project" >/dev/null || { rm -rf "$$tmp"; exit 1; }; \
	found=0; \
	for d in "$$tmp"/project/.agents/skills/openspec-*; do \
		[ -d "$$d" ] || continue; \
		rm -rf "$(SKILLS_DIR)/$$(basename "$$d")"; \
		cp -R "$$d" "$(SKILLS_DIR)/"; \
		found=$$((found+1)); \
	done; \
	rm -rf "$$tmp"; \
	if [ $$found -eq 0 ]; then echo "openspec init 未生成 openspec-* skill，检查 npx/网络" >&2; exit 1; fi; \
	echo "openspec-*（$$found 个）→ $(SKILLS_DIR)"

install-agent-roster:
	@mkdir -p $(SKILLS_DIR)
	npx -y skills add sunzhenkai/agent-roster -g -y -s agent-roster
	@command -v acpx >/dev/null || echo "提示：agent-roster 的委派执行依赖 acpx（https://acpx.sh），缺失时委派会停住；可跑 make install-acpx"

install-dotfiles:
	@mkdir -p $(SKILLS_DIR)
	npx -y skills add sunzhenkai/dotfiles -g -y $(addprefix -s ,$(DOTFILES_SKILLS))

install-acpx:
	@command -v acpx >/dev/null && echo "acpx 已安装：$$(command -v acpx)" || \
	echo "未自动安装 acpx。它是 agent-roster 的运行时二进制（不在 skills 包里），请按 https://acpx.sh 的安装方式手动安装。"

check-deps:
	@miss=0; \
	for s in $(EXTERNAL); do \
		if [ -f "$(SKILLS_DIR)/$$s/SKILL.md" ]; then echo "ok    $$s"; \
		else echo "MISS  $$s"; miss=1; fi; \
	done; \
	if command -v acpx >/dev/null; then echo "ok    acpx"; \
	else echo "WARN  acpx 未安装（仅 agent-roster 委派执行需要，见 make install-acpx）"; fi; \
	exit $$miss
