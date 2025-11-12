from csv_reader import read_csv
from render_engine import render_chapters
from parameter_parser import parse_parameters

PROJECT_NAME = "Neoway AT 命令手册"
VERSION = "v1.4"
AUTHOR = "文档工程组"
DATE = datetime.now().strftime("%Y-%m-%d")

CSV_PATH = PROJECT_ROOT / "csv-input" / "at_N706B.csv"
ROOT_DIR = PROJECT_ROOT / "docs" / "N706B" / "source"
OUTPUT_DIR = ROOT_DIR
TEMPLATE_DIR = PROJECT_ROOT / "docs" / "_common" / "templates"

df = read_csv(CSV_PATH)

chapters = render_chapters(df, OUTPUT_DIR, TEMPLATE_DIR)

# Main Index
main_rst = render_main_index(PROJECT_NAME, VERSION, AUTHOR, DATE, chapters)
(OUTPUT_DIR / "index.rst").write_text(main_rst.strip()+"\n", encoding="utf-8")
print(f"🎯 主 index.rst 生成完成 → {OUTPUT_DIR/'index.rst'}")
