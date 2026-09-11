"""灌入管理员账号样例（原教师演示号迁移为 admin）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, init_db
from app.db.models import User
from app.services.auth import hash_password


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        phone = "13900000001"
        exists = db.query(User).filter(User.phone == phone).first()
        if exists:
            if exists.role != "admin":
                exists.role = "admin"
                exists.nickname = "系统管理员"
                db.commit()
                print(f"已升级为管理员: {exists.nickname} ({phone})")
            else:
                print(f"管理员已存在: {exists.nickname} ({phone})")
            return
        u = User(
            nickname="系统管理员",
            phone=phone,
            password_hash=hash_password("123456"),
            role="admin",
        )
        db.add(u)
        db.commit()
        print(f"管理员账号已创建: {phone} / 123456")
    finally:
        db.close()


if __name__ == "__main__":
    main()
