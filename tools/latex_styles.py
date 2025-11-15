# tools/latex_styles.py
from pathlib import Path
import sys

# 自动将项目根目录加入 sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paths import PATHS


def load_latex_styles():
    """
    加载 docs/_common/latex/ 目录中的 LaTeX 模板。
    """
    latex_dir = PATHS["latex"]

    template_files = {
        "fontpkg": latex_dir / "fonts.tex",
        "preamble": latex_dir / "base_preamble.tex",
        "headerfooter": latex_dir / "headerfooter.tex",
        "cover": latex_dir / "cover.tex",
    }

    styles = {}

    for key, path in template_files.items():
        if not path.exists():
            raise FileNotFoundError(f"❌ 缺失 LaTeX 模板文件：{path}")

        styles[key] = path.read_text(encoding="utf-8")

    # preamble + headerfooter 合并成一个独立层（更符合 Sphinx 逻辑）
    styles["preamble_full"] = styles["preamble"] + "\n" + styles["headerfooter"]

    return styles
