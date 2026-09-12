"""Pack shudian_agent slim release tarball for ECS deploy."""
from __future__ import annotations

import os
import shutil
import tarfile
from pathlib import Path

ROOT = Path(r"f:\code\揭榜挂帅-单学科教育智能体")
SRC = ROOT / "shudian_agent"
STAGING = Path(r"f:\code\_shudian_pack_staging")
OUT = Path(os.environ.get("DEPLOY_TAR", r"f:\code\shudian_latest.tar.gz"))
JAR_CANDIDATES = [
    SRC / "backend" / "app" / "tools" / "draw" / "digital_dig" / "vendor" / "Digital.jar",
    Path(r"f:\code\digital-circuit-poc\digital\Digital.jar"),
]

SKIP_DIR_NAMES = {
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
    "reports",
    ".turbo",
    "coverage",
}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return False


def copy_tree(src: Path, dst: Path) -> None:
    for root, dirs, files in os.walk(src):
        root_p = Path(root)
        # prune
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not should_skip(root_p / d)]
        rel = root_p.relative_to(src)
        target_dir = dst / rel
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            sp = root_p / name
            if should_skip(sp):
                continue
            # skip local secrets except we synthesize docker/.env later
            if sp.name == ".env" and "docker" not in sp.parts[-3:]:
                # allow nothing from backend/.env copy as file; synthesize below
                if "backend" in sp.parts:
                    continue
            if sp.name in {".env"} and "docker" in sp.parts:
                continue
            shutil.copy2(sp, target_dir / name)


def load_backend_env() -> dict[str, str]:
    env: dict[str, str] = {}
    p = SRC / "backend" / ".env"
    if not p.is_file():
        return env
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def write_docker_env(dst_docker: Path, be: dict[str, str]) -> None:
    key = (be.get("DEEPSEEK_KEY") or be.get("MIMO_API_KEY") or "").strip()
    if not key:
        raise SystemExit("backend/.env 缺少 DEEPSEEK_KEY，无法部署")
    lines = [
        f"DEEPSEEK_KEY={key}",
        f"DEEPSEEK_API_BASE={be.get('DEEPSEEK_API_BASE') or be.get('MIMO_API_BASE') or 'https://api.deepseek.com/v1'}",
        f"DEEPSEEK_MODEL={be.get('DEEPSEEK_MODEL') or be.get('MIMO_MODEL') or 'deepseek-flash'}",
        f"DEEPSEEK_OCR_MODEL={be.get('DEEPSEEK_OCR_MODEL') or be.get('MIMO_OCR_MODEL') or be.get('DEEPSEEK_MODEL') or be.get('MIMO_MODEL') or 'deepseek-flash'}",
        "DEEPSEEK_MOCK=false",
        "MEDIA_BASE_URL=http://39.105.20.113/media",
        "AUTH_DISABLED=false",
        "AUTH_SALT=shudian-agent-slim-prod-salt",
        "DEMO_CLASS_CODE=DEMO01",
        "HIT_SCORE_THRESHOLD=0.95",
        "REFLOW_MODE=manual",
        "POSTGRES_PASSWORD=postgres",
        "MINIO_ACCESS_KEY=minioadmin",
        "MINIO_SECRET_KEY=minioadmin",
        "MINIO_BUCKET=shudian-textbook",
        "DRAW_RUNTIME_ROOT=/app/runtime",
        "NODE_BIN=node",
        "AGENT_MAX_DRAW_CALLS=3",
        "DIGITAL_JAR=/app/app/tools/draw/digital_dig/vendor/Digital.jar",
        "NEO4J_ENABLED=false",
        "BGE_USE_REAL_MODEL=false",
    ]
    mineru = be.get("MINERU_TOKEN", "").strip()
    if mineru:
        lines.extend(
            [
                f"MINERU_TOKEN={mineru}",
                f"MINERU_MODE={be.get('MINERU_MODE', 'precision')}",
                f"MINERU_TIMEOUT_SEC={be.get('MINERU_TIMEOUT_SEC', '600')}",
                f"MINERU_MAX_FILE_MB={be.get('MINERU_MAX_FILE_MB', '25')}",
            ]
        )
    (dst_docker / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    dst = STAGING / "shudian_agent"
    print("copy tree...")
    copy_tree(SRC, dst)

    # ensure runtime present
    for name in ("netlist_workbench", "schematex_workbench"):
        if not (dst / "runtime" / name / "scripts").is_dir():
            raise SystemExit(f"missing runtime/{name}")

    be = load_backend_env()
    write_docker_env(dst / "docker", be)
    print("docker/.env synthesized (key present)")

    vendor = dst / "backend" / "app" / "tools" / "draw" / "digital_dig" / "vendor"
    vendor.mkdir(parents=True, exist_ok=True)
    jar_dst = vendor / "Digital.jar"
    if not jar_dst.is_file():
        for cand in JAR_CANDIDATES:
            if cand.is_file():
                shutil.copy2(cand, jar_dst)
                print(f"bundled Digital.jar from {cand} ({cand.stat().st_size/1e6:.1f} MB)")
                break
        else:
            print("WARN: Digital.jar not found; MSI draw may fail")
    else:
        print(f"vendor Digital.jar already in pack ({jar_dst.stat().st_size/1e6:.1f} MB)")

    # enable jar volume in compose for clarity (jar already in image via COPY app)
    # no change needed — jar is inside app tree

    print(f"writing {OUT} ...")
    if OUT.exists():
        OUT.unlink()
    with tarfile.open(OUT, "w:gz") as tar:
        tar.add(dst, arcname="shudian_agent")
    print(f"done {OUT.stat().st_size/1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
