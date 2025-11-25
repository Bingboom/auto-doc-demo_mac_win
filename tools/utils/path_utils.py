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
# 公共资源
# ============================================================
def common_templates():
    return ROOT / config["common"]["templates"]

def static_images_path():
    return ROOT / config["common"]["static"]

def latex_common_path():
    return ROOT / config["common"]["latex"]


# ============================================================
# 产品配置读取
# ============================================================
def product_conf(product: str):
    return config["products"][product]

# ============================================================
# 新增 langs_dir()
# ============================================================

def langs_dir() -> Path:
    return ROOT / config["common"]["langs"]

# ============================================================
# 语言优先路径渲染
# ============================================================
def _render_lang_path(template: str, product: str, lang: str) -> Path:
    """修正：模板中传递 product 和 lang 变量"""
    path_str = template.format(lang=lang, product=product)
    return ROOT / path_str


# ============================================================
# 渲染路径函数：支持语言和产品
# ============================================================
def rst_source_path(product: str, lang: str = "zh_CN") -> Path:
    return _render_lang_path(product_conf(product)["source"], product, lang)

def build_html_path(product: str, lang: str = "zh_CN") -> Path:
    return _render_lang_path(product_conf(product)["build_html"], product, lang)

def build_pdf_path(product: str, lang: str = "zh_CN") -> Path:
    return _render_lang_path(product_conf(product)["build_pdf"], product, lang)


# ============================================================
# CSV 路径
# ============================================================
def csv_path(lang: str, product: str) -> Path:
    """修正：首先是语言，其次是产品"""
    return ROOT / config["products"][product]["csv"].format(lang=lang, product=product)

# 默认产品
def get_default_product():
    return config.get("default_product")

# 定义输出路径

def output_html_dir() -> Path:
    return ROOT / config["output"]["html"]

def output_pdf_dir() -> Path:
    return ROOT / config["output"]["pdf"]
