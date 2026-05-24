from __future__ import annotations

from pathlib import Path
import html

try:
    import markdown
except ImportError:
    raise SystemExit("Install markdown: python3 -m pip install markdown")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
PAGES = [
    ("index.md", "index.html", "Home"),
    ("getting-started.md", "getting-started.html", "Getting started"),
    ("architecture.md", "architecture.html", "Architecture"),
    ("maintainer-notes.md", "maintainer-notes.html", "Maintainer notes"),
]
NAV = [
    ("index.html", "Home"),
    ("getting-started.html", "Getting started"),
    ("architecture.html", "Architecture"),
    ("maintainer-notes.html", "Maintainer notes"),
]


def render_page(src: Path, title: str) -> str:
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["fenced_code", "tables"])
    nav = " ".join(f'<a href="{html.escape(href)}">{html.escape(label)}</a>' for href, label in NAV)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{html.escape(title)} · training-manager</title>
  <link rel=\"stylesheet\" href=\"site.css\">
</head>
<body>
  <nav>{nav}</nav>
  <main>
  {body}
  </main>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "site.css").write_text((ROOT / "site.css").read_text(encoding="utf-8"), encoding="utf-8")
    for md_name, html_name, title in PAGES:
        page = render_page(ROOT / md_name, title)
        (OUT / html_name).write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
