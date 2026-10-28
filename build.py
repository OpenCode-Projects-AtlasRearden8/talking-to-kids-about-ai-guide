#!/usr/bin/env python3
"""Build the static HTML site from docs/ markdown.

Local-first: no network access, no accounts, no analytics. The only
dependency is the Python `markdown` package (pip install markdown).

Usage:
    python3 build.py            # build site/ from docs/
    python3 build.py --check    # build, then fail on broken internal links
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "error: the 'markdown' package is required (python3 -m pip install markdown)\n"
    )
    sys.exit(1)

NAV_PAGES = [
    ("index.html", "Start Here"),
    ("01-what-ai-actually-is.html", "What AI Actually Is"),
    ("02-homework-honesty-and-school-policies.html", "Homework Honesty"),
    ("03-when-a-chatbot-feels-like-a-friend.html", "Chatbots & Friends"),
    ("04-sharing-rules-photos-names-feelings.html", "Sharing Rules"),
    ("05-spotting-a-bad-ai-interaction.html", "Bad Interactions"),
    ("06-setting-family-defaults-together.html", "Family Defaults"),
    ("07-first-account-checklist.html", "First Account"),
    ("age-band-scripts.html", "Age-Band Scripts"),
    ("family-agreement-sheet.html", "Agreement Sheet"),
    ("glossary.html", "Glossary"),
]

TITLE_SUFFIX = "Talking to Kids About AI - Asdale Dynamics, LLC"

CHECKBOX_RE = re.compile(r"^(\s*)- \[([ xX])\] (.*)$")

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<style>
  :root {{
    --ink: #1f2933; --muted: #616e7c; --accent: #1a6b5a;
    --bg: #fdfcf9; --card: #f4f6f5; --line: #e4e7eb;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
    color: var(--ink); background: var(--bg); margin: 0;
    line-height: 1.65; font-size: 18px;
  }}
  header.site, footer.site {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  header.site {{
    background: var(--card); border-bottom: 1px solid var(--line); padding: 1rem 1.2rem 0.6rem;
  }}
  header.site .brand {{
    font-weight: 700; letter-spacing: 0.01em; margin: 0 0 0.5rem;
  }}
  header.site .brand a {{ color: var(--accent); text-decoration: none; }}
  nav.pages {{ display: flex; flex-wrap: wrap; gap: 0.15rem 1.1rem; padding-bottom: 0.6rem; }}
  nav.pages a {{ color: var(--muted); text-decoration: none; font-size: 0.88rem; }}
  nav.pages a:hover, nav.pages a.here {{ color: var(--accent); text-decoration: underline; }}
  main {{ max-width: 46rem; margin: 0 auto; padding: 2rem 1.2rem 3rem; }}
  h1, h2, h3 {{ line-height: 1.25; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
  h1 {{ font-size: 1.9rem; margin: 0 0 1rem; }}
  h2 {{ font-size: 1.35rem; margin-top: 2.2rem; }}
  h3 {{ font-size: 1.08rem; margin-top: 1.6rem; }}
  a {{ color: var(--accent); }}
  blockquote {{
    margin: 1.2rem 0; padding: 0.8rem 1.1rem; background: var(--card);
    border-left: 4px solid var(--accent); border-radius: 0 6px 6px 0;
  }}
  blockquote p {{ margin: 0.3rem 0; }}
  code, pre {{
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; font-size: 0.86em;
    background: var(--card); border-radius: 4px;
  }}
  pre {{ padding: 0.8rem 1rem; overflow-x: auto; border: 1px solid var(--line); }}
  code {{ padding: 0.1em 0.35em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1.2rem 0; font-size: 0.95em; }}
  th, td {{ border: 1px solid var(--line); padding: 0.45rem 0.6rem; text-align: left; }}
  th {{ background: var(--card); }}
  input[type="checkbox"] {{ accent-color: var(--accent); transform: scale(1.25); margin-right: 0.55rem; }}
  li:has(input[type="checkbox"]) {{ list-style: none; margin: 0.45rem 0; }}
  ul:has(input[type="checkbox"]), ol:has(input[type="checkbox"]) {{ padding-left: 0.6rem; }}
  hr {{ border: none; border-top: 1px solid var(--line); margin: 2.5rem 0; }}
  footer.site {{
    border-top: 1px solid var(--line); color: var(--muted);
    padding: 1.2rem; font-size: 0.85rem; text-align: center;
  }}
  footer.site a {{ color: var(--muted); }}
  .footnote {{ font-size: 0.85rem; color: var(--muted); }}
  @media print {{
    header.site nav.pages, footer.site {{ display: none; }}
    body {{ font-size: 12pt; background: #fff; }}
    main {{ max-width: none; padding: 0; }}
    a {{ color: inherit; }}
    blockquote, th, td, pre, code {{ background: #fff; }}
    input[type="checkbox"] {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
</style>
</head>
<body>
<header class="site">
  <p class="brand"><a href="index.html">Talking to Kids About AI</a></p>
  <nav class="pages">
{nav}
  </nav>
</header>
<main>
{content}
</main>
<footer class="site">
  <p>Parent manual by Asdale Dynamics, LLC &mdash; plain-English AI education, local-first.</p>
  <p class="footnote">Copyright (c) 2026 Asdale Dynamics, LLC. Educational use only &mdash; not legal, medical, or mental-health advice.</p>
</footer>
</body>
</html>
"""


