---
id: project-init
name: project-init
description: >-
  按约定脚手架初始化新项目，或把已有项目架构对齐到本 skill 的约定（v1：Python API 与前端）。
  用户要求初始化项目、创建项目脚手架、scaffold，或按 project-init 对齐已有项目时使用。
---

# Project Init

面向用户的输出默认使用简体中文。命令、路径、代码、包名与既成术语保持原文。

按约定脚手架**创建**新项目，或把**已有项目**对齐到本 skill 的架构约定。v1 只覆盖 Python API 与前端两栈；栈内按需求在 reference 的分层表里选层。

## 门禁（强制）

**算触发**（白名单，用户须**显式**表达其一）：

- 点名本 skill / `project-init`；
- 明确要**初始化项目**、**创建项目脚手架**、**scaffold 新项目**；
- 明确要把**已有项目 / 已有架构向本 skill 对齐**（如「按 project-init 对齐」「对齐 FastAPI 脚手架」）。

白名单之外（加功能、改 bug、加页面或接口、`git init`、装机、克隆、启停服务等）按普通编码任务处理。过门禁后，还要等用户确认最终方案、并就缺失依赖表态，才创建目录、改依赖、改配置或重写结构。

## 范围

产物是能跑通的空壳：配置、空布局、健康检查、`.env.example`（只放变量名与无害示例值）、`.gitignore`、README。业务功能、装机与系统包、部署、CI、commit / push 留给用户或其他流程。扩栈改本 skill 的 reference，一次脚手架会话只用已有约定。

## 模式

| 模式 | 何时 | 行为 |
|------|------|------|
| `init` | 目标目录不存在、为空，或只有 git 占位（如 `README` / `.gitignore` / `.git`） | 方案确认后用官方工具命令创建，再套本 skill 约定 |
| `align` | 目标已有实质源码或依赖清单 | 对照约定出缺口报告，**确认后再改** |

`align` 沿用目录里已有的框架：已有 Django 按 Django 路径对照，已有 Next.js 按 Next.js 路径、已有 Vite 按 Vite 路径对照；Flask、Vue、CRA 等无 reference 的框架先报告不兼容。换框架属于迁移，只在用户明确要求时进入，仍先给计划再改。

一次会话只服务**一个**目标根。前后端都要时，先问清是两个根还是 monorepo 子目录，再分别套对应 reference。

## 栈：默认 + 例外

| 栈 id | 何时 | 先读 |
|-------|------|------|
| `python-api` | 像 API 服务的 Python | [references/python-api.md](references/python-api.md) |
| `frontend` | 像 SPA / 站点 UI 的前端 | [references/frontend.md](references/frontend.md) |

Python 但不是 API（CLI / 库 / 脚本）→ 告知 v1 未覆盖并停下。

**按需求选层（强制）**：分层表（含「建议」列）只在各 reference 里。用户点名的库优先，并在摘要标明偏离；需求没说到的层取默认。

- **python-api 默认**：FastAPI + Pydantic / OpenAPI + SQLAlchemy；asyncio · uvicorn；pytest · httpx；uv，推荐 Ruff 与 mypy / pyright。
  例外：要 Admin / MTV / Django 生态 → Django（特定场景再用，随 Django ORM 与 DRF）；Flask、Litestar、Tortoise 仅用户点名；模型与 schema 一体 → SQLModel；需要后台任务再用 Celery · Dramatiq · ARQ 之一；浏览器 E2E → Playwright。
- **frontend 默认**：Vite 路径——TypeScript + React + Vite + Tailwind CSS + shadcn/ui，TanStack Query、Zustand、Zod、OpenAPI / Zod 契约，Playwright E2E + Vitest。
  例外：SSR / RSC / SEO / App Router / 全栈路由，或点名 Next.js → **Next.js 路径**（`create-next-app` 承担构建与服务端，其余层不变；一次只走一条，Vite 与 Next 并存不允许）；有表单时加 React Hook Form。

包管理器：用户指定优先；否则 Python `uv`、前端 `pnpm`。缺失时列入依赖缺口并**询问是否补齐**（安装，或改用回退：Python venv + pip，前端 npm）；切换包管理器与全局安装都以用户同意为前提。

## 工作流

1. **过门禁**，判定 `init` 或 `align`。目标路径未给则询问（写入位置）。
   做完的标志：模式与目标路径已定。
2. **收集输入**：目标路径、栈、项目名、包管理器（若会写进锁文件）；`init` 确认目标可写且不覆盖已有工程。会影响选层的需求特征（Admin、后台任务、模型与 schema 一体、浏览器 E2E、SSR 等）缺则问。
3. **形成最终方案并确认**：只读对应 reference，按需求选层，列出模式、目标路径、各层选择与原因、拟用官方工具命令、将写入的约定、冒烟命令。**展示给用户并等待明确确认**；用户改需求就回到选层重出方案。
   做完的标志：用户明确确认了这份方案。
4. **检查依赖**：确认后、动手前检查方案所需命令（如 `uv`、`python3`、`pnpm`/`npm`、`node`、官方 create/init CLI），列出缺失项并**询问是否补齐**；同意后安装或启用回退，拒绝则停下或改用其指定替代。框架包经官方 CLI / `uv add` / 包管理器安装，lockfile 由工具生成。
5. **执行**：`init` **优先借助该栈官方工具命令**（`uv init`、`django-admin startproject`、`pnpm create vite`、`create-next-app`、`shadcn init`，见各 reference），再补本 skill 约定；官方 CLI 实在不可用且用户同意后才写最小可运行壳。`align` 只改已确认项，补齐同样走官方工具命令，业务代码保持原样。冒烟按 reference，跑完即停，不留长期 dev server。
   做完的标志：reference 的冒烟命令全部通过。
6. **交付摘要**（见下）。不 commit。

## 安全

- 只写用户指定或确认过的路径（家目录根、系统目录、其他仓库都不在其列）。
- `init` 遇到已有源码：改为 `align` 或停下，保留原文件。
- 只运行该栈官方文档中的 create/init CLI，不执行未审查的远程脚本。
- 真实密钥与 `.env` 值不入库。

## 交付摘要

完成后用简短列表告诉用户：

- 模式（`init` / `align`）与目标路径；方案是否已经用户确认
- 依赖检查：缺什么、是否补齐、用了什么回退
- 实际采用的栈与偏离默认之处（各层装了什么、因何需求、故意没装什么）
- 关键路径（如何启动、健康检查 URL 或 build / test 命令）
- 改了哪些文件（align 必列）
- 明确没做的事（业务、部署、CI、commit）

## 扩展

新增栈：增加 `references/<stack-id>.md`（写清分层表、官方脚手架命令、目录约定、默认依赖、冒烟命令、align 对照清单），并在上方栈表加一行。无 reference 的栈 = 未支持。同类变体（如 `frontend` 的 Vite / Next.js）优先在原 reference 内加一节。
