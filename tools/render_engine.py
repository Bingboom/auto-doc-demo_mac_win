from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def render_chapters(df, output_dir, template_dir):
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    chapters = []
    for chap, group in df.groupby("章节", sort=True):
        chap_name = group["章节名称"].iloc[0].strip() or f"第{chap}章"
        chapters.append((chap, chap_name, group))
        chapter_dir = output_dir / str(chap)
        chapter_dir.mkdir(parents=True, exist_ok=True)
        render_chapter_content(group, chapter_dir, env)
    return chapters

def render_chapter_content(group, chapter_dir, env):
    cmd_list = []
    for _, row in group.iterrows():
        cmd_name = row["命令"].strip()
        cmd_title = row["命令标题"].strip()
        cmd_list.append(cmd_name)
        rendered = render_command(row, cmd_name, cmd_title, env)
        (chapter_dir / f"{cmd_name}.rst").write_text(rendered.strip()+"\n", encoding="utf-8")
    return cmd_list

def render_command(row, cmd_name, cmd_title, env):
    cmd_tmpl = env.get_template("command_page.j2")
    return cmd_tmpl.render(
        cmd_name=cmd_name,
        cmd_title=cmd_title,
        desc=row.get("功能描述",""),
        subtypes=[],  # Example structure
        parameters={},  # Example structure
        note=row.get("备注", ""),
    )
