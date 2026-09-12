# 阿里云 ECS 精简部署手册

> 基于本机 ECS（Alibaba Cloud Linux 3 · 约 2C/2G）实操沉淀。  
> **2GB 内存机器请用 slim 方案**，不要直接上完整 `docker-compose.yml`（含 Neo4j/Postgres/MinIO 易 OOM）。  
>
> **第三方 / 一键部署（自备 DeepSeek Key）**：优先看 [`docker/README.md`](../docker/README.md)  
> （`cp .env.example .env` → 填 `DEEPSEEK_KEY` → `./bootstrap_slim.sh`）。本文偏本机 ECS 运维细节。

---

## 0. 登录与账号（私密 · 勿推公网仓库）

> 下列信息供本仓库后续自动/人工部署直接使用，**不要**提交到公开 GitHub；若密码曾泄露请到阿里云控制台重置。

| 项 | 值 |
|----|-----|
| 公网 IP | `39.105.20.113` |
| SSH 端口 | `22` |
| 用户名 | `root` |
| 密码 | （本地私密保管，勿写入仓库；用环境变量 `DEPLOY_PASSWORD`） |
| 系统 | Alibaba Cloud Linux 3 (OpenAnolis) |
| 应用目录 | `/opt/shudian_agent` |
| 站点（IP） | http://39.105.20.113 |
| 域名 | `moknobita.xyz` / `www.moknobita.xyz`（需实名+NS 生效后使用） |
| DeepSeek API Key | 见本机 `shudian_agent/backend/.env` 的 `DEEPSEEK_KEY`，及服务器 `/opt/shudian_agent/docker/.env` |

### SSH 一键登录

```bash
ssh root@39.105.20.113
# 密码见本地私密渠道 / 环境变量 DEPLOY_PASSWORD
```

PowerShell / Paramiko：`shudian_agent/scripts/deploy_slim_remote.py`（需 `DEPLOY_PASSWORD`）。

### 编排与密钥文件（服务器）

```bash
cd /opt/shudian_agent/docker
# 环境变量文件（含 DEEPSEEK_KEY）
cat .env
docker compose -f docker-compose.slim.yml --env-file .env up -d --build --force-recreate
```

---

## 1. 部署目标

| 项 | 值 |
|----|-----|
| 应用 | `shudian_agent`（数电教育智能体） |
| 访问 | http://39.105.20.113 （域名就绪后用 `www.moknobita.xyz`） |
| 栈 | Nginx(前端:80) + FastAPI(后端容器内 8000) + SQLite |
| 不含 | Postgres / Redis / Neo4j / MinIO（精简） |
| 代码目录（服务器） | `/opt/shudian_agent` |

---

## 2. 上线前清单

### 2.1 云服务器

- [ ] ECS 已分配**公网 IP**
- [ ] 安全组入方向放行：
  - `TCP 22`（SSH，建议限制为自己的出口 IP）
  - `TCP 80`（HTTP）
  - 可选 `TCP 443`（HTTPS）
- [ ] 已设置 root（或 ecs-user）**密码或密钥**，本机可 SSH 登录
- [ ] 建议内存 **≥ 2GB**；完整栈建议 **≥ 4GB**

### 2.2 域名（可选，可后做）

- [ ] 域名实名认证已通过（未通过时公网常为 `Non-existent domain`）
- [ ] DNS 服务器为阿里云分配 NS（如 `dns13/14.hichina.com`）
- [ ] A 记录：`www` → 公网 IP；建议再加 `@` → 公网 IP
- [ ] 验证：`nslookup www.你的域名 8.8.8.8`

> 域名未生效时，可先用 `http://公网IP` 验收部署。

### 2.3 本机准备

- [ ] 代码含 `runtime/` 与 `frontend/` 源码（前端在 Docker 内构建，不必本机 `npm run build`）
- [ ] **自备** DeepSeek / MIMO API Key，写入服务器 `docker/.env`（由 `.env.example` 复制）
- [ ] 不要把含密钥的 `.env` 提交进 Git

---

## 3. 精简包应包含 / 应排除

### 必须带上

```text
shudian_agent/
  backend/app/
  backend/alembic/ + alembic.ini
  backend/scripts/
  backend/requirements.slim.txt
  backend/data/canonical/
  runtime/                        # netlist + schematex workbench（无 node_modules）
  data/kg/                        # 尤其 path_graph.json
  frontend/                       # 源码；镜像内 npm run build，不必再带 dist
  docker/
    docker-compose.slim.yml
    Dockerfile.backend.slim
    Dockerfile.frontend.slim
    nginx.slim.conf
    .env.example → 服务器复制为 .env 并自填 DEEPSEEK_KEY
    bootstrap_slim.sh / bootstrap_slim.ps1
    daemon.json.cn                # Docker 国内镜像参考
```

