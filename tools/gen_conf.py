from pathlib import Path

# -------------------------------------------------------------
# 1. 强制定位仓库根目录（防止 Sphinx cwd 干扰）
# -------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]     # auto-doc-demo_mac_win/
TOOLS_ROOT   = THIS_FILE.parents[1]     # tools/

# 避免 import tools 失败
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

import tools.utils.path_utils as paths

def generate_conf(product, lang):
    target = paths.rst_source_path(product, lang) / "conf.py"
    target.parent.mkdir(parents=True, exist_ok=True)

    content = f"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import tools.utils.path_utils as paths

PRODUCT = "{product}"
LANG = "{lang}"
paths = paths

COMMON_CONF = PROJECT_ROOT / "docs" / "_common" / "conf_common.py"
exec(COMMON_CONF.read_text(encoding="utf-8"), globals())
"""

    target.write_text(content, encoding="utf-8")
    print(f"[OK] conf.py → {target}")

def main():
    cfg = paths.config
    products = cfg["products"].keys()
    languages = cfg["languages"]

    for product in products:
        for lang in languages:
            generate_conf(product, lang)

if __name__ == "__main__":
    main()
