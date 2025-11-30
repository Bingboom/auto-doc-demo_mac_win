from pathlib import Path
import yaml
from tools.utils import path_utils as paths

# 统一从 path_utils 拿 ROOT，不再手写 parents[..]
ROOT = paths.ROOT

# 约定：PDF 主题目录 = ROOT / tools / themes / pdf
PDF_THEME_ROOT = ROOT / "tools" / "themes" / "pdf"




def _template_key(f: Path) -> str:
    """
    根据文件名生成 key：
      - theme.tex.j2      -> "theme"
      - headerfooter.tex.j2 -> "headerfooter"
      - fonts.tex.j2      -> "fonts"
      - colors.tex.j2     -> "colors"
    """
    name = f.name

    if name.endswith(".tex.j2"):
        # 去掉尾部的 ".tex.j2"
        base = name[:-len(".tex.j2")]   # 例如 "theme.tex" -> "theme"
        # 再把残余的 ".tex" 去掉
        if base.endswith(".tex"):
            base = base[:-len(".tex")]  # "theme.tex" -> "theme"
        return base

    if name.endswith(".j2"):
        # 普通 j2 模板，比如 "something.j2" -> "something"
        return name[:-3]

    # 理论上不会走到这里，兜底
    return f.stem


def load_pdf_theme(theme_name: str):
    """
    加载指定 PDF 主题：
      - 主题目录：ROOT/tools/themes/pdf/<theme_name>/
      - 必须包含：theme.yaml + theme.tex.j2
      - 返回： (theme_cfg: dict, theme_files: dict[str, Path])
    """
    theme_dir = PDF_THEME_ROOT / theme_name
    if not theme_dir.exists():
        raise FileNotFoundError(f"PDF 主题不存在: {theme_dir}")

    # 1) 读取 theme.yaml（如果存在）
    yaml_file = theme_dir / "theme.yaml"
    if yaml_file.exists():
        theme_cfg = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    else:
        theme_cfg = {}

    # 2) 收集所有 *.j2 模板
    theme_files = {}
    for f in theme_dir.glob("*.j2"):
        key = _template_key(f)
        theme_files[key] = f

    # 打印一下方便你调试
    print(f"[THEME] loaded templates from {theme_dir}: {list(theme_files.keys())}")

    # 3) 必须包含 theme.tex.j2 -> key="theme"
    if "theme" not in theme_files:
        raise FileNotFoundError(
            f"theme.tex.j2 未被识别为 'theme'，当前模板 keys: {list(theme_files.keys())}"
        )

    return theme_cfg, theme_files
