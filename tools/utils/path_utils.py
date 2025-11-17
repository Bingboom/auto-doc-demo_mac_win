from pathlib import Path
import yaml

# ============================================================
# 自动查找仓库根目录（确保找到 config.yaml）
# ============================================================
def find_repo_root() -> Path:
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / "config.yaml").exists():
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
# 公共资源路径（保持原样）
# ============================================================
def common_templates():
    return ROOT / config["common"]["templates"]

def static_images_path():
    return ROOT / config["common"]["static"]

def latex_common_path():
    return ROOT / config["common"]["latex"]


# ============================================================
# 产品配置（保持原样）
# ============================================================
def product_conf(product: str):
    return config["products"][product]

def get_default_product():
    return config["default_product"]


# ============================================================
# 语言注入器（精确插入在产品名后）
#   示例：
#     docs/N706B/source      → docs/N706B/zh_CN/source
#     docs/N706B/build/html  → docs/N706B/zh_CN/build/html
# ============================================================
def _inject_lang_for_product(path_str: str, product: str, lang: str) -> Path:
    p = ROOT / path_str

    # 若路径已经包含语言目录则直接返回
    if "zh_CN" in p.parts or "en" in p.parts:
        return p

    parts = list(p.parts)

    # 找到产品名在路径中的位置
    try:
        idx = parts.index(product)
    except ValueError:
        # 找不到产品名（不应该出现），回退原逻辑
        return p.parent / lang / p.name

    # 在产品名后插入语言层
    insert_pos = idx + 1
    parts.insert(insert_pos, lang)

    return Path(*parts)


# ============================================================
# 多语言路径函数（正式版）
# ============================================================
def rst_source_path(product: str, lang: str = "zh_CN") -> Path:
    base = product_conf(product)["source"]
    return _inject_lang_for_product(base, product, lang)

def build_html_path(product: str, lang: str = "zh_CN") -> Path:
    base = product_conf(product)["build_html"]
    return _inject_lang_for_product(base, product, lang)

def build_pdf_path(product: str, lang: str = "zh_CN") -> Path:
    base = product_conf(product)["build_pdf"]
    return _inject_lang_for_product(base, product, lang)


# ============================================================
# CSV 路径（保持原样，不依赖语言）
# ============================================================
def csv_path(product: str) -> Path:
    return ROOT / product_conf(product)["csv"]


# ============================================================
# tools 根路径
# ============================================================
def tools_root():
    return ROOT / config["tools_root"]
