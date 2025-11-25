# ============================================================
# render_rst.py — Intro CN/EN + Timeout + Appendix A–G (Fixed Template Paths)
# ============================================================

from pathlib import Path
import sys, json
import pandas as pd
from jinja2 import Environment, FileSystemLoader

# ------------------------------------------------------------
# 1) inject search paths
# ------------------------------------------------------------
THIS = Path(__file__).resolve()
TOOLS_ROOT = THIS.parent
PROJECT_ROOT = TOOLS_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

# ------------------------------------------------------------
# 2) unified path system
# ------------------------------------------------------------
from tools.utils import path_utils as paths

# ------------------------------------------------------------
# 3) load language packs
# ------------------------------------------------------------
LANG_DIR = paths.langs_dir()
sys.path.insert(0, str(LANG_DIR))

def safe_import(lang):
    try:
        return __import__(lang)
    except:
        return None

zh_mod = safe_import("zh_cn")
en_mod = safe_import("en")

# ------------------------------------------------------------
# 4) field mapping
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
    "zh_cn": {"module": zh_mod, "is_en": False, "chapter_label_tpl": "第{no}章"},
    "en":    {"module": en_mod, "is_en": True,  "chapter_label_tpl": "Chapter {no}"},
}

for lang, info in LANG_CONFIG.items():
    mod = info["module"]
    info["FIELD_MAP"]  = get_field_map(mod, info["is_en"])
    info["LABELS"]     = getattr(mod, "LABELS", {}) if mod else {}
    info["TITLE"]      = getattr(mod, "PROJECT_TITLE", "AT Commands Manual")


# ------------------------------------------------------------
# 5) field getter
# ------------------------------------------------------------
def get_field(row, key, fmap):
    mapped = fmap.get(key, key)
    if mapped in row and str(row[mapped]).strip():
        return str(row[mapped]).strip()
    if key in row and str(row[key]).strip():
        return str(row[key]).strip()
    return ""


# ------------------------------------------------------------
# 6) templates loader  (only use paths.common_templates)
# ------------------------------------------------------------
env = Environment(loader=FileSystemLoader(str(paths.common_templates())))
env.globals.update(max=max, len=len)

# command page template
cmd_tmpl = env.get_template("command_page.j2")

# intro templates loader
def load_intro_template(base, lang):
    name = f"{base}.j2" if lang == "zh_cn" else f"{base}_en.j2"
    return env.get_template(name)

# appendix template loader  (目录不再使用 f"appendix/xxx")
def load_appendix_template(name):
    return env.get_template(name)


