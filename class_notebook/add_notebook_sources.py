from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", ROOT / "bda_study.html", ROOT / "sjnjkwv.txt"]
TEXT_DIR = ROOT / "class_notebook" / "text"
PDF_DIR = ROOT / "class_notebook" / "pdf"
SLIDE_DIR = ROOT / "class_notebook" / "slides"


DOCS = [
  ("src-unit-1", "Unit 1", "unit-1_bda"),
  ("src-unit-2", "Unit 2", "unit-2_bda"),
  ("src-unit-3", "Unit 3", "unit-3_bda"),
  ("src-unit-4", "Unit 4 (Hadoop in Unit 3)", "unit-4_bda"),
  ("src-unit-5a", "Unit 5A", "unit-5a_bda"),
  ("src-unit-5b", "Unit 5B", "unit-5b_bda"),
  ("src-unit-5c", "Unit 5C", "unit-5c_bda"),
]


CSS_START = "/* CLASS NOTEBOOK SOURCES START */"
CSS_END = "/* CLASS NOTEBOOK SOURCES END */"
NAV_START = "<!-- CLASS NOTEBOOK NAV START -->"
NAV_END = "<!-- CLASS NOTEBOOK NAV END -->"
PAGES_START = "<!-- CLASS NOTEBOOK SOURCE PAGES START -->"
PAGES_END = "<!-- CLASS NOTEBOOK SOURCE PAGES END -->"


def read_pages(stem: str) -> list[str]:
    text_path = TEXT_DIR / f"{stem}.txt"
    raw = text_path.read_text(encoding="utf-8", errors="replace")
    pages = [page.strip("\n\r ") for page in raw.split("\f")]
    return [page for page in pages if page.strip()]


def pdf_href(stem: str) -> str:
    return f"class_notebook/pdf/{stem}.pdf"


