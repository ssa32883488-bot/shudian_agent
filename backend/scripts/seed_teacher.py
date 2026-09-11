"""兼容旧脚本名：转发到 seed_admin。"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("seed_admin.py")), run_name="__main__")
