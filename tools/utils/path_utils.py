# tools/utils/path_utils.py

from pathlib import Path
import yaml

# ============================================================
# 读取 config.yaml
# ============================================================
def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

config = load_config()

# 根路径（相对路径即可，自动转绝对）
ROOT = Path(config["root"]).resolve()


# ============================================================
# 通用路径（_common）
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
# 产品线下的关键目录
# ============================================================
def csv_path(product: str) -> Path:
    """CSV 输入目录"""
    return ROOT / product_conf(product)["csv"]


def rst_source_path(product: str) -> Path:
    """RST 源目录（Sphinx source）"""
    return ROOT / product_conf(product)["source"]


def build_html_path(product: str) -> Path:
    """HTML 输出目录"""
    return ROOT / product_conf(product)["build_html"]


def build_pdf_path(product: str) -> Path:
    """PDF 输出目录"""
    return ROOT / product_conf(product)["build_pdf"]


# ============================================================
# 工具路径（tools/）
# ============================================================
def tools_root():
    return ROOT / config["tools_root"]
