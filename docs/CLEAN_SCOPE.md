# 纯净上线范围（slim）

> 目标：服务器只跑 `shudian_agent` 精简栈；本机研发杂项不进发布包。  
> **绘图运行时**：与 `docs/定稿-绘图子系统.md` 对齐——`runtime/*_workbench` + Node/JRE 进镜像；`Digital.jar` 默认在 `app/tools/draw/digital_dig/vendor/`（GPL-3.0 上游），亦可被 `DIGITAL_JAR` 覆盖。

## 保留（产品本体）

```
shudian_agent/
  backend/app/
  backend/alembic/ + alembic.ini
  backend/scripts/          # seed_* + check_draw_runtime + smoke（部署自检可用）
  backend/requirements.slim.txt
  backend/data/canonical/                   # 教材 canonical
  runtime/netlist_workbench/                # logic_dag（无 node_modules）
  runtime/schematex_workbench/              # wave / state（无 node_modules）
  # Digital.jar → 默认 vendor/Digital.jar（随仓）；可 DIGITAL_JAR 覆盖
  data/kg/path_graph.json（及 kg 目录）
  frontend/src/ + package.json …            # 镜像内 npm build，不必预置 dist
  docker/docker-compose.slim.yml
  docker/Dockerfile.*.slim
  docker/nginx.slim.conf
  docker/.env.example → 复制为 .env 并自填 DEEPSEEK_KEY
  docker/bootstrap_slim.sh / bootstrap_slim.ps1
```

## 不进发布包 / 已淘汰或非产品

| 路径 | 原因 |
|------|------|
| 仓库根 `_archive/*` | 历史实验与素材；**workbench 已迁至 `shudian_agent/runtime/`**，`_archive` 仅本机兼容回退 |
| `textbook_schematic_workbench/`（若仍在 archive） | 文档标明停用 |
| `课本/`、`原理图/`、`_crawl/`、`_docx_extract/` | 素材/爬取，非运行时 |
| `xuelingban/`、根目录 PDF/docx/临时 txt/erc/log | 申报材料与临时文件 |
| `shudian_agent/reports/` | 评测/验收产物 |
| `backend/data/{acceptance_*,figure_recall_eval,retrieval_eval,tier_a_prompt_lab,artifacts}` | 实验产物 |
| `backend/.venv/`、`frontend/node_modules/`、`runtime/**/node_modules/` | 本机/构建时安装 |
| `docker-compose.yml` 全量栈 | 2G 机勿用；本机演示可留源码 |

> 冒烟脚本 `smoke_all_draw_kinds.py` **可进镜像**，用于部署后验收；仓库已含 `Digital.jar` 时 MSI 应可绿。

## 服务器形态

Nginx:80 + FastAPI + SQLite；无 Postgres/Redis/Neo4j/MinIO。  
出图：容器内 Node + OpenJDK17 + `runtime/` workbench；MSI 使用镜像内 `vendor/Digital.jar`。