### 不要上传

- `backend/.venv/`、`frontend/node_modules/`
- `__pycache__/`、评测/验收大目录、`docs` 草稿（可选）
- 根目录 `_crawl`、`课本` PDF/ZIP、workbench 的 `node_modules`
- 本机 Windows 绝对路径的 `.env`（如 `C:/Users/.../chroma`）

---

## 4. 服务器初始化（首次）

### 4.1 SSH 登录

```bash
ssh root@39.105.20.113
# 密码见环境变量 DEPLOY_PASSWORD / 本地私密保管
```

### 4.2 加 Swap（2G 机强烈建议）

```bash
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
fi
free -h
```

### 4.3 安装 Docker（国内源）

`get.docker.com` 在国内常失败，用阿里云 Docker CE 源：

```bash
dnf -y install yum-utils device-mapper-persistent-data lvm2 || true
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable docker
systemctl start docker
docker --version
docker compose version
```

### 4.4 Docker Hub 加速

```bash
mkdir -p /etc/docker
cat > /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://docker.1ms.run",
    "https://mirror.ccs.tencentyun.com",
    "https://hub-mirror.c.163.com"
  ],
  "max-concurrent-downloads": 10
}
EOF
systemctl daemon-reload
systemctl restart docker
```

### 4.5 宿主机 pip 默认走阿里云（可选）

```bash
cat > /etc/pip.conf <<'EOF'
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
timeout = 120
EOF
```

---

## 5. 上传代码并启动

### 5.1 本机打包示例（PowerShell）

在仓库根目录（含 `shudian_agent`）执行思路：

1. `frontend` 执行 `npm run build`
2. 用 robocopy/tar 打出 slim 包（排除 venv、node_modules）
3. `scp` / SFTP 传到服务器 `/tmp/shudian_latest.tar.gz`

### 5.2 服务器解压

```bash
rm -rf /opt/shudian_agent.bak
mv /opt/shudian_agent /opt/shudian_agent.bak 2>/dev/null || true
mkdir -p /opt
tar -xzf /tmp/shudian_latest.tar.gz -C /opt
# 得到 /opt/shudian_agent
```

### 5.3 配置环境变量

```bash
cd /opt/shudian_agent/docker
cp .env.slim .env   # 若尚未有 .env
# 编辑 .env，至少保证：
# DEEPSEEK_KEY=sk-xxxx
```

`docker-compose.slim.yml` 关键环境（摘要）：

| 变量 | 精简部署建议 |
|------|----------------|
| `DATABASE_URL` | `sqlite:///./data/shudian_agent.db` |
| `DEEPSEEK_MOCK` | `false` |
| `DEEPSEEK_KEY` | 真实 Key |
| `DEEPSEEK_MODEL` | `deepseek-flash` |
| `DEEPSEEK_OCR_MODEL` | `deepseek-flash` |
| `BGE_USE_REAL_MODEL` | `false`（省内存） |
| `NEO4J_ENABLED` | `false` |
| `AUTH_DISABLED` | `false`（强制登录） |
| `MEDIA_BASE_URL` | `http://39.105.20.113/media` |
| `HF_ENDPOINT` | `https://hf-mirror.com` |

### 5.4 构建并启动

```bash
cd /opt/shudian_agent/docker
docker compose -f docker-compose.slim.yml --env-file .env up -d --build --force-recreate

docker ps
docker logs -f docker-backend-1
```

### 5.5 验收

```bash
curl -I http://127.0.0.1/
# 浏览器：http://39.105.20.113/

# 解题冒烟（示例）
curl -s -X POST http://127.0.0.1/api/student/solve \
  -H 'Content-Type: application/json' \
  -H 'X-Dev-Persona: student' \
  -d '{"text":"hi"}'
```

期望：首页 HTTP 200；解题接口返回业务 JSON（非 Checkpointer / Session 序列化 500）。

---

## 6. 国内源约定（构建相关）

| 类型 | 推荐 |
|------|------|
| 基础镜像 | `docker.m.daocloud.io/library/python:3.12-slim`、`nginx:1.27-alpine` |
| PyPI | `https://mirrors.aliyun.com/pypi/simple/` |
| npm（若容器内 build 前端） | `https://registry.npmmirror.com` |
| HuggingFace | `HF_ENDPOINT=https://hf-mirror.com` |
| Debian apt（若 Dockerfile 装编译工具） | `mirrors.aliyun.com` |

