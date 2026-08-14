#!/usr/bin/env python3
"""Repair Pass 6 accessibility and mobile issues idempotently."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
STYLES = ROOT / "docs" / "assets" / "styles.css"
READING = ROOT / "docs" / "reading-list.html"


READING_STYLE = (
    ".reading-nav{max-width:1200px;margin:0 auto;padding:1rem 1.3rem 0}"
    ".reading-table-wrap{max-width:100%;overflow-x:auto;border-radius:var(--radius)}"
    "table{table-layout:fixed}th,td{overflow-wrap:anywhere}"
    "th:first-child,td:first-child{width:22%}th:last-child,td:last-child{width:18%}"
    "@media(max-width:760px){.reading-shell{padding-inline:.85rem}.reading-nav{padding-inline:.85rem}"
    ".coverage-grid{grid-template-columns:1fr 1fr}th:first-child,td:first-child{display:none}"
    "th:last-child,td:last-child{width:32%}th:nth-child(2),td:nth-child(2){width:68%}}"
)


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if '<h2 class="hidden" id="browseResultsHeading">Matching entries</h2>' not in text:
        anchor = '      <div id="browseCards" class="card-grid three"></div>'
        if anchor not in text:
            raise RuntimeError("Browse results anchor missing")
        text = text.replace(anchor, '      <h2 class="hidden" id="browseResultsHeading">Matching entries</h2>\n' + anchor, 1)
    text = text.replace('<h3>Find a path</h3>', '<h2 class="control-heading">Find a path</h2>', 1)
    INDEX.write_text(text, encoding="utf-8")


def patch_styles() -> None:
    text = STYLES.read_text(encoding="utf-8")
    text = text.replace('.map-controls h3 { margin: 0; color: var(--accent); }', '.map-controls h3, .map-controls .control-heading { margin: 0; color: var(--accent); font-size: 1.17em; }')
    STYLES.write_text(text, encoding="utf-8")


def patch_reading_page() -> None:
    text = READING.read_text(encoding="utf-8")
    if 'assets/site-enhancements.css' not in text:
        text = text.replace('<style>', '<link rel="stylesheet" href="assets/site-enhancements.css?v=0.16.3-visual"><style>', 1)

    start = text.index('<style>') + len('<style>')
    end = text.index('</style>', start)
    inline = text[start:end]
    # Remove the older mobile rule before appending the more precise fixed-table rule.
    inline = inline.replace('@media(max-width:760px){.coverage-grid{grid-template-columns:1fr 1fr}th:first-child,td:first-child{display:none}}', '')
    if '.reading-table-wrap' not in inline:
        inline += READING_STYLE
    text = text[:start] + inline + text[end:]

    if 'id="reading-main"' not in text:
        text = text.replace(
            '<body>\n<div class="reading-shell"><p><a href="index.html#view=home">← The Necessary Tangle</a></p>',
            '<body>\n<a class="skip-link" href="#reading-main">Skip to reading list</a>\n<nav class="reading-nav" aria-label="Reading-list navigation"><a href="index.html#view=home">← The Necessary Tangle</a></nav>\n<main id="reading-main" class="reading-shell" tabindex="-1">',
            1,
        )
    if '<div class="reading-table-wrap"><table>' not in text:
        text = text.replace('<table><thead>', '<div class="reading-table-wrap"><table><thead>', 1)
    if 'data-update-thread-dot' not in text:
        text = text.replace(
            '</tbody></table></div>\n<script>',
            '</tbody></table></div></main>\n<a class="update-thread-dot" data-update-thread-dot href="https://github.com/antlerboy/the-necessary-tangle/issues/2" target="_blank" rel="noopener" aria-label="Open updates"></a>\n<script>',
            1,
        )
    READING.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    patch_index()
    patch_styles()
    patch_reading_page()
    print("Applied Pass 6 accessibility and reading-list mobile repairs.")
