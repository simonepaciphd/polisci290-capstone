"""Refresh resource pages, downloads, and embedded download copies.

Maintainers: requires markdown-it-py and beautifulsoup4. From the repo root:
    python tools/build-resources.py
The original weekly workflow HTML is preserved. Students do not run this tool.
"""

import base64
import io
import json
import posixpath
import re
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
PAGE_PATHS = {
    "overview": "polisci290-00-project-overview.md",
    "how-to-use": "polisci290-README.md",
    **{f"wf-{p.name.split('-')[1]}": p.relative_to(ROOT).as_posix()
       for p in sorted((ROOT / "workflows").glob("*.md"))},
    "formats": "docs/polisci290-capstone-formats.md",
    "rubrics": "docs/polisci290-rubrics.md",
    "ai-use": "docs/polisci290-ai-use-and-disclosure.md",
    "agentic-ai": "docs/polisci290-agentic-ai.md",
}
PAGE_IDS = {path: page_id for page_id, path in PAGE_PATHS.items()}


def archive(entries):
    """Stable bytes: unchanged sources produce unchanged ZIPs."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, content)
    return buffer.getvalue()


def render_page(page_id, path):
    source = (ROOT / path).read_text(encoding="utf-8")
    html = MarkdownIt("commonmark").enable("table").render(source)
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        slug = re.sub(r"[^\w\s-]", "", heading.get_text().lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        heading_id = f"{page_id}-{slug}"
        while heading_id in seen:
            heading_id += "-2"
        heading["id"] = heading_id
        seen.add(heading_id)
    for link in soup.select("a[href]"):
        url = urlsplit(link["href"])
        if url.scheme or url.netloc or not url.path:
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), url.path))
        if target in PAGE_IDS:
            target_id = PAGE_IDS[target]
            link["href"] = f"#{target_id}-{url.fragment}" if url.fragment else f"#{target_id}"
        elif (ROOT / target).is_dir():
            # GitHub renders directory listings; GitHub Pages does not.
            link["href"] = "https://github.com/simonepaciphd/polisci290-capstone/tree/main/" + target
        else:
            link["href"] = target + (f"#{url.fragment}" if url.fragment else "")
    for table in soup.select("table"):
        labels = [cell.get_text() for cell in table.select("thead th")]
        for row in table.select("tbody tr"):
            for label, cell in zip(labels, row.select("td")):
                cell["data-label"] = label
    button = (f'<p class="page-tools" hidden=""><button class="btn" '
              f'data-download="{page_id}" type="button">Download this page for your AI (.md)</button>'
              '<span aria-live="polite" class="note"></span></p>')
    content = str(soup)
    content = content.replace("</h1>", "</h1>" + button, 1)
    return f'<section class="page" id="{page_id}">\n{content}\n</section>'


def main():
    starter = {p.relative_to(ROOT).as_posix(): p.read_bytes()
               for p in (ROOT / "replication-starter").rglob("*") if p.is_file()}
    starter_zip = archive(starter)
    (ROOT / "replication-starter.zip").write_bytes(starter_zip)
    files = {f"final-project/{path}": (ROOT / path).read_bytes()
             for path in PAGE_PATHS.values()}
    files.update({f"final-project/{name}": data for name, data in starter.items()})
    files["final-project/replication-starter.zip"] = starter_zip
    package = archive(files)
    (ROOT / "polisci290-capstone-package.zip").write_bytes(package)

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for page_id in ("how-to-use", "ai-use", "agentic-ai"):
        section = render_page(page_id, PAGE_PATHS[page_id])
        pattern = rf'<section class="page" id="{page_id}">.*?</section>'
        if re.search(pattern, html, flags=re.S):
            html = re.sub(pattern, lambda _: section, html, flags=re.S)
        else:
            html = html.replace('<nav class="pager"', section + '\n<nav class="pager"', 1)
    old_link = '<li><a href="#ai-use">AI use and disclosure</a></li>'
    new_link = '<li><a href="#agentic-ai">Working with an AI agent</a></li>'
    if new_link not in html:
        html = html.replace(old_link, old_link + "\n" + new_link)
    embedded = {page_id: {"name": path.split("/")[-1],
                          "text": (ROOT / path).read_text(encoding="utf-8")}
                for page_id, path in PAGE_PATHS.items()}
    embedded["zip"] = {"name": "polisci290-capstone-package.zip",
                       "base64": base64.b64encode(package).decode("ascii")}
    # A literal closing script tag in a Markdown example must not end the JSON script.
    payload = json.dumps(embedded, ensure_ascii=False).replace("</", "<\\/")
    html = re.sub(r'(<script[^>]*id="guide-files"[^>]*>).*?(</script>)',
                  lambda m: m[1] + payload + m[2], html, flags=re.S)
    for name in ("index.html", "polisci290-capstone-guide.html"):
        (ROOT / name).write_text(html, encoding="utf-8", newline="\n")
    print(f"Built {len(starter)} starter files, {len(files)} package entries, and {len(PAGE_PATHS)} embedded pages.")


if __name__ == "__main__":
    main()
