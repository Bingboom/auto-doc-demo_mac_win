# ============================================================
# render_rst.py — Final Stable Version (No Hardcoded Paths)
# 全路径统一使用 path_utils（语言包也走 config.yaml + path_utils）
# ============================================================

"""
功能：
    1) 将 CSV 自动转换为 RST（产品 × 语言）
    2) 多子命令类型 Execute / Query / Test / Set
    3) *_en 字段 fallback
    4) 自动生成章节 index.rst
    5) 自动生成项目 index.rst（如不存在）
    6) 不允许任何硬编码路径
"""

from pathlib import Path
import sys, json
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------
# 1) 注入搜索路径（必须先于 import path_utils）
# ------------------------------------------------------------
THIS = Path(__file__).resolve()
TOOLS_ROOT = THIS.parent
PROJECT_ROOT = TOOLS_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

# ------------------------------------------------------------
# 2) path_utils（统一路径体系核心）
# ------------------------------------------------------------
from tools.utils import path_utils as paths


# ------------------------------------------------------------
# 3) 加载语言包路径（来自 config.yaml，而不是硬编码）
# ------------------------------------------------------------
LANG_DIR = paths.langs_dir()   # <—— 完全改为 path_utils 提供

sys.path.insert(0, str(LANG_DIR))

def safe_import(lang):
    try:
        return __import__(lang)
    except Exception as e:
        print(f"[WARN] 无法加载语言包 {lang}: {e}")
        return None


zh_mod = safe_import("zh_cn")
en_mod = safe_import("en")


# ------------------------------------------------------------
# 4) 字段映射规则（支持 *_en fallback）
# ------------------------------------------------------------
def get_field_map(module, is_en=False):

    # 语言包自己定义 FIELD_MAP（最高优先级）
    if module and hasattr(module, "FIELD_MAP"):
        return module.FIELD_MAP

    # 自动 fallback
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


# 语言配置
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

# 语言包补全
for lang, info in LANG_CONFIG.items():
    mod = info["module"]
    info["FIELD_MAP"] = get_field_map(mod, info["is_en"])
    info["LABELS"] = getattr(mod, "LABELS", {}) if mod else {}
    info["TITLE"] = getattr(mod, "PROJECT_TITLE", "AT Commands Manual")


# ------------------------------------------------------------
# 5) 字段获取（支持英文优先）
# ------------------------------------------------------------
def get_field(row, key, fmap):
    mapped_key = fmap.get(key, key)

    if mapped_key in row and str(row[mapped_key]).strip():
        return str(row[mapped_key]).strip()

    if key in row and str(row[key]).strip():
        return str(row[key]).strip()

    return ""


# ------------------------------------------------------------
# 6) Jinja2 模板（路径同样来自 path_utils）
# ------------------------------------------------------------
env = Environment(loader=FileSystemLoader(str(paths.common_templates())))
env.globals.update(max=max, len=len)
cmd_tmpl = env.get_template("command_page.j2")


# ------------------------------------------------------------
# 7) 主流程
# ------------------------------------------------------------
def render_all():

    cfg = paths.config
    languages = list(cfg["doc_types"]["AT"].keys())
    products = list(cfg["products"].keys())

    print("\n📘 开始生成 RST（完全统一路径体系）\n")

    for lang in languages:
        lang_info = LANG_CONFIG[lang]
        fmap = lang_info["FIELD_MAP"]
        labels = lang_info["LABELS"]

        for product in products:

            print(f"\n🌍 [{lang}] {product}")

            # ① 获取 CSV
            csv_path = paths.csv_path(lang, product) / f"at_{product}.csv"
            df = pd.read_csv(csv_path, dtype=str).fillna("")

            # ② 输出 rst 根目录
            rst_root = paths.rst_source_path(product, lang)
            rst_root.mkdir(parents=True, exist_ok=True)

            # ③ 分章节
            chapters = []
            for chap_id, grp in df.groupby("章节", sort=True):
                chap_name = get_field(grp.iloc[0], "章节名称", fmap)

                if not chap_name:
                    chap_name = lang_info["chapter_label_tpl"].format(no=chap_id)

                chapters.append((chap_id, chap_name, grp))

            # ④ 渲染章节
            for chap_id, chap_name, grp in chapters:

                chap_dir = rst_root / str(chap_id)
                chap_dir.mkdir(parents=True, exist_ok=True)

                cmd_list = []

                for _, row in grp.iterrows():
                    cmd_name = row["命令"].strip()
                    cmd_list.append(cmd_name)

                    # 子命令拆分
                    types = [x.strip() for x in row["命令类型"].split(";")]
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
                    param_raw = get_field(row, "参数json", fmap)
                    try:
                        parameters = json.loads(param_raw) if param_raw else {}
                    except:
                        parameters = {}

                    # 渲染 rst
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

                # 章节 index.rst
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

            # ⑤ 根 index.rst（仅在不存在时创建）
            root_index = rst_root / "index.rst"
            if not root_index.exists():
                root_index.write_text(
                    env.from_string("""
{{ title }}
{{ "=" * title|length }}

.. toctree::
   :maxdepth: 1
{% for c in chapters %}
   {{ c }}/index
{% endfor %}
""").render(
                        title=lang_info["TITLE"],
                        chapters=[str(cid) for cid, _, _ in chapters]
                    ),
                    encoding="utf-8"
                )

    print("\n🏁 RST 生成完成（无硬编码路径）！\n")


if __name__ == "__main__":
    render_all()
