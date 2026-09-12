#!/usr/bin/env bash
# 精简栈一键启动（Linux / macOS / WSL）
# 用法：
#   cd shudian_agent/docker
#   cp .env.example .env    # 首次
#   编辑 .env 填写 DEEPSEEK_KEY
#   ./bootstrap_slim.sh
set -euo pipefail

cd "$(dirname "$0")"

echo "== 数电教育智能体 · slim 一键部署 =="

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: 未找到 docker。请先安装 Docker Engine + Compose 插件。" >&2
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: 需要 docker compose 插件（Docker Compose V2）。" >&2
  exit 1
fi

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "已生成 .env（来自 .env.example）。"
  else
    echo "ERROR: 缺少 .env.example" >&2
    exit 1
  fi
fi

# 读取 DEEPSEEK_KEY（兼容旧名 MIMO_API_KEY）
KEY="$(grep -E '^[[:space:]]*DEEPSEEK_KEY=' .env | tail -1 | cut -d= -f2- | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
if [ -z "$KEY" ]; then
  KEY="$(grep -E '^[[:space:]]*MIMO_API_KEY=' .env | tail -1 | cut -d= -f2- | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
fi
if [ -z "$KEY" ] || [ "$KEY" = "sk-xxx" ] || [ "$KEY" = "CHANGE_ME" ]; then
  echo ""
  echo "请先在 docker/.env 中填写自备的 DeepSeek API Key："
  echo "  DEEPSEEK_KEY=sk-xxxxxxxx"
  echo "申请：https://platform.deepseek.com/"
  echo "填好后重新执行本脚本。"
  exit 1
fi

# 2G 机器提示
if command -v free >/dev/null 2>&1; then
  MEM_MB="$(free -m | awk '/^Mem:/{print $2}')"
  if [ "${MEM_MB:-0}" -gt 0 ] && [ "$MEM_MB" -lt 1800 ]; then
    echo "WARN: 物理内存约 ${MEM_MB}MB，首次构建建议加 2G swap，否则可能 OOM。"
  fi
fi

echo "== docker compose build & up =="
docker compose -f docker-compose.slim.yml --env-file .env up -d --build

echo ""
echo "== 等待健康检查 =="
ok=0
for i in $(seq 1 30); do
  if curl -sf "http://127.0.0.1:${HTTP_PORT:-80}/health" >/dev/null 2>&1; then
    ok=1
    break
  fi
  sleep 2
done

if [ "$ok" -eq 1 ]; then
  echo "OK  http://127.0.0.1:${HTTP_PORT:-80}/  （/health 已通）"
else
  echo "WARN: /health 暂未就绪，请查看：docker compose -f docker-compose.slim.yml logs -f"
fi

echo ""
echo "演示账号（seed 后）：管理员 13900000001 / 123456"
echo "设计电路 MSI：仓库已含 Digital.jar（vendor/）；自检 python -m scripts.check_draw_runtime"
echo "绘图自检：docker compose -f docker-compose.slim.yml exec backend python -m scripts.check_draw_runtime"
