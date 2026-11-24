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


def page(filename, title, content, body_class=""):
    html = f"""<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · 异星录</title><link rel="stylesheet" href="style.css">
<body class="{body_class}"><header>{link('index.html', TITLE)}</header><main>{content}</main>
<footer>小说免费阅读，欢迎分享链接。商业使用须另行取得授权，法律另有规定或已有有效授权的除外。</footer></body></html>"""
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
    (OUT / "assets").mkdir(exist_ok=True)
    shutil.copyfile(Path(__file__).with_name("assets") / "cover.jpg", OUT / "assets" / "cover.jpg")
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
    page("index.html", TITLE,
         '<section class="book-intro" aria-labelledby="book-title">'
         '<img class="book-cover" src="assets/cover.jpg" width="1024" height="1536" '
         'alt="《异星录：断阶之城》封面：临海木城的断裂阶梯下，两名旅人面对翻涌的海浪。" fetchpriority="high">'
         '<div class="book-summary"><p class="book-meta">废土科幻 · 群像冒险</p>'
         f'<h1 id="book-title">异星录<span>断阶之城</span></h1>'
         '<p class="book-description">岚岬的海越来越热。栈城第七码头的水工林渡还要给三户人家送水，脚下的木板已经开始下沉。</p>'
         '<p class="book-meta">全八卷 · 800章 · 已完结 · 免费阅读</p>'
         '<nav class="reading-actions" aria-label="开始阅读">'
         '<a class="read-button" href="ch-000.html">从楔子读起</a>'
         '<a href="ch-001.html">读第一章</a><a href="#volumes">浏览目录</a></nav></div></section>'
         '<section class="volume-section" aria-labelledby="volumes"><h2 id="volumes">全书目录</h2>'
         f'<ul class="volumes">{"".join(volume_links)}</ul></section>', body_class="home")
    print(f"生成 {len(chapters)} 篇正文、{len(volumes)} 个分卷目录和首页 → {OUT}")


if __name__ == "__main__":
    build()
