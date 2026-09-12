# 部署指南（精简 · 推荐）

> **默认路径**：`docker-compose.slim.yml`  
> 服务：Nginx + FastAPI + **Postgres + Redis + MinIO**（**不含 Neo4j**）。  
> 适合 2GB+ 云主机（务必加 swap）；全量含 Neo4j 见文末。

---

## 别人一键部署（自备 DeepSeek Key）

### 前置

- Docker Engine + Compose V2（或 Docker Desktop）
- 建议内存 ≥ 2GB；2G 机首次构建请加 **2G swap**
- **自备** [DeepSeek API Key](https://platform.deepseek.com/)

### 步骤

```bash
cd shudian_agent/docker
cp .env.example .env
# 编辑 .env：DEEPSEEK_KEY=sk-你自己的密钥

chmod +x bootstrap_slim.sh && ./bootstrap_slim.sh
# Windows：.\bootstrap_slim.ps1
```

打开：`http://127.0.0.1/`（或服务器公网 IP）

| 项 | 值 |
|----|-----|
| 健康检查 | `GET /health`（含 `database` / `redis` / `minio` 字段） |
| 演示管理员 | `13900000001` / `123456` |
| 演示学生 | `13800000001` / `123456` |

### 基础设施实装说明

| 组件 | 状态 | 用途 |
|------|------|------|
| **Postgres** | ✅ 默认启用 | 业务库（用户/题库/聊天/学情…） |
| **Redis** | ✅ 默认启用 | **登录 Token**（7 天 TTL；宕机回退内存） |
| **MinIO** | ✅ 默认启用 | 教材图对象存储；`/media` 优先读 MinIO，没有则本地文件 |
| **Neo4j** | ❌ 关闭 | 2G 不够；图谱走 JSON |

灌教材图到 MinIO（可选，有课本图片时）：

```bash
# 在能访问 MinIO 的环境（端口映射或进 backend 容器网络）
python data/upload_textbook_images.py
```

绘图产物（SVG）仍写本地 `artifacts/`，经 `/media/artifacts/` 访问。

### 常用命令

```bash
docker compose -f docker-compose.slim.yml --env-file .env ps
docker compose -f docker-compose.slim.yml --env-file .env logs -f backend
curl -s http://127.0.0.1/health
docker compose -f docker-compose.slim.yml exec backend python -m scripts.check_draw_runtime
```

改端口：`HTTP_PORT=8080 ./bootstrap_slim.sh`

---

## 环境变量要点

| 变量 | 说明 |
|------|------|
| `DEEPSEEK_KEY` | **必填** |
| `DEEPSEEK_API_BASE` | 默认 `https://api.deepseek.com/v1` |
| `DEEPSEEK_MODEL` / `OCR` | 默认 `deepseek-flash` |
| `DEEPSEEK_MOCK` | 生产填 `false` |
| `MEDIA_BASE_URL` | 默认 `/media` |
| `POSTGRES_PASSWORD` | 默认 `postgres` |
| `MINIO_ACCESS_KEY` / `SECRET` | 默认 minioadmin |

`.env` 已 gitignore，勿提交密钥。

---

## 全量栈（含 Neo4j，需 ≥4–8GB）

```bash
docker compose -f docker-compose.yml up --build
```

阿里云实操：`docs/DEPLOY-阿里云精简.md`。
