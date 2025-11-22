# ============================================================
# render_rst.py — Final Stable Version (Unified path + Safe import)
# ============================================================

"""
功能：
    1) 将 CSV 自动转换为 RST（产品 × 语言）
    2) 多子命令类型：执行/查询/测试/设置 + exec/read/test/set
    3) 支持 *_en 字段 fallback
    4) 为每个命令生成 xxx.rst
    5) 生成 chapter/index.rst
    6) 保留 docs/{lang}/{product}/source/index.rst（不会覆盖！）
"""

import json
import pandas as pd
from pathlib import Path
import sys
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------
# 1) 统一路径注入（必须先于 import path_utils）
# ------------------------------------------------------------
THIS = Path(__file__).resolve()
TOOLS_ROOT = THIS.parent
PROJECT_ROOT = TOOLS_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

# ------------------------------------------------------------
# 2) 引入 path_utils（路径体系核心）
# ------------------------------------------------------------
from tools.utils import path_utils as paths


# ------------------------------------------------------------
# 3) 加载语言包（docs/_langs）
# ------------------------------------------------------------
LANG_DIR = paths.ROOT / "docs" / "_langs"
sys.path.insert(0, str(LANG_DIR))

def safe_import(name):
    try:
        return __import__(name)
    except Exception:
        print(f"[WARN] 无法加载语言包 {name}")
        return None

zh_mod = safe_import("zh_cn")
en_mod = safe_import("en")


# ------------------------------------------------------------
# 4) 字段映射：中英文 fallback
# ------------------------------------------------------------
def get_field_map(module, is_en=False):

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


LANG_CONFIG = {
    "zh_cn": {
        "module": zh_mod,
        "is_en": False,
        "chapter_label_tpl": "第{no}章",
    },
    "en": {
        "module": en_mod,
        "is_en": True,
        "chapter_label_tpl": "Chapter {no}",
    },
}

# 填充字段信息
for lang, info in LANG_CONFIG.items():
    mod = info["module"]
    info["FIELD_MAP"] = get_field_map(mod, info["is_en"])
    info["LABELS"] = getattr(mod, "LABELS", {}) if mod else {}
    info["TITLE"] = getattr(mod, "PROJECT_TITLE", "AT Commands Manual")


# ------------------------------------------------------------
# 5) 字段读取（自动支持 *_en fallback）
# ------------------------------------------------------------
def get_field(row, key, fmap):

    mapped = fmap.get(key, key)

    # *_en 字段优先
    if mapped in row and str(row[mapped]).strip():
        return str(row[mapped]).strip()

    # fallback 中文
    if key in row and str(row[key]).strip():
        return str(row[key]).strip()

    return ""


# ------------------------------------------------------------
# 6) Jinja2 模板环境
# ------------------------------------------------------------
env = Environment(loader=FileSystemLoader(str(paths.common_templates())))
env.globals.update(max=max, len=len)
cmd_tmpl = env.get_template("command_page.j2")


# ------------------------------------------------------------
# 7) 主流程：生成所有 RST
# ------------------------------------------------------------
def render_all():

    cfg = paths.config
    languages = list(cfg["doc_types"]["AT"].keys())
    products = list(cfg["products"].keys())

    print("\n📘 开始生成 RST（双语 + 路径体系统一）\n")

    for lang in languages:
        lang_info = LANG_CONFIG[lang]
        fmap = lang_info["FIELD_MAP"]
        labels = lang_info["LABELS"]

        for product in products:
            print(f"\n🌍 [{lang}] {product}")

            # ---------- CSV ----------
            csv_file = paths.csv_path(lang, product) / f"at_{product}.csv"
            df = pd.read_csv(csv_file, dtype=str).fillna("")

            # ---------- rst 输出目录 ----------
            rst_root = paths.rst_source_path(product, lang)
            rst_root.mkdir(parents=True, exist_ok=True)

            # ---------- 章节分组 ----------
            chapters = []
            for chap_id, grp in df.groupby("章节", sort=True):
                chap_name = get_field(grp.iloc[0], "章节名称", fmap)
                if not chap_name:
                    chap_name = lang_info["chapter_label_tpl"].format(no=chap_id)
                chapters.append((chap_id, chap_name, grp))

            # ---------- 渲染每个章节 ----------
            for chap_id, chap_name, grp in chapters:

                chap_dir = rst_root / str(chap_id)
                chap_dir.mkdir(parents=True, exist_ok=True)

                cmd_list = []

                for _, row in grp.iterrows():
                    cmd_name = row["命令"].strip()
                    cmd_list.append(cmd_name)

                    # ---------- 多子命令类型 ----------
                    types     = [x.strip() for x in row["命令类型"].split(";")]
                    formats   = [x.strip() for x in row["命令格式"].split(";")]
                    responses = [x.strip() for x in row["响应"].split(";")]
                    examples  = [x.strip() for x in row["示例命令"].split(";")]

                    max_len = max(len(types), len(formats), len(responses), len(examples))
                    types     += [""] * (max_len - len(types))
                    formats   += [""] * (max_len - len(formats))
                    responses += [""] * (max_len - len(responses))
                    examples  += [""] * (max_len - len(examples))

                    subtypes = []
                    for i in range(max_len):
                        if formats[i]:
                            subtypes.append({
                                "type":     types[i],
                                "fmt":      formats[i],
                                "response": responses[i],
                                "example":  examples[i],
                            })

                    # ---------- 参数 JSON ----------
                    param_json = get_field(row, "参数json", fmap)
                    try:
                        parameters = json.loads(param_json) if param_json else {}
                    except:
                        parameters = {}

                    # ---------- 渲染 command.rst ----------
                    rendered = cmd_tmpl.render(
                        cmd_name=cmd_name,
                        cmd_title=get_field(row, "命令标题", fmap),
                        desc=get_field(row, "功能描述", fmap),
                        subtypes=subtypes,
                        parameters=parameters,
                        note=get_field(row, "备注", fmap),
                        response_fix=get_field(row, "响应校正", fmap),
                        labels=labels,
                    )

                    (chap_dir / f"{cmd_name}.rst").write_text(
                        rendered.strip() + "\n",
                        encoding="utf-8"
                    )

                # ---------- 章节 index.rst ----------
                chapter_index = env.from_string("""
{{ title }}
{{ "=" * title|length }}

.. toctree::
   :maxdepth: 1
   :titlesonly:
{% for c in cmds %}
   {{ c }}
{% endfor %}
""").render(title=chap_name, cmds=cmd_list)

                (chap_dir / "index.rst").write_text(chapter_index, encoding="utf-8")

            # ---------- （重要）保持源目录的 index.rst，不覆盖 ----------
            # 如果 docs/.../source/index.rst 不存在，则自动生成
            project_index = rst_root / "index.rst"
            if not project_index.exists():
                product_title = lang_info["TITLE"]
                product_chapters = [str(cid) for cid, _, _ in chapters]

                root_text = env.from_string("""
{{ title }}
{{ "=" * title|length }}

.. toctree::
   :maxdepth: 1
{% for c in chapters %}
   {{ c }}/index
{% endfor %}
""").render(title=product_title, chapters=product_chapters)

                project_index.write_text(root_text, encoding="utf-8")

    print("\n🏁 RST 已全部生成！\n")


if __name__ == "__main__":
    render_all()
