"""Run remote deploy assuming /tmp/shudian_latest.tar.gz already exists."""
from __future__ import annotations

import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import paramiko

HOST = os.environ.get("DEPLOY_HOST", "39.105.20.113")
USER = os.environ.get("DEPLOY_USER", "root")
PASSWORD = os.environ.get("DEPLOY_PASSWORD", "")
LOCAL_TAR = os.environ.get("DEPLOY_TAR", r"f:\code\shudian_latest.tar.gz")
REMOTE_TAR = "/tmp/shudian_latest.tar.gz"
REMOTE_SH = "/tmp/deploy_shudian_slim.sh"
SKIP_UPLOAD = os.environ.get("SKIP_UPLOAD", "0") == "1"

REMOTE_SCRIPT = r"""#!/bin/bash
set -euo pipefail
echo "== host =="
free -h | head -2
docker --version
docker compose version
ls -lh /tmp/shudian_latest.tar.gz

if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  grep -q swapfile /etc/fstab || echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
fi

rm -rf /opt/shudian_agent.bak
if [ -d /opt/shudian_agent ]; then
  mv /opt/shudian_agent /opt/shudian_agent.bak
fi
mkdir -p /opt
tar -xzf /tmp/shudian_latest.tar.gz -C /opt
test -d /opt/shudian_agent/docker
cd /opt/shudian_agent/docker

if [ -f /opt/shudian_agent.bak/docker/.env ]; then
  # 新包已带 .env；若新包无有效 Key 则回退旧 Key
  if ! grep -qE '^[[:space:]]*(DEEPSEEK_KEY|MIMO_API_KEY)=.+' .env 2>/dev/null || grep -qE '^[[:space:]]*(DEEPSEEK_KEY|MIMO_API_KEY)=\s*$' .env 2>/dev/null; then
    cp /opt/shudian_agent.bak/docker/.env .env
  fi
elif [ ! -f .env ]; then
  cp .env.example .env
fi
# 必须自备 Key：拒绝空密钥（优先 DEEPSEEK_KEY，兼容 MIMO_API_KEY）
if ! grep -qE '^[[:space:]]*DEEPSEEK_KEY=.+' .env && ! grep -qE '^[[:space:]]*MIMO_API_KEY=.+' .env; then
  echo "ERROR: 请在 /opt/shudian_agent/docker/.env 填写自备 DEEPSEEK_KEY 后再部署" >&2
  exit 1
fi
if grep -qE '^[[:space:]]*DEEPSEEK_KEY=\s*$' .env && ! grep -qE '^[[:space:]]*MIMO_API_KEY=.+' .env; then
  echo "ERROR: 请在 /opt/shudian_agent/docker/.env 填写自备 DEEPSEEK_KEY 后再部署" >&2
  exit 1
fi
# 若只有旧名，写入 DEEPSEEK_KEY 供 compose 使用
if ! grep -qE '^[[:space:]]*DEEPSEEK_KEY=.+' .env && grep -qE '^[[:space:]]*MIMO_API_KEY=.+' .env; then
  OLDKEY="$(grep -E '^[[:space:]]*MIMO_API_KEY=' .env | tail -1 | cut -d= -f2-)"
  echo "DEEPSEEK_KEY=${OLDKEY}" >> .env
fi
# 公网媒体前缀（若仍是本机/相对路径则纠正）
if grep -qE '^MEDIA_BASE_URL=(/media|http://127\.|http://localhost)' .env || ! grep -q '^MEDIA_BASE_URL=' .env; then
  if grep -q '^MEDIA_BASE_URL=' .env; then
    sed -i 's|^MEDIA_BASE_URL=.*|MEDIA_BASE_URL=http://39.105.20.113/media|' .env
  else
    echo 'MEDIA_BASE_URL=http://39.105.20.113/media' >> .env
  fi
fi
# 强制真实登录
if grep -q '^AUTH_DISABLED=' .env; then
  sed -i 's/^AUTH_DISABLED=.*/AUTH_DISABLED=false/' .env
else
  echo 'AUTH_DISABLED=false' >> .env
fi

echo "== compose up =="
export DOCKER_BUILDKIT=1
# 先拉/起基础设施，再构建应用（降低 2G 机并行 OOM）
docker compose -f docker-compose.slim.yml --env-file .env up -d postgres redis minio
sleep 8
docker compose -f docker-compose.slim.yml --env-file .env up -d minio-init || true
docker compose -f docker-compose.slim.yml --env-file .env build backend
docker compose -f docker-compose.slim.yml --env-file .env build frontend
docker compose -f docker-compose.slim.yml --env-file .env up -d --force-recreate
sleep 25
docker ps
echo "== curl home =="
curl -sI http://127.0.0.1/ | head -8
echo "== curl health =="
curl -s http://127.0.0.1/health || true
echo
echo "== draw runtime =="
docker compose -f docker-compose.slim.yml --env-file .env exec -T backend python -m scripts.check_draw_runtime || true
echo "== auth check (expect 401 without token) =="
curl -s -o /tmp/solve_noauth.txt -w "%{http_code}" -X POST http://127.0.0.1/api/student/solve \
  -H 'Content-Type: application/json' \
  -d '{"text":"hi"}'
echo
head -c 200 /tmp/solve_noauth.txt; echo
echo "== login demo admin =="
curl -s -X POST http://127.0.0.1/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"phone":"13900000001","password":"123456"}' | head -c 300
echo
echo "== deploy done =="
"""