def checkbox_sub(text: str) -> str:
    """Turn GitHub-style task lists into real checkbox inputs."""
    lines = text.split("\n")
    out = []
    for line in lines:
        m = CHECKBOX_RE.match(line)
        if m:
            indent, mark, rest = m.groups()
            checked = " checked" if mark.strip() else ""
            out.append(f"{indent}- <input type=\"checkbox\"{checked}>{rest}")
        else:
            out.append(line)
    return "\n".join(out)


def md_to_html(text: str) -> str:
    text = checkbox_sub(text)
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )


def first_h1(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else "Untitled"


def clean_title(text: str) -> str:
    t = first_h1(text)
    if t.endswith(" — Start Here"):
        t = "Talking to Kids About AI"
    return f"{t} — {TITLE_SUFFIX}" if t else TITLE_SUFFIX


def nav_html(current: str) -> str:
    links = []
    for href, label in NAV_PAGES:
        cls = ' class="here"' if href == current else ""
        links.append(f'    <a{cls} href="{href}">{label}</a>')
    return "\n".join(links).lstrip()


def description_of(text: str) -> str:
    """First non-heading, non-blank paragraph line as the meta description."""
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        return line[:200]
    return "A plain-English parent manual for talking to kids and teens about AI."


def build(check_links: bool = False) -> list[str]:
    if not DOCS.is_dir():
        sys.stderr.write(f"error: docs/ not found at {DOCS}\n")
        sys.exit(1)

    md_files = sorted(DOCS.glob("*.md"))
    if not md_files:
        sys.stderr.write("error: no markdown files found in docs/\n")
        sys.exit(1)

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    built: dict[str, str] = {}
    for src in md_files:
        text = src.read_text(encoding="utf-8")
        html = md_to_html(text)
        page = TEMPLATE.format(
            title=clean_title(text).replace("&", "&amp;"),
            description=description_of(text),
            nav=nav_html(src.stem + ".html"),
            content=html,
        )
        out = SITE / (src.stem + ".html")
        out.write_text(page, encoding="utf-8")
        built[src.stem] = text

    broken: list[str] = []
    for stem, text in built.items():
        for target in re.findall(r"\]\(([^)#\s]+\.html)\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_file = SITE / Path(target).name
            if not target_file.exists():
                broken.append(f"{stem}.md -> {target}")
    if broken and check_links:
        for b in broken:
            sys.stderr.write(f"broken internal link: {b}\n")
        sys.exit(1)

    return sorted(built.keys())


def main() -> None:
    check = "--check" in sys.argv[1:]
    pages = build(check_links=check)
    print(f"built {len(pages)} pages -> site/:")
    for p in pages:
        print(f"  site/{p}.html")
    if not check:
        print("(run with --check to fail on broken internal links)")


if __name__ == "__main__":
    main()
