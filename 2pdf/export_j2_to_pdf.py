from pathlib import Path
from weasyprint import HTML, CSS
from datetime import datetime
from PyPDF2 import PdfMerger
import re, math, tempfile, time

# ============================================================
# ⚙️ 基本配置
# ============================================================
TARGET_DIR = Path("code2pdf/docs/_common/templates")   # ✅ 只导出此目录
OUTPUT_PDF = "code2pdf_templates.pdf"
BATCH_SIZE = 20  # 每批渲染文件数

root = TARGET_DIR.resolve()
gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============================================================
# 🎨 样式（Jinja 模板专用）
# ============================================================
STYLE = f"""
@page {{
    size: A4;
    margin: 15mm 12mm 15mm 12mm;
    @top-center {{
        content: "📘 {root.name} 模板导出";
        font-size: 10px;
        color: #3a4a5a;
    }}
    @bottom-center {{
        content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
        font-size: 10px;
        color: #3a4a5a;
    }}
}}
body {{
  font-family: "PingFang SC", "Segoe UI", monospace;
  background: #fcfdff;
  color: #1c1c1c;
  font-size: 12px;
  line-height: 1.55;
  padding: 0 20px;
}}
h2.file-title {{
  background: linear-gradient(90deg, #4e73df, #2e59d9);
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  margin-top: 25px;
  font-size: 14px;
  font-family: "Menlo", monospace;
}}
pre {{
  background: #f8fafc;
  border-left: 4px solid #4e73df;
  padding: 10px 14px;
  border-radius: 6px;
  font-family: "Menlo", "Consolas", monospace;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-wrap: anywhere;
  font-size: 11.5px;
  text-align: left;
}}
.kw {{ color: #d73a49; font-weight: 600; }}
.fn {{ color: #005cc5; }}
.str {{ color: #22863a; }}
.cm {{ color: #6a737d; font-style: italic; }}
.tag {{ color: #b000b0; font-weight: 600; }}
.num {{ color: #b07d00; }}
"""

# ============================================================
# 🧩 高亮函数（支持 Jinja2 模板）
# ============================================================
def highlight_j2(text: str) -> str:
    """轻量语法高亮：识别 {{ }}、{% %}、# 注释"""
    # 注释
    text = re.sub(r"(?m)({#.*?#})", r"<span class='cm'>\1</span>", text)
    # Jinja2 表达式块 {{ ... }}
    text = re.sub(r"(\{\{.*?\}\})", r"<span class='tag'>\1</span>", text)
    # 控制块 {% ... %}
    text = re.sub(r"(\{%.*?%\})", r"<span class='kw'>\1</span>", text)
    # 字符串
    text = re.sub(r"('[^']*'|\"[^\"]*\")", r"<span class='str'>\1</span>", text)
    # 数字
    text = re.sub(r"(?<![a-zA-Z])([0-9]+)(?![a-zA-Z])", r"<span class='num'>\1</span>", text)
    return text

# ============================================================
# 📁 扫描目标目录
# ============================================================
if not root.exists():
    print(f"❌ 目录不存在: {root}")
    exit(1)

included_files = [p for p in sorted(root.rglob("*.j2")) if p.is_file()]
if not included_files:
    print("⚠️ 未找到任何 .j2 模板文件")
    exit(0)

print(f"📘 收录 {len(included_files)} 个模板文件于 {root}")

# ============================================================
# 🧾 分批生成 PDF
# ============================================================
temp_files = []
start_time = time.time()

for batch_i in range(math.ceil(len(included_files) / BATCH_SIZE)):
    batch = included_files[batch_i * BATCH_SIZE:(batch_i + 1) * BATCH_SIZE]
    html_parts = [f"<html><head><meta charset='utf-8'><style>{STYLE}</style></head><body>"]

    for p in batch:
        text = p.read_text(encoding="utf-8", errors="ignore")
        text = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
        text = highlight_j2(text)
        html_parts.append(f"<h2 class='file-title'>{p.relative_to(root)}</h2><pre>{text}</pre>")

    html_parts.append("</body></html>")
    html_string = "\n".join(html_parts)

    part_pdf = Path(tempfile.gettempdir()) / f"j2_part_{batch_i+1}.pdf"
    print(f"🧩 生成分卷 {batch_i+1}/{math.ceil(len(included_files)/BATCH_SIZE)} → {part_pdf}")
    HTML(string=html_string).write_pdf(part_pdf, stylesheets=[CSS(string=STYLE)])
    temp_files.append(part_pdf)

# ============================================================
# 🪄 合并总 PDF
# ============================================================
print("🧷 正在合并 PDF ...")
merger = PdfMerger()
for part in temp_files:
    merger.append(str(part))
merger.write(OUTPUT_PDF)
merger.close()

print(f"✅ 完成！输出文件：{OUTPUT_PDF}")
print(f"⏱️ 总耗时：{time.time() - start_time:.1f} 秒")
