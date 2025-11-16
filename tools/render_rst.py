# tools/render_rst.py
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path
import json
import sys
import yaml

# 加载 config.yaml 配置文件
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 获取配置
config = load_config()

# === 自动加入项目根目录 ===
ROOT = Path(config['root']).resolve()  # 确保 ROOT 是实际路径
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 使用 config.yaml 中的路径设置
PROJECT_NAME = "Neoway AT 命令手册"
VERSION = "v1.4"
AUTHOR = "文档工程组"
DATE = datetime.now().strftime("%Y-%m-%d")

# 获取产品线配置
product_line = config['default_product_line']

# 从 config.yaml 中读取路径
PROJECT_ROOT = Path(config['root']).resolve()
CSV_PATH = Path(config['csv_input']) / "at_N706B.csv"  # 获取 CSV 路径

# 获取产品线的路径配置
ROOT_DIR = Path(config['product_lines'][product_line]['rst_source']).resolve()  # 获取文档源路径
OUTPUT_DIR = Path(config['product_lines'][product_line]['build_pdf']).resolve()  # 获取输出目录路径
TEMPLATE_DIR = Path(config['templates']).resolve()  # 获取模板目录路径

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))  # 加载 Jinja2 模板
env.globals.update(max=max, min=min, len=len)

# === ★★★ 修复 metadata 的主 index 模板（其他不变） ★★★
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

cmd_tmpl = env.get_template("command_page.j2")  # 获取命令模板

# === 读取CSV ===
df = pd.read_csv(CSV_PATH, dtype=str).fillna("")

# === 分章渲染 ===
chapters = []
for chap, group in df.groupby("章节", sort=True):
    chap_name = group["章节名称"].iloc[0].strip() or f"第{chap}章"
    chapters.append((chap, chap_name, group))

for chap_num, chap_name, group in chapters:
    chap_dir = OUTPUT_DIR / str(chap_num)
    chap_dir.mkdir(parents=True, exist_ok=True)

    cmd_list = []
    for _, row in group.iterrows():
        cmd_name  = row["命令"].strip()
        cmd_title = row["命令标题"].strip()
        cmd_list.append(cmd_name)

        types    = [t.strip() for t in str(row.get('命令类型', '')).split(';') if t.strip()!='']
        formats  = [t.strip() for t in str(row.get('命令格式', '')).split(';')]
        raw_corr = str(row.get('响应校正', '')).strip().strip("'''")
        if raw_corr:
            responses = [t.strip() for t in raw_corr.split(';')]
        else:
            responses = [t.strip() for t in str(row.get('响应', '')).split(';')]
        examples = [t.strip() for t in str(row.get('示例命令', '')).split(';')]

        max_len = max(len(types), len(formats), len(responses), len(examples))
        if len(types) < max_len:
            types = types + [""] * (max_len - len(types))

        subtypes = []
        for i in range(max_len):
            st = {
                "type":     types[i]     if i < len(types)     else "",
                "fmt":      formats[i]   if i < len(formats)   else "",
                "response": responses[i] if i < len(responses) else "",
                "example":  examples[i]  if i < len(examples)  else "",
            }
            if st["fmt"]:
                subtypes.append(st)

        try:
            parameters = json.loads(row.get('参数json', '{}'))
        except Exception:
            parameters = {}
        if isinstance(parameters, list):
            pdict = {}
            for p in parameters:
                name   = (p.get('name') or '').strip()
                desc   = (p.get('desc') or '').strip()
                valmap = p.get('valmap', {}) or {}
                if name:
                    pdict[name] = {'__desc__': desc}
                    for k, v in valmap.items():
                        pdict[name][str(k)] = v
            parameters = pdict

        rendered = cmd_tmpl.render(
            cmd_name=cmd_name,
            cmd_title=cmd_title,
            desc=row.get("功能描述",""),
            subtypes=subtypes,
            parameters=parameters,
            note=row.get("备注", ""),
        )
        (chap_dir / f"{cmd_name}.rst").write_text(rendered.strip()+"\n", encoding="utf-8")
        print(f"✅ 已生成命令：{cmd_name}")

    idx_render = chapter_index_tmpl.render(chap_num=chap_num, chap_name=chap_name, cmds=cmd_list)
    (chap_dir / "index.rst").write_text(idx_render.strip()+"\n", encoding="utf-8")
    print(f"📘 第{chap_num}章 {chap_name} 生成完成（{len(cmd_list)} 条命令）")

# 主 index
main_rst = main_index_tmpl.render(
    project_name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    date=DATE,
    chapters=chapters
)
(OUTPUT_DIR / "index.rst").write_text(main_rst.strip()+"\n", encoding="utf-8")
print(f"🎯 主 index.rst 生成完成 → {OUTPUT_DIR/'index.rst'}")
