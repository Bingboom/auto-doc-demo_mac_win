"""
render_rst.py — 最终完整版（适配 _en 字段 + 修复 TOC 缩进）
✓ 使用 tools/utils/path_utils.py
✓ 语言脚本来自 docs/_common/_lang/zh_CN.py & en.py
✓ 支持 *_en 字段自动读取，fallback 中文字段
✓ 多语言目录自动生成 docs/{lang}/{product}/source
✓ index.rst / chapter index 缩进完全与原版一致（不会再出错）
"""

import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path
import sys


# ============================================================
# (1) 加载 path_utils（tools/utils/path_utils.py）
# ============================================================

THIS_FILE = Path(__file__).resolve()
TOOLS_DIR = THIS_FILE.parent
UTILS_DIR = TOOLS_DIR / "utils"

sys.path.insert(0, str(UTILS_DIR))
import path_utils as pu  # noqa: E402


# ============================================================
# (2) 加载语言脚本 docs/_common/_lang/*.py
# ============================================================

REPO_ROOT = TOOLS_DIR.parent
LANG_DIR = REPO_ROOT / "docs" / "_common" / "_lang"
sys.path.insert(0, str(LANG_DIR))

try:
    import zh_CN as zh_mod
except ImportError:
    zh_mod = None

try:
    import en as en_mod
except ImportError:
    en_mod = None


# ============================================================
# (3) 默认 language 字段映射（基于 *_en）
# ============================================================

def _get_field_map(module, is_en: bool):
    """如果语言模块有 FIELD_MAP，使用它；否则自动创建 _en 映射。"""
    if module is not None and hasattr(module, "FIELD_MAP"):
        return module.FIELD_MAP

    if is_en:
        return {
            "章节名称": "章节名称_en",
            "命令标题": "命令标题_en",
            "功能描述": "功能描述_en",
            "示例命令": "示例命令_en",
            "备注": "备注_en",
            "响应校正": "响应校正_en",
            "参数": "参数_en",
            "参数json": "参数json_en",
        }

    else:
        return {
            "章节名称": "章节名称",
            "命令标题": "命令标题",
            "功能描述": "功能描述",
            "示例命令": "示例命令",
            "备注": "备注",
            "响应校正": "响应校正",
            "参数": "参数",
            "参数json": "参数json",
        }


# ============================================================
# (4) 多语言配置
# ============================================================

LANG_CONFIG = {
    "zh_cn": {
        "module": zh_mod,
        "is_en": False,
        "toc": "目录",
        "appendix": "附录",
        "chapter_label_tpl": "第{no}章",
    },
    "en": {
        "module": en_mod,
        "is_en": True,
        "toc": "Contents",
        "appendix": "Appendix",
        "chapter_label_tpl": "Chapter {no}",
    },
}

# 自动补充 title / FIELD_MAP
for lang, info in LANG_CONFIG.items():
    mod = info["module"]

    if mod is not None and hasattr(mod, "PROJECT_TITLE"):
        info["title"] = mod.PROJECT_TITLE
    else:
        info["title"] = pu.config["doc_types"]["AT"].get(lang, "AT Command Manual")

    info["FIELD_MAP"] = _get_field_map(mod, info["is_en"])


# ============================================================
# (5) 字段读取函数（支持 *_en fallback）
# ============================================================

def get_field(row, base, field_map):
    mapped = field_map.get(base, base)

    # 如果英文字段有内容
    if mapped in row and str(row[mapped]).strip():
        return str(row[mapped]).strip()

    # 否则 fallback 中文
    if base in row and str(row[base]).strip():
        return str(row[base]).strip()

    return ""


# ============================================================
# (6) 初始化 Jinja2
# ============================================================

env = Environment(loader=FileSystemLoader(str(pu.common_templates())))
env.globals.update(max=max, len=len)

cmd_tmpl = env.get_template("command_page.j2")


# ============================================================
# (7) 主渲染流程
# ============================================================

