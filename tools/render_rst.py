# ============================================================
# render_rst.py — Final Stable Version (Bilingual + _en Fields)
# ============================================================

import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import sys

# ------------------------------------------------------------
# Load path_utils
# ------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
TOOLS_DIR = THIS_FILE.parent
UTILS_DIR = TOOLS_DIR / "utils"
sys.path.insert(0, str(UTILS_DIR))
import path_utils as pu


# ------------------------------------------------------------
# Load language packages
# ------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = REPO_ROOT / "docs" / "_langs"
sys.path.insert(0, str(LANG_DIR))

print(f"[语言包目录] {LANG_DIR}")

def safe_import(name):
    try:
        module = __import__(name)
        print(f"✔ 语言包加载成功: {name}")
        return module
    except Exception as e:
        print(f"❌ {name} 加载失败: {e}")
        return None

zh_mod = safe_import("zh_cn")
en_mod = safe_import("en")


# ------------------------------------------------------------
# Default field map (_en fallback)
# ------------------------------------------------------------
def _get_field_map(module, is_en: bool):
    if module and hasattr(module, "FIELD_MAP"):
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


# ------------------------------------------------------------
# Language config
# ------------------------------------------------------------
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

# Auto-complete fields
for lang, info in LANG_CONFIG.items():
    mod = info["module"]
    info["FIELD_MAP"] = _get_field_map(mod, info["is_en"])
    info["LABELS"] = getattr(mod, "LABELS", {}) if mod else {}
    info["title"] = getattr(mod, "PROJECT_TITLE", info.get("title", "AT Commands Manual"))


# ------------------------------------------------------------
# Field getter
# ------------------------------------------------------------
def get_field(row, base, fmap):
    f = fmap.get(base, base)

    if f in row and str(row[f]).strip():
        return str(row[f]).strip()

    if base in row and str(row[base]).strip():
        return str(row[base]).strip()

    return ""


# ------------------------------------------------------------
# Init templates
# ------------------------------------------------------------
env = Environment(loader=FileSystemLoader(str(pu.common_templates())))
env.globals.update(max=max, len=len)
cmd_tmpl = env.get_template("command_page.j2")


# ------------------------------------------------------------
# Main renderer
# ------------------------------------------------------------
def render_all():
    print("\n📘 开始生成 RST（双语模式）\n")

    cfg = pu.config
    languages = list(cfg["doc_types"]["AT"].keys())
    products = list(cfg["products"].keys())

    for lang in languages:
        info = LANG_CONFIG[lang]
        fmap = info["FIELD_MAP"]
        labels = info["LABELS"]

        for product in products:
            print(f"🌍 生成语言={lang} 产品={product}")

            csv_file = pu.csv_path(lang, product) / f"at_{product}.csv"
            df = pd.read_csv(csv_file, dtype=str).fillna("")

            rst_dir = pu.rst_source_path(product, lang)
            rst_dir.mkdir(parents=True, exist_ok=True)

            # group by chapter
            chapters = []
            for chap_id, grp in df.groupby("章节", sort=True):
                chap_name = get_field(grp.iloc[0], "章节名称", fmap)
                if not chap_name:
                    chap_name = info["chapter_label_tpl"].format(no=chap_id)
                chapters.append((chap_id, chap_name, grp))

            # ------------------------------------------------
            # Render commands
            # ------------------------------------------------
            for chap_id, chap_name, grp in chapters:
                chap_dir = rst_dir / str(chap_id)
                chap_dir.mkdir(parents=True, exist_ok=True)

                cmd_list = []

                for _, row in grp.iterrows():
                    cmd_name = row["命令"].strip()
                    cmd_list.append(cmd_name)

                    # ========== FIX: subtypes real parsing ==========
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
                    # =================================================

                    rendered = cmd_tmpl.render(
                        cmd_name=cmd_name,
                        cmd_title=get_field(row, "命令标题", fmap),
                        desc=get_field(row, "功能描述", fmap),
                        subtypes=subtypes,
                        parameters=json.loads(get_field(row, "参数json", fmap) or "{}"),
                        note=get_field(row, "备注", fmap),
                        response_fix=get_field(row, "响应校正", fmap),
                        labels=labels,
                    )

                    (chap_dir / f"{cmd_name}.rst").write_text(
                        rendered.strip() + "\n", encoding="utf-8"
                    )

                # chapter index
                idx = env.from_string("""
{{ title }}
{{ "=" * (title|length) }}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for c in cmds %}
   {{ c }}
{% endfor %}
""").render(title=chap_name, cmds=cmd_list)

                (chap_dir / "index.rst").write_text(idx, encoding="utf-8")

            print(f"✔ 完成章节：{rst_dir}")

    print("\n🏁 所有语言生成完毕！")


if __name__ == "__main__":
    render_all()
