from pathlib import Path
import sys
import yaml

# 加载 config.yaml 配置文件
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 获取配置
config = load_config()

# 使用 config.yaml 中的路径设置
ROOT = Path(config['root']).resolve()  # 获取项目根目录
LATEX_DIR = Path(config['latex']).resolve()  # 获取 LaTeX 配置路径

def load_latex_styles():
    """
    加载 docs/_common/latex/ 目录中的 LaTeX 模板。
    """
    template_files = {
        "fontpkg": LATEX_DIR / "fonts.tex",
        "preamble": LATEX_DIR / "base_preamble.tex",
        "headerfooter": LATEX_DIR / "headerfooter.tex",
        "cover": LATEX_DIR / "cover.tex",
    }

    styles = {}

    for key, path in template_files.items():
        if not path.exists():
            raise FileNotFoundError(f"❌ 缺失 LaTeX 模板文件：{path}")

        styles[key] = path.read_text(encoding="utf-8")

    # preamble + headerfooter 合并成一个独立层（更符合 Sphinx 逻辑）
    styles["preamble_full"] = styles["preamble"] + "\n" + styles["headerfooter"]

    return styles
