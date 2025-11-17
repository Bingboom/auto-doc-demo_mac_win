from utils.path_utils import latex_common_path

LATEX_DIR = latex_common_path()

def load_latex_styles():
    """加载 latex 模板"""

    files = {
        "fontpkg": LATEX_DIR / "fonts.tex",
        "preamble": LATEX_DIR / "base_preamble.tex",
        "headerfooter": LATEX_DIR / "headerfooter.tex",
        "cover": LATEX_DIR / "cover.tex",
    }

    styles = {}

    for k, p in files.items():
        if not p.exists():
            raise FileNotFoundError(f"❌ 缺少 LaTeX 模板：{p}")
        styles[k] = p.read_text(encoding="utf-8")

    styles["preamble_full"] = styles["preamble"] + "\n" + styles["headerfooter"]

    return styles
