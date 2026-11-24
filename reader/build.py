"""Build the complete reader from the canonical manuscripts using standard Python."""
from html import escape
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "异星录" / "正文"
OUT = ROOT / "dist"
TITLE = "异星录：断阶之城"


def link(url, label):
    return f'<a href="{url}">{escape(label)}</a>'


def page(filename, title, content):
    html = f"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · 异星录</title><link rel="stylesheet" href="style.css">
<header>{link('index.html', TITLE)}</header><main>{content}</main>
<footer>小说免费阅读，欢迎分享链接。商业使用须另行取得授权，法律另有规定或已有有效授权的除外。</footer></html>"""
    (OUT / filename).write_text(html, encoding="utf-8")


def build():
    volumes = []
    chapters = []
    for volume_id, numeral in enumerate("一二三四五六七八", 1):
        directory, = BOOK.glob(f"第{numeral}卷_*")
        volume_title = directory.name.replace("_", "　")
        files = sorted(directory.glob("第*章_*.md"))
        numbers = [int(p.name.split("章")[0][1:]) for p in files]
        if numbers != list(range(100 * (volume_id - 1) + 1, 100 * volume_id + 1)):
            raise ValueError(f"{volume_title} 章号重复或缺失")
        if volume_id == 1:
            prologue, = directory.glob("楔子_*.md")
            files.insert(0, prologue)
        start = len(chapters)
        for path in files:
            heading, _, body = path.read_text(encoding="utf-8").strip().partition("\n")
            if not heading.startswith("# ") or not body.strip():
                raise ValueError(f"正文标题或内容缺失：{path}")
            chapters.append((heading[2:].strip(), body, volume_id))
        volumes.append((volume_title, start, len(chapters)))

    OUT.mkdir(exist_ok=True)
    shutil.copyfile(Path(__file__).with_name("style.css"), OUT / "style.css")
    volume_links = []
    for volume_id, (name, start, end) in enumerate(volumes, 1):
        filename = f"volume-{volume_id}.html"
        volume_links.append(f"<li>{link(filename, name)}</li>")
        items = "".join(f"<li>{link(f'ch-{i:03}.html', chapters[i][0])}</li>" for i in range(start, end))
        page(filename, name, f"<h1>{escape(name)}</h1><ul>{items}</ul>")
    for i, (title, body, volume_id) in enumerate(chapters):
        nav = []
        if i:
            nav.append(link(f"ch-{i-1:03}.html", "上一章"))
        nav.append(link(f"volume-{volume_id}.html", "本卷目录"))
        if i + 1 < len(chapters):
            nav.append(link(f"ch-{i+1:03}.html", "下一章"))
        paragraphs = ["<hr>" if p.strip() == "***" else f"<p>{escape(p.strip())}</p>"
                      for p in re.split(r"\n\s*\n", body.strip())]
        volume = volumes[volume_id-1][0]
        page(f"ch-{i:03}.html", title, f"<p>{link(f'volume-{volume_id}.html', volume)}</p>"
             f"<h1>{escape(title)}</h1><article>{''.join(paragraphs)}</article>"
             f"<nav aria-label=\"章节导航\">{''.join(nav)}</nav>")
    page("index.html", TITLE, f"<h1>{TITLE}</h1><p>岚岬的海越来越热。栈城第七码头的水工林渡还要给三户人家送水，脚下的木板已经开始下沉。</p>"
         f"<nav>{link('ch-000.html','从楔子读起')}{link('ch-001.html','读第一章')}</nav>"
         f"<h2>全八卷 · 完结</h2><ul class=\"volumes\">{''.join(volume_links)}</ul>")
    print(f"生成 {len(chapters)} 篇正文、{len(volumes)} 个分卷目录和首页 → {OUT}")


if __name__ == "__main__":
    build()
