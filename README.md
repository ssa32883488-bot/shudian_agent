# 数电教育智能体（学灵伴）

单学科（数字电子技术）助学智能体：学生问答 / 自适应练习 / 学情 + 管理端题库回流。

## 快速部署（Docker Slim）

需要：Docker Desktop / Compose V2，自备 [DeepSeek API Key](https://platform.deepseek.com/)。

```bash
cd docker
cp .env.example .env
# 编辑 .env，填写：DEEPSEEK_KEY=sk-你的密钥

# Windows
.\bootstrap_slim.ps1

# Linux / macOS
chmod +x bootstrap_slim.sh && ./bootstrap_slim.sh
```

浏览器打开 http://127.0.0.1/  

演示账号：管理员 `13900000001` / 学生 `13800000001`，密码均为 `123456`。

详细说明见 [`docker/README.md`](docker/README.md)。

## 栈说明

默认 slim 含：Nginx + FastAPI + **Postgres + Redis + MinIO**（不含 Neo4j）。  
绘图：8 种图类；MSI 设计电路需自备 `Digital.jar`（见 `backend/app/tools/draw/digital_dig/vendor/README.md`）。

## 文档

- `docs/产品范围-学生端与管理端.md`
- `docs/定稿-绘图子系统.md`
- `docs/技术设计-智能体构建.md`
