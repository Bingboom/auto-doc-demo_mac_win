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

def static_images_path() -> Path:
    """返回当前主题的 _static 目录，而不是 common.static 的固定值"""
    theme_name = config.get("theme", {}).get("pdf_default", "neoway_default")
    return ROOT / "tools" / "themes" / "pdf" / theme_name / "_static"


# ========================================
# PDF Theme Root
#   tools/themes/pdf/
# ========================================
def pdf_theme_root() -> Path:
    """
    返回 PDF 主题根目录，例如：
    ROOT / tools / themes / pdf
    """
    return ROOT / "tools" / "themes" / "pdf"


# ============================================================
# pdf 主题目录
# ============================================================
def latex_theme_path() -> Path:
    """
    返回当前 PDF 主题的 LaTeX 目录路径。
    优先使用 common.latex_theme，没有则回退到 common.latex（兼容旧版）。
    """
    common_cfg = config.get("common", {})
    latex_dir = common_cfg.get("latex_theme") or common_cfg.get("latex")

    if not latex_dir:
        # 最兜底：防止 key 写错导致直接爆炸
        latex_dir = "docs/_common/latex_templates"

    return ROOT / latex_dir

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

# ============================================================
# PDF Theme Loader: load theme.yaml
# ============================================================
import yaml

def load_pdf_theme_cfg(theme_name: str) -> dict:
    """
    读取 tools/themes/pdf/<theme_name>/theme.yaml
    不存在则返回 {}（绝不抛异常）
    """
    try:
        root = ROOT / "tools" / "themes" / "pdf" / theme_name
        cfg_file = root / "theme.yaml"

        if cfg_file.exists():
            return yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}
        else:
            return {}  # 无 theme.yaml 返回空
    except Exception:
        return {}
