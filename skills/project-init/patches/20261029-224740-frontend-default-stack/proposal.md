# 更新 frontend 默认七层栈

- target: skills/project-init
- mode: update
- patch: 20261029-224740-frontend-default-stack
- risk: medium
- status: proposed

## Intent

把 `frontend` 默认栈改为用户确认的七层约定：

1. React + TypeScript + Vite
2. Tailwind CSS + CSS Variables / Design Tokens
3. shadcn/ui + Radix UI
4. Lucide React；Motion 按需
5. TanStack Query + Zod
6. 项目级 `DESIGN.md` + 组件与页面模式
7. Storybook + Playwright + 视觉回归（`toHaveScreenshot`）

同步降级：Zustand / Vitest 改为「需要再用」；OpenAPI codegen 改为「有 spec 再用」。Next.js 路径与表单例外保持。非目标：不改 python-api；不引入 Chromatic；不做 pretty-ui 完整色阶生成。

## Conflict check

- 与 pretty-ui 的 `DESIGN.md` / tokens 约定对齐：init 只写可填模板与 `tokens.css` 骨架，完整体系仍归 pretty-ui。
- 契约测试原先断言 Zustand / Vitest 为默认层，本轮一并改断言。
- 不改变门禁、init/align 模式或包管理器约定。

## Rationale

用户明确给出默认前端技术选型；确认后按该栈更新唯一真源（`SKILL.md` 摘要 + `references/frontend.md` 分层与落地），并用契约测试锁住新默认与降级语义。

## Files

- `skills/project-init/SKILL.md`：更新 frontend 默认与例外摘要
- `skills/project-init/references/frontend.md`：分层表、建议→行为、Vite/Next 落地、目录、冒烟、align
- `skills/project-init/tests/test_project_init_contract.py`：守卫新默认关键词与降级用语

## Validation

- `git apply --check --recount` 通过后再应用
- `python3 -m pytest skills/project-init/tests -q`
- `git diff --check -- skills/project-init`（排除 patches/）
