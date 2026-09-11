#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传教材图片到 MinIO。

用法（在 shudian_agent 项目根目录）:
  pip install minio
  python data/upload_textbook_images.py
  python data/upload_textbook_images.py --dry-run

对象键：
  chapters/<hash>.jpg  ← 正文「按章节拆分」
  guide/<hash>.jpg     ← 学习辅导

公网 URL = {MEDIA_BASE_URL}/{object_key}
"""
from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
REPO = ROOT.parent
sys.path.insert(0, str(BACKEND))

from app.config import get_settings  # noqa: E402


def _default_image_roots() -> list[tuple[Path, str]]:
    """(本地目录, object key 前缀)。"""
    base = REPO / "课本" / "课本加习题册" / "markdown_云端解析"
    return [
        (base / "按章节拆分" / "images", "chapters"),
        (base / "学习辅导按章节拆分" / "images", "guide"),
    ]


def _content_type(path: Path) -> str:
    ctype, _ = mimetypes.guess_type(str(path))
    return ctype or "application/octet-stream"


def upload(
    roots: list[tuple[Path, str]],
    *,
    dry_run: bool = False,
    skip_existing: bool = True,
) -> None:
    settings = get_settings()
    endpoint = os.getenv("MINIO_ENDPOINT", settings.minio_endpoint)
    access = os.getenv("MINIO_ACCESS_KEY", settings.minio_access_key)
    secret = os.getenv("MINIO_SECRET_KEY", settings.minio_secret_key)
    bucket = os.getenv("MINIO_BUCKET", settings.minio_bucket)
    secure = os.getenv("MINIO_SECURE", str(settings.minio_secure)).lower() in {
        "1",
        "true",
        "yes",
    }
    media_base = os.getenv("MEDIA_BASE_URL", settings.media_base_url).rstrip("/")

    files: list[tuple[Path, str]] = []
    for root, prefix in roots:
        if not root.is_dir():
            print(f"[skip] 目录不存在: {root}")
            continue
        for p in sorted(root.glob("*")):
            if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                files.append((p, f"{prefix}/{p.name}"))

    print(f"待上传 {len(files)} 张 → bucket={bucket} endpoint={endpoint}")
    print(f"MEDIA_BASE_URL={media_base}")
    if dry_run:
        for _, key in files[:5]:
            print(f"  dry-run {key} → {media_base}/{key}")
        if len(files) > 5:
            print(f"  ... 另有 {len(files) - 5} 张")
        return

    from minio import Minio
    from minio.error import S3Error

    client = Minio(endpoint, access_key=access, secret_key=secret, secure=secure)
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"已创建 bucket: {bucket}")

    uploaded = skipped = failed = 0
    for path, key in files:
        try:
            if skip_existing:
                try:
                    client.stat_object(bucket, key)
                    skipped += 1
                    continue
                except S3Error:
                    pass
            client.fput_object(
                bucket_name=bucket,
                object_name=key,
                file_path=str(path),
                content_type=_content_type(path),
            )
            uploaded += 1
            if uploaded % 200 == 0:
                print(f"  ... 已上传 {uploaded}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[fail] {key}: {exc}")

    print(f"完成: uploaded={uploaded} skipped={skipped} failed={failed}")
    if files:
        sample_key = files[0][1]
        print(f"示例 URL: {media_base}/{sample_key}")


def main() -> None:
    parser = argparse.ArgumentParser(description="上传教材图片到 MinIO")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="即使对象已存在也重新上传",
    )
    parser.add_argument(
        "--chapters-dir",
        type=str,
        default="",
        help="覆盖正文 images 目录",
    )
    parser.add_argument(
        "--guide-dir",
        type=str,
        default="",
        help="覆盖辅导 images 目录",
    )
    args = parser.parse_args()

    roots = _default_image_roots()
    if args.chapters_dir:
        roots[0] = (Path(args.chapters_dir), "chapters")
    if args.guide_dir:
        roots[1] = (Path(args.guide_dir), "guide")

    upload(roots, dry_run=args.dry_run, skip_existing=not args.force)


if __name__ == "__main__":
    main()