def render_all():
    cfg = pu.config

    languages = list(cfg["doc_types"]["AT"].keys())
    products = list(cfg["products"].keys())

    print("📘 开始生成 RST（含 _en 字段 + 缩进修复）")

    for lang in languages:
        if lang not in LANG_CONFIG:
            print(f"⚠ 跳过未配置语言：{lang}")
            continue

        info = LANG_CONFIG[lang]
        field_map = info["FIELD_MAP"]
        doc_title = info["title"]
        toc_title = info["toc"]
        appendix_title = info["appendix"]
        chapter_lbl = info["chapter_label_tpl"]

        for product in products:

            print(f"\n🌍 语言 = {lang}, 产品 = {product}")

            csv_file = pu.csv_path(lang, product) / f"at_{product}.csv"
            df = pd.read_csv(csv_file, dtype=str).fillna("")

            rst_dir = pu.rst_source_path(product, lang)
            rst_dir.mkdir(parents=True, exist_ok=True)

            # 章节分组
            chapters = []
            for chap_id, grp in df.groupby("章节", sort=True):
                chap_name = get_field(grp.iloc[0], "章节名称", field_map)
                if not chap_name:
                    chap_name = chapter_lbl.format(no=chap_id)
                chapters.append((chap_id, chap_name, grp))

            # -------------------------------
            # Render Chapter Contents
            # -------------------------------
            for chap_id, chap_name, grp in chapters:

                chap_dir = rst_dir / str(chap_id)
                chap_dir.mkdir(parents=True, exist_ok=True)

                cmd_list = []

                for _, row in grp.iterrows():

                    cmd_name = row["命令"].strip()
                    cmd_title = get_field(row, "命令标题", field_map)
                    desc = get_field(row, "功能描述", field_map)
                    note = get_field(row, "备注", field_map)
                    response_fix = get_field(row, "响应校正", field_map)

                    cmd_list.append(cmd_name)

                    # 命令子类型
                    types = [x.strip() for x in row["命令类型"].split(";") if x.strip()]
                    formats = [x.strip() for x in row["命令格式"].split(";")]
                    responses = [x.strip() for x in row["响应"].split(";")]
                    examples = [x.strip() for x in row["示例命令"].split(";")]

                    max_len = max(len(types), len(formats), len(responses), len(examples))
                    types += [""] * (max_len - len(types))
                    formats += [""] * (max_len - len(formats))
                    responses += [""] * (max_len - len(responses))
                    examples += [""] * (max_len - len(examples))

                    subtypes = []
                    for i in range(max_len):
                        if formats[i]:
                            subtypes.append({
                                "type": types[i],
                                "fmt": formats[i],
                                "response": responses[i],
                                "example": examples[i],
                            })

                    # 参数 JSON
                    param_json = get_field(row, "参数json", field_map)
                    try:
                        parameters = json.loads(param_json)
                    except:
                        parameters = {}

                    rendered = cmd_tmpl.render(
                        cmd_name=cmd_name,
                        cmd_title=cmd_title,
                        desc=desc,
                        subtypes=subtypes,
                        parameters=parameters,
                        note=note,
                        response_fix=response_fix,
                    )

                    (chap_dir / f"{cmd_name}.rst").write_text(
                        rendered.strip() + "\n", encoding="utf-8"
                    )

                # chapter index（注意缩进！）
                chapter_index = env.from_string("""
{{ chap_name }}
{{ "=" * (chap_name|length) }}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for c in cmds %}
   {{ c }}
{% endfor %}
""").render(chap_name=chap_name, cmds=cmd_list)

                (chap_dir / "index.rst").write_text(chapter_index, encoding="utf-8")

            # -------------------------------
            # Render Main index.rst（最关键修复处）
            # -------------------------------
            main_index = env.from_string("""
{{ doc_title }}
{{ "=" * (doc_title|length) }}

.. toctree::
   :maxdepth: 1
   :caption: {{ toc_title }}
   :titlesonly:

{% for chap in chapters %}
   {{ chap[0] }}/index
{% endfor %}

{{ appendix_title }}
-----------------
.. toctree::
   :maxdepth: 1
   :titlesonly:

   appendix/abbreviations
   appendix/index
""").render(
                doc_title=doc_title,
                toc_title=toc_title,
                appendix_title=appendix_title,
                chapters=chapters,
            )

            (rst_dir / "index.rst").write_text(main_index, encoding="utf-8")

            print(f"🎯 完成 index.rst → {rst_dir/'index.rst'}")

    print("\n🏁 所有 RST 生成完成（含缩进修复）")


# ============================================================
# main
# ============================================================

if __name__ == "__main__":
    render_all()