def slide_href(stem: str, page_number: int) -> str | None:
    slide_dir = SLIDE_DIR / stem
    candidates = [
        slide_dir / f"page-{page_number}.jpg",
        slide_dir / f"page-{page_number:02d}.jpg",
        slide_dir / f"page-{page_number:03d}.jpg",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.relative_to(ROOT).as_posix()
    return None


def replace_or_insert(text: str, start: str, end: str, block: str, marker: str) -> str:
    if start in text and end in text:
        before = text[: text.index(start)]
        after = text[text.index(end) + len(end) :]
        return before + block + after
    return text.replace(marker, block + "\n" + marker)


def build_css() -> str:
    return f"""{CSS_START}
.source-note-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
  margin: 18px 0 28px;
}}
.source-card {{
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 14px 16px;
  cursor: pointer;
}}
.source-card:hover {{ border-color: var(--text); background: var(--bg3); }}
.source-card strong {{
  display: block;
  font-size: 13px;
  color: var(--text);
  margin-bottom: 6px;
}}
.source-card span {{
  display: block;
  font-size: 11px;
  color: var(--text3);
  font-family: 'JetBrains Mono', monospace;
}}
.source-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 14px 0 22px;
}}
.source-pill, .source-link {{
  border: 1px solid var(--border2);
  border-radius: 4px;
  padding: 5px 9px;
  font-size: 11px;
  color: var(--text2);
  background: var(--bg2);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
}}
.source-link:hover {{ border-color: var(--text); color: var(--text); }}
.source-slide {{
  border: 1px solid var(--border);
  border-radius: 6px;
  margin: 16px 0;
  background: var(--bg);
  overflow: hidden;
}}
.source-slide-head {{
  background: var(--text);
  color: #fff;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  letter-spacing: 1px;
  padding: 8px 12px;
  text-transform: uppercase;
}}
.source-slide-image {{
  display: block;
  width: 100%;
  height: auto;
  background: #f2f2f0;
  border-top: 1px solid var(--border);
}}
pre.source-text {{
  margin: 0;
  border-radius: 0;
  background: #fbfbfa;
  color: var(--text);
  border-top: 1px solid var(--border);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  font-size: 12px;
  line-height: 1.55;
}}
{CSS_END}"""


def build_nav() -> str:
    lines = [
        NAV_START,
        '    <div class="nav-section-label">Class Notebook Source</div>',
        '    <a class="nav-item special" onclick="showPage(\'source-index\')">📚 Source Index</a>',
    ]
    for doc_id, title, _ in DOCS:
        lines.append(f'    <a class="nav-item sub" onclick="showPage(\'{doc_id}\')">{escape(title)}</a>')
    lines.append(NAV_END)
    return "\n".join(lines)


def build_index() -> str:
    cards = []
    rows = []
    total_pages = 0
    total_chars = 0
    for doc_id, title, stem in DOCS:
        pages = read_pages(stem)
        chars = sum(len(page) for page in pages)
        total_pages += len(pages)
        total_chars += chars
        cards.append(
            f"""      <div class="source-card" onclick="showPage('{doc_id}')">
        <strong>{escape(title)}</strong>
        <span>{len(pages)} pages · {chars:,} extracted chars</span>
      </div>"""
        )
        rows.append(
            f"<tr><td>{escape(title)}</td><td>{len(pages)}</td><td>{chars:,}</td><td><a href=\"{escape(pdf_href(stem))}\">PDF</a></td></tr>"
        )

    return f"""  <div id="page-source-index" class="page">
    <div class="hero">
      <div class="unit-label">Class Notebook Source</div>
      <h2>Full PPT/PDF Source Content</h2>
      <p>Extracted from the uploaded class notebook ZIP on May 28, 2026. This section keeps the raw source material next to the exam-ready notes.</p>
      <div class="hero-tags">
        <span class="hero-tag">{len(DOCS)} files</span>
        <span class="hero-tag">{total_pages} pages</span>
        <span class="hero-tag">{total_chars:,} extracted characters</span>
      </div>
    </div>

    <div class="callout callout-blue"><strong>Coverage note:</strong> These pages preserve both rendered slide images and extracted text from every PDF in the ZIP. The original PDFs are linked beside each source.</div>

    <div class="source-note-grid">
{chr(10).join(cards)}
    </div>

    <div class="tbl-wrap">
      <table class="vs-table">
        <thead><tr><th>Source File</th><th>Pages</th><th>Text Size</th><th>Original</th></tr></thead>
        <tbody>
          {chr(10).join(rows)}
        </tbody>
      </table>
    </div>
  </div>"""


def build_doc_page(doc_id: str, title: str, stem: str) -> str:
    pages = read_pages(stem)
    page_blocks = []
    for idx, page in enumerate(pages, start=1):
        image_rel = slide_href(stem, idx)
        image_html = ""
        if image_rel:
            image_html = (
                f'\n      <img class="source-slide-image" loading="lazy" '
                f'src="{escape(image_rel)}" alt="{escape(title)} page {idx}">'
            )
        page_blocks.append(
            f"""    <div class="source-slide">
      <div class="source-slide-head">Source Page {idx}</div>{image_html}
      <pre class="source-text">{escape(page)}</pre>
    </div>"""
        )
    char_count = sum(len(page) for page in pages)
    return f"""  <div id="page-{doc_id}" class="page source-page">
    <div class="hero">
      <div class="unit-label">Class Notebook Source</div>
      <h2>{escape(title)}</h2>
      <p>Full text extracted from {escape(stem)}.pdf.</p>
      <div class="hero-tags">
        <span class="hero-tag">{len(pages)} pages</span>
        <span class="hero-tag">{char_count:,} extracted characters</span>
      </div>
    </div>

    <div class="source-meta">
      <a class="source-link" href="{escape(pdf_href(stem))}">Original PDF</a>
      <span class="source-pill">{escape(stem)}.pdf</span>
    </div>

{chr(10).join(page_blocks)}
  </div>"""


def build_pages() -> str:
    pages = [PAGES_START, build_index()]
    for doc_id, title, stem in DOCS:
        pages.append(build_doc_page(doc_id, title, stem))
    pages.append(PAGES_END)
    return "\n\n".join(pages)


def update_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = replace_or_insert(text, CSS_START, CSS_END, build_css(), "\n@media (max-width: 768px)")
    text = replace_or_insert(text, NAV_START, NAV_END, build_nav(), "  </div>\n</nav>")
    text = replace_or_insert(text, PAGES_START, PAGES_END, build_pages(), "\n</div><!-- /#main -->")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    missing = [stem for _, _, stem in DOCS if not (TEXT_DIR / f"{stem}.txt").exists()]
    if missing:
        raise SystemExit(f"Missing extracted text files: {missing}")
    for html_file in HTML_FILES:
        if html_file.exists():
            update_html(html_file)
            print(f"updated {html_file.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
