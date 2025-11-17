# tools/utils/path_utils.py
from pathlib import Path
import yaml

# ============================================================
# 自动查找仓库根目录（确保能定位到 config.yaml）
# ============================================================
def find_repo_root() -> Path:
    """
    从当前文件开始，逐级向上查找 config.yaml 所在目录。
    无论 Sphinx 从哪里调用，都可正确找到仓库根。
    """
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        cfg = parent / "config.yaml"
        if cfg.exists():
            return parent

    raise FileNotFoundError("未找到 config.yaml，请确认仓库结构是否正确。")


# ============================================================
# 读取 config.yaml
# ============================================================
def load_config():
    repo_root = find_repo_root()
    cfg_path = repo_root / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader), repo_root


config, ROOT = load_config()


# ============================================================
# 通用资源（_common）
# ============================================================
def common_templates():
    return ROOT / config["common"]["templates"]

def static_images_path():
    return ROOT / config["common"]["static"]

def latex_common_path():
    return ROOT / config["common"]["latex"]


# ============================================================
# 产品线配置
# ============================================================
def get_default_product():
    return config["default_product"]

def product_conf(product: str):
    return config["products"][product]


# ============================================================
# 产品线目录
# ============================================================
def csv_path(product: str) -> Path:
    return ROOT / product_conf(product)["csv"]

def rst_source_path(product: str) -> Path:
    return ROOT / product_conf(product)["source"]

def build_html_path(product: str) -> Path:
    return ROOT / product_conf(product)["build_html"]

def build_pdf_path(product: str) -> Path:
    return ROOT / product_conf(product)["build_pdf"]


# ============================================================
# tools 路径
# ============================================================
def tools_root():
    return ROOT / config["tools_root"]