def connect() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(1, 6):
        try:
            print(f"connect attempt {attempt} ...")
            client.connect(
                HOST,
                username=USER,
                password=PASSWORD,
                timeout=60,
                banner_timeout=60,
                auth_timeout=60,
                allow_agent=False,
                look_for_keys=False,
            )
            t = client.get_transport()
            if t:
                t.set_keepalive(15)
            return client
        except Exception as exc:
            print(f"  fail: {exc}")
            time.sleep(3 * attempt)
    raise RuntimeError("ssh connect failed")


def main() -> int:
    if not PASSWORD:
        print("DEPLOY_PASSWORD required", file=sys.stderr)
        return 2

    client = connect()
    sftp = client.open_sftp()

    if not SKIP_UPLOAD:
        if not os.path.isfile(LOCAL_TAR):
            print(f"missing {LOCAL_TAR}", file=sys.stderr)
            return 2
        size = os.path.getsize(LOCAL_TAR)
        print(f"upload tar {size/1e6:.1f} MB")
        last = {"t": time.time()}

        def cb(transferred: int, total: int) -> None:
            now = time.time()
            if now - last["t"] > 2 or transferred == total:
                last["t"] = now
                print(f"  {transferred/1e6:.1f}/{total/1e6:.1f} MB")

        # write via temp then rename for resilience
        tmp = REMOTE_TAR + ".part"
        sftp.put(LOCAL_TAR, tmp, callback=cb)
        try:
            sftp.remove(REMOTE_TAR)
        except OSError:
            pass
        sftp.rename(tmp, REMOTE_TAR)
    else:
        print("SKIP_UPLOAD=1, reuse remote tar")

    with sftp.file(REMOTE_SH, "w") as f:
        f.write(REMOTE_SCRIPT.replace("\r\n", "\n"))
    sftp.chmod(REMOTE_SH, 0o755)
    sftp.close()

    print("run remote script (docker build may take several minutes)...")
    stdin, stdout, stderr = client.exec_command(f"bash {REMOTE_SH}", timeout=2400)
    channel = stdout.channel
    while not channel.exit_status_ready():
        while channel.recv_ready():
            sys.stdout.write(channel.recv(4096).decode("utf-8", "replace"))
            sys.stdout.flush()
        while channel.recv_stderr_ready():
            sys.stderr.write(channel.recv_stderr(4096).decode("utf-8", "replace"))
            sys.stderr.flush()
        time.sleep(0.5)
    # drain
    while channel.recv_ready():
        sys.stdout.write(channel.recv(4096).decode("utf-8", "replace"))
    while channel.recv_stderr_ready():
        sys.stderr.write(channel.recv_stderr(4096).decode("utf-8", "replace"))
    code = channel.recv_exit_status()
    print(f"\nexit={code}")
    client.close()
    return 0 if code == 0 else code


if __name__ == "__main__":
    raise SystemExit(main())
