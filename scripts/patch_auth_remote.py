"""Patch auth-required student.py and rebuild backend on ECS."""
from __future__ import annotations

import os
import sys
import time

import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HOST = os.environ.get("DEPLOY_HOST", "39.105.20.113")
PASSWORD = os.environ["DEPLOY_PASSWORD"]
LOCAL = r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\app\api\student.py"
REMOTE = "/opt/shudian_agent/backend/app/api/student.py"

REMOTE_SH = r"""#!/bin/bash
set -euo pipefail
cd /opt/shudian_agent/docker
docker compose -f docker-compose.slim.yml --env-file .env up -d --build --force-recreate backend
sleep 14
docker ps --format 'table {{.Names}}\t{{.Status}}'
echo 'NOAUTH_CODE='
curl -s -o /tmp/na.txt -w '%{http_code}' -X POST http://127.0.0.1/api/student/solve \
  -H 'Content-Type: application/json' \
  -d '{"text":"hi"}'
echo
echo 'NOAUTH_BODY='
head -c 200 /tmp/na.txt; echo
TOK=$(curl -s -X POST http://127.0.0.1/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"phone":"13800000001","password":"123456"}' \
  | python -c 'import sys,json; print(json.load(sys.stdin).get("token",""))')
echo "TOKEN_LEN=${#TOK}"
echo 'WITHAUTH_CODE='
curl -s -o /tmp/wa.txt -w '%{http_code}' -X POST http://127.0.0.1/api/student/solve \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${TOK}" \
  -d '{"text":"1+1=?"}'
echo
echo 'WITHAUTH_BODY='
head -c 260 /tmp/wa.txt; echo
echo DONE
"""


def main() -> int:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username="root",
        password=PASSWORD,
        timeout=60,
        allow_agent=False,
        look_for_keys=False,
    )
    t = client.get_transport()
    if t:
        t.set_keepalive(15)

    sftp = client.open_sftp()
    sftp.put(LOCAL, REMOTE)
    with sftp.file("/tmp/patch_auth.sh", "w") as f:
        f.write(REMOTE_SH.replace("\r\n", "\n"))
    sftp.chmod("/tmp/patch_auth.sh", 0o755)
    sftp.close()
    print("uploaded; rebuilding backend...")

    _, stdout, stderr = client.exec_command("bash /tmp/patch_auth.sh", timeout=900)
    ch = stdout.channel
    while not ch.exit_status_ready():
        while ch.recv_ready():
            sys.stdout.write(ch.recv(4096).decode("utf-8", "replace"))
            sys.stdout.flush()
        while ch.recv_stderr_ready():
            sys.stderr.write(ch.recv_stderr(4096).decode("utf-8", "replace"))
            sys.stderr.flush()
        time.sleep(0.3)
    while ch.recv_ready():
        sys.stdout.write(ch.recv(4096).decode("utf-8", "replace"))
    while ch.recv_stderr_ready():
        sys.stderr.write(ch.recv_stderr(4096).decode("utf-8", "replace"))
    code = ch.recv_exit_status()
    print(f"exit={code}")
    client.close()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