# ------------------------------------------------------------
# 7) main render
# ------------------------------------------------------------
def render_all():

    cfg = paths.config
    languages = list(cfg["doc_types"]["AT"].keys())
    products  = list(cfg["products"].keys())

    print("\n📘 Generating RST (Intro + Timeout + Appendix A–G)\n")

    for lang in languages:
        info  = LANG_CONFIG[lang]
        fmap  = info["FIELD_MAP"]
        labels = info["LABELS"]

        for product in products:

            print(f"\n🌍 [{lang}] {product}")

            csv_path = paths.csv_path(lang, product) / f"at_{product}.csv"
            df = pd.read_csv(csv_path, dtype=str).fillna("")

            rst_root = paths.rst_source_path(product, lang)
            rst_root.mkdir(parents=True, exist_ok=True)

            intro_dir = rst_root / "intro"
            intro_dir.mkdir(exist_ok=True)

            intro1_tmpl = load_intro_template("intro_ch1", lang)
            (intro_dir / "1_intro_log.rst").write_text(
                intro1_tmpl.render(labels=labels),
                encoding="utf-8"
            )

            timeout_csv = paths.csv_path(lang, product) / "intro_timeout.csv"
            if not timeout_csv.exists():
                timeout_csv = paths.csv_path("zh_cn", product) / "intro_timeout.csv"

            timeout_rows = []
            if timeout_csv.exists():
                df_t = pd.read_csv(timeout_csv, dtype=str).fillna("")
                for _, r in df_t.iterrows():
                    timeout_rows.append({
                        "no":      r.get("No.", r.get("no", "")),
                        "cmd":     r.get("命令", r.get("Command", "")),
                        "timeout": r.get("超时_s", r.get("Timeout_s", "")),
                    })

            intro2_tmpl = load_intro_template("intro_ch2", lang)
            (intro_dir / "2_intro_syntax.rst").write_text(
                intro2_tmpl.render(labels=labels, timeout_rows=timeout_rows),
                encoding="utf-8"
            )

            chapters = []
            for chap_id, grp in df.groupby("章节", sort=True):
                chap_name = get_field(grp.iloc[0], "章节名称", fmap)
                if not chap_name:
                    chap_name = info["chapter_label_tpl"].format(no=chap_id)
                chapters.append((chap_id, chap_name, grp))

            for chap_id, chap_name, grp in chapters:
                chap_dir = rst_root / str(chap_id)
                chap_dir.mkdir(exist_ok=True)

                cmd_list = []

                for _, row in grp.iterrows():
                    cmd_name = row["命令"].strip()
                    cmd_list.append(cmd_name)

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
                                "type": types[i],
                                "fmt": formats[i],
                                "response": responses[i],
                                "example": examples[i],
                            })

                    param_raw = get_field(row, "参数json", fmap)
                    try:
                        parameters = json.loads(param_raw) if param_raw else {}
                    except:
                        parameters = {}

                    rendered = cmd_tmpl.render(
                        cmd_name   = cmd_name,
                        cmd_title  = get_field(row, "命令标题", fmap),
                        desc       = get_field(row, "功能描述", fmap),
                        subtypes   = subtypes,
                        parameters = parameters,
                        note       = get_field(row, "备注", fmap),
                        response_fix = get_field(row, "响应校正", fmap),
                        labels=labels,
                    )

                    (chap_dir / f"{cmd_name}.rst").write_text(
                        rendered + "\n", encoding="utf-8"
                    )

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


            # ====================================================
            # ⑦ 附录（修复模板路径）
            # ====================================================
            appendix_dir_csv = paths.csv_path(lang, product) / "appendix"
            appendix_dir_rst = rst_root / "appendix"
            appendix_dir_rst.mkdir(exist_ok=True)

            appendix_map = {
                "A_error_codes.csv": ("appendix_A.j2", "附录 A 错误码说明" if lang=="zh_cn" else "Appendix A Error Codes"),
                "B_atv.csv": ("appendix_B.j2", "附录 B ATV 命令集" if lang=="zh_cn" else "Appendix B ATV Commands"),
                "C_band_list.csv": ("appendix_C.j2", "附录 C 频段列表" if lang=="zh_cn" else "Appendix C Band List"),
                "D_result_codes.csv": ("appendix_D.j2", "附录 D 结果码" if lang=="zh_cn" else "Appendix D Result Codes"),
                "E_cme_cms_errors.csv": ("appendix_E1.j2", "附录 E1 CME/CMS 错误码" if lang=="zh_cn" else "Appendix E1 CME/CMS Errors"),
                "E_custom_errors.csv": ("appendix_E2.j2", "附录 E2 自定义错误码" if lang=="zh_cn" else "Appendix E2 Custom Errors"),
                "F_urc.csv": ("appendix_F.j2", "附录 F URC 列表" if lang=="zh_cn" else "Appendix F URCs"),
                "G_reference.csv": ("appendix_G.j2", "附录 G 参考资料" if lang=="zh_cn" else "Appendix G Reference"),
            }

            appendix_pages = []

            for csv_name, (tmpl_name, title) in appendix_map.items():
                csv_file = appendix_dir_csv / csv_name
                if not csv_file.exists():
                    continue

                df_app = pd.read_csv(csv_file, dtype=str, encoding="utf-8-sig", engine="python").fillna("")
                headers = list(df_app.columns)
                rows = df_app.values.tolist()

                tmpl = load_appendix_template(tmpl_name)
                out_text = tmpl.render(
                    title=title,
                    headers=headers,
                    rows=rows,
                    labels=labels
                )

                out_path = appendix_dir_rst / f"{csv_name.replace('.csv','')}.rst"
                out_path.write_text(out_text, encoding="utf-8")
                appendix_pages.append(out_path.stem)

            (appendix_dir_rst / "index.rst").write_text(
                env.from_string("""
附录
====
.. toctree::
   :maxdepth: 1
{% for p in pages %}
   {{ p }}
{% endfor %}
""").render(pages=appendix_pages),
                encoding="utf-8"
            )

            # root index
            root_index = rst_root / "index.rst"
            root_index.write_text(
                env.from_string("""
{{ title }}
{{ "=" * title|length }}

.. toctree::
   :maxdepth: 1

   intro/1_intro_log
   intro/2_intro_syntax

{% for c in chapters %}
   {{ c }}/index
{% endfor %}

   appendix/index
""").render(title=info["TITLE"], chapters=[str(cid) for cid, _, _ in chapters]),
                encoding="utf-8"
            )

    print("\n🏁 DONE — Intro CN/EN + Timeout + Appendix A–G 完成构建！\n")


if __name__ == "__main__":
    render_all()
