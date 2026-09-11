"""MinIO 对象存储（可选）：教材图；失败时调用方回退本地文件。"""

from __future__ import annotations

import io
import logging
from typing import Optional

from app.config import get_settings

logger = logging.getLogger(__name__)

_client = None
_client_failed = False


def minio_enabled() -> bool:
    s = get_settings()
    # 空 endpoint 或明确关闭
    ep = (s.minio_endpoint or "").strip()
    return bool(ep) and ep.lower() not in ("", "off", "false", "none", "-")


def get_minio():
    global _client, _client_failed
    if _client is not None:
        return _client
    if _client_failed or not minio_enabled():
        return None
    try:
        from minio import Minio

        s = get_settings()
        endpoint = s.minio_endpoint.replace("http://", "").replace("https://", "")
        client = Minio(
            endpoint,
            access_key=s.minio_access_key,
            secret_key=s.minio_secret_key,
            secure=bool(s.minio_secure),
        )
        # 探活：bucket 存在即可
        if not client.bucket_exists(s.minio_bucket):
            client.make_bucket(s.minio_bucket)
        _client = client
        logger.info("MinIO 已连接: %s / %s", endpoint, s.minio_bucket)
        return _client
    except Exception as exc:  # noqa: BLE001
        logger.warning("MinIO 不可用，回退本地 /media: %s", exc)
        _client_failed = True
        return None


def get_object_bytes(object_key: str) -> Optional[bytes]:
    """读取 bucket 对象；不存在或失败返回 None。"""
    client = get_minio()
    if not client:
        return None
    s = get_settings()
    try:
        resp = client.get_object(s.minio_bucket, object_key)
        try:
            return resp.read()
        finally:
            resp.close()
            resp.release_conn()
    except Exception:
        return None


def put_object_bytes(
    object_key: str,
    data: bytes,
    *,
    content_type: str = "application/octet-stream",
) -> bool:
    client = get_minio()
    if not client:
        return False
    s = get_settings()
    try:
        client.put_object(
            s.minio_bucket,
            object_key,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("MinIO put 失败 %s: %s", object_key, exc)
        return False


def minio_info() -> dict:
    if not minio_enabled():
        return {"enabled": False, "ok": False}
    c = get_minio()
    if not c:
        return {"enabled": True, "ok": False}
    return {"enabled": True, "ok": True, "bucket": get_settings().minio_bucket}
