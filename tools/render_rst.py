# tools/render_rst.py

import sys
import json
import yaml
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path

# ============================================================
# 🔧 全局路径体系（统一从 path_utils 获取）
# ============================================================
from utils.path_utils import (
    csv_path,
    rst_source_path,
    common_templates,
    get_default_product,
)


# ============================================================
# 🔧 加载统一配置（不再在此做路径）
# ============================================================
def load_config():
    with open("config.yaml", "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


config = load_config()

PRODUCT = get_default_product()

# 工程属性
PROJECT_NAME = "Neoway AT 命令手册"
VERSION = "v1.4"
AUTHOR = "文档工程组"
DATE = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# 🔧 关键路径（来自 path_utils）
# ============================================================
CSV_DIR = csv_path(PRODUCT)
CSV_FILE = CSV_DIR / "at_{}.csv".format(PRODUCT)

RST_OUT_DIR = rst_source_path(PRODUCT)
TEMPLATE_DIR = common_templates()

RST_OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 🔧 Jinja2 模板加载
# ============================================================
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
env.globals.update(max=max, min=min, len=len)

# 主 index 模板
main_index_tmpl = env.from_string("""
{{ project_name }} {{ version }}
{{ "=" * (project_name|length + version|length + 1) }}

.. Author: {{ author }}
.. Date: {{ date }}
.. Version: {{ version }}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for chap in chapters %}
   {{ chap[0] }}/index
{% endfor %}

附录
----
.. toctree::
   :maxdepth: 1
   :titlesonly:

   appendix/abbreviations
   appendix/index
""".strip())

# 章节 index 模板
chapter_index_tmpl = env.from_string("""
{{ chap_name }}
{{ "=" * max((chap_name|length + 2), 10) }}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for cmd in cmds %}
   {{ cmd }}
{% endfor %}
""".strip())

# 命令模板
cmd_tmpl = env.get_template("command_page.j2")


# ============================================================
# 🔧 读取 CSV
# ============================================================
print(f"📥 正在读取 CSV: {CSV_FILE}")
df = pd.read_csv(CSV_FILE, dtype=str).fillna("")

# ============================================================
# 🔧 按章节生成 RST
# ============================================================
chapters = []

for chap_id, grp in df.groupby("章节", sort=True):
    chap_name = grp["章节名称"].iloc[0].strip() or f"第{chap_id}章"
    chapters.append((chap_id, chap_name, grp))

for chap_id, chap_name, grp in chapters:

    chap_dir = RST_OUT_DIR / str(chap_id)
    chap_dir.mkdir(parents=True, exist_ok=True)

    cmd_list = []

    for _, row in grp.iterrows():

        cmd_name = row["命令"].strip()
        cmd_title = row["命令标题"].strip()
        cmd_list.append(cmd_name)

        # ---- 解析命令类型/格式/响应/示例 ----
        types = [t.strip() for t in str(row.get("命令类型", "")).split(";") if t.strip()]
        formats = [t.strip() for t in str(row.get("命令格式", "")).split(";")]

        raw_corr = str(row.get("响应校正", "")).strip().strip("'''")
        if raw_corr:
            responses = [t.strip() for t in raw_corr.split(";")]
        else:
            responses = [t.strip() for t in str(row.get("响应", "")).split(";")]

        examples = [t.strip() for t in str(row.get("示例命令", "")).split(";")]

        max_len = max(len(types), len(formats), len(responses), len(examples))
        types += [""] * (max_len - len(types))
        formats += [""] * (max_len - len(formats))
        responses += [""] * (max_len - len(responses))
        examples += [""] * (max_len - len(examples))

        subtypes = []
        for i in range(max_len):
            fmt = formats[i]
            if fmt:
                subtypes.append({
                    "type": types[i],
                    "fmt": fmt,
                    "response": responses[i],
                    "example": examples[i],
                })

        # ---- 解析参数 JSON ----
        try:
            parameters = json.loads(row.get("参数json", "{}"))
        except:
            parameters = {}

        if isinstance(parameters, list):
            param_dict = {}
            for p in parameters:
                name = (p.get("name") or "").strip()
                desc = (p.get("desc") or "").strip()
                valmap = p.get("valmap", {}) or {}
                if name:
                    param_dict[name] = {"__desc__": desc, **{str(k): v for k, v in valmap.items()}}
            parameters = param_dict

        # ---- 渲染命令页 ----
        rendered = cmd_tmpl.render(
            cmd_name=cmd_name,
            cmd_title=cmd_title,
            desc=row.get("功能描述", ""),
            subtypes=subtypes,
            parameters=parameters,
            note=row.get("备注", ""),
        )

        (chap_dir / f"{cmd_name}.rst").write_text(
            rendered.strip() + "\n", encoding="utf-8"
        )

        print(f"  ✔ 已生成命令：{cmd_name}")

    # ---- 渲染章节 index ----
    idx_rst = chapter_index_tmpl.render(
        chap_name=chap_name,
        cmds=cmd_list
    )

    (chap_dir / "index.rst").write_text(idx_rst.strip() + "\n", encoding="utf-8")

    print(f"📘 第{chap_id}章《{chap_name}》生成完成（{len(cmd_list)} 条命令）")


# ============================================================
# 🔧 生成主 index.rst
# ============================================================
main_rst = main_index_tmpl.render(
    project_name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    date=DATE,
    chapters=chapters,
)

(RST_OUT_DIR / "index.rst").write_text(main_rst.strip() + "\n", encoding="utf-8")

print(f"\n🎯 主 index.rst 生成完成 → {RST_OUT_DIR/'index.rst'}")
print("🏁 全部 RST 内容已生成完毕！")