对应文件：

- `docker/Dockerfile.backend.slim`
- `docker/Dockerfile.frontend.slim`
- `docker/daemon.json.cn`

---

## 7. 日常运维

```bash
# 状态
docker ps
docker compose -f /opt/shudian_agent/docker/docker-compose.slim.yml ps

# 日志
docker logs --tail 100 docker-backend-1
docker logs --tail 50 docker-frontend-1

# 重启
cd /opt/shudian_agent/docker
docker compose -f docker-compose.slim.yml restart

# 停服
docker compose -f docker-compose.slim.yml down

# 更新代码后重建
docker compose -f docker-compose.slim.yml --env-file .env up -d --build --force-recreate
```

数据卷：`docker_backend_data`（SQLite / Chroma 等持久化）。重建容器一般不丢 volume；删 volume 会清空库。

---

## 8. 踩坑与已修问题（务必知晓）

### 8.1 前端 `dist` 过期

Slim 前端镜像默认 `COPY frontend/dist`。若只更新了 `src` 未 `npm run build`，线上仍是旧 UI。  
**每次发版前必须本地 build dist，或改用多阶段 Node 构建 Dockerfile。**

### 8.2 Checkpointer + SQLAlchemy Session

`SolveState` 含 DB `Session`，不能挂 LangGraph Checkpointer（会报缺 `thread_id` 或 `Type is not msgpack serializable: Session`）。  
当前 `solve_graph` **不挂 checkpointer**，单次请求解题即可。

### 8.3 容器路径 `parents[N]` IndexError

Docker 内代码深度浅于本机 monorepo，`runners.py` / `media.py` 等需安全取 `parents`，不能写死 `parents[5]`。

### 8.4 域名 Non-existent domain

多为**实名未过**或 NS 未切到云解析，不是 A 记录配错那么简单。先修实名与 NS，再用 `nslookup`。

### 8.5 内存与 BGE

2G 机器请保持 `BGE_USE_REAL_MODEL=false`。真向量模型 + Chroma 重灌极易 OOM。

### 8.6 安全

- 生产勿设 `AUTH_DISABLED=true` 对公网裸奔  
- Root 密码若曾出现在聊天/工单，部署后**重置密码**  
- `.env` 中的 API Key 轮换

---

## 9. 目录与端口对照

| 容器 | 宿主机端口 | 说明 |
|------|------------|------|
| `docker-frontend-1` | **80** | Nginx；`/api`、`/media` 反代到 backend |
| `docker-backend-1` | 不映射（仅 compose 网络内 8000） | FastAPI |

Nginx 关键见 `docker/nginx.slim.conf`。

---

## 10. 从完整 compose 迁到 slim 时注意

完整 `docker-compose.yml` 含 Windows 绝对路径挂载（如 `C:/Users/.../chroma`），**不能原样用于 Linux**。  
教材图、Chroma 预置库若需要，请改为：

- 相对路径挂载，或  
- 事先 `docker cp` / 导入 volume，或  
- 容器内执行 ingest 脚本  

---

## 11. 快速回顾命令（复制用）

```bash
# 本机
cd shudian_agent/frontend && npm run build

# 服务器（已上传并解压到 /opt/shudian_agent）
cd /opt/shudian_agent/docker
cp -n .env.slim .env
# 填 DEEPSEEK_KEY
docker compose -f docker-compose.slim.yml --env-file .env up -d --build --force-recreate
curl -I http://127.0.0.1/
```

浏览器打开：`http://39.105.20.113/`  
强制刷新（Ctrl+F5）以免旧前端缓存。

SSH：`ssh root@39.105.20.113`（密码见文首 §0）。

---

## 12. 相关文件索引

| 文件 | 作用 |
|------|------|
| `docker/docker-compose.slim.yml` | 精简编排 |
| `docker/Dockerfile.backend.slim` | 后端镜像（阿里云 PyPI） |
| `docker/Dockerfile.frontend.slim` | 前端 Nginx + dist |
| `docker/nginx.slim.conf` | `/api` `/media` 反代 |
| `docker/.env.slim` | 密钥模板 |
| `backend/requirements.slim.txt` | 无 torch/neo4j 的依赖集 |
| `docker/README.md` | 本地完整一键演示（非 2G 云主机） |

---

*文档随 2026-09 阿里云精简上线实操整理；若升配到 4G+ 再考虑启用 Postgres / 真 BGE / MinIO。*
