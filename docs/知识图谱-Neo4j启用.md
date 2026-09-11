# 知识图谱 · Neo4j 启用说明

## 现状

- 学生端路由：`/kg`（侧栏「知识图谱」）
- API：`/api/student/kg/*`（status / graph / concept / ask）
- 智能体工具：`graph_query`（与可视化共用同一套 `graph_kg` 数据源）
- `.env`：`NEO4J_ENABLED=true`；Neo4j 未就绪时**自动回落 JSON**

## 启动 Neo4j（本机 Docker）

1. 打开 Docker Desktop
2. 启动服务：

```bash
cd shudian_agent/docker
docker compose up -d neo4j
```

浏览器可开 http://localhost:7474 （neo4j / shudian123）

3. 安装驱动（若未装）：

```bash
cd shudian_agent/backend
.\.venv\Scripts\pip.exe install "neo4j>=5.26.0"
```

4. 同步图谱：

```bash
cd shudian_agent/backend
.\.venv\Scripts\python.exe scripts\sync_kg_to_neo4j.py --reset
```

5. 重启后端，打开学生端 `/kg`，状态应显示 `引擎：Neo4j`。

## 验证

```bash
# 状态
curl -H "X-Dev-Persona: student" http://127.0.0.1:8001/api/student/kg/status

# 子图
curl -H "X-Dev-Persona: student" "http://127.0.0.1:8001/api/student/kg/graph?limit=30"
```
