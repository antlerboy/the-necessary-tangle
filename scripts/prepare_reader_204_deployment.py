#!/usr/bin/env python3
"""Prepare 0.20.4 reader placement and SCiO/SysBoK link surfaces.

Runs after prepare_reader_203_deployment.py. The changes are deliberately static
where discoverability matters: external resource routes appear in the HTML even
without JavaScript, while scio-links-204.js enriches source records before the
main application indexes public data.
"""

from pathlib import Path

INDEX = Path("docs/index.html")

SCIO_LINKS_SCRIPT = '<script src="assets/scio-links-204.js?v=0.20.4-scio-links"></script>'
ITERATION_SCRIPT = '<script src="assets/iteration-20.js?v=0.20.4-rule-position"></script>'

CF_DROPBOX = "https://www.dropbox.com/scl/fi/v5vl9o1e9gtwxbqiyb2no/SCiO-CF-Resources.pdf?dl=0&amp;rlkey=a9d5ckhbsdjld7ab3sp60jaj9"
RESOURCES = "https://www.systemspractice.org/resources"
BOOKS = "https://www.systemspractice.org/resources/books-articles-newsletters?author=All&amp;category=All&amp;field_author_is_a_member_value=All&amp;field_has_attachments_value=All&amp;field_organiser__target_id=All&amp;language=All&amp;resource_type%5B0%5D=10&amp;resource_type%5B1%5D=1&amp;resource_type%5B2%5D=11&amp;resource_type%5B3%5D=10&amp;resource_type%5B4%5D=1&amp;resource_type%5B5%5D=11&amp;sort_by=field_publication_date_value&amp;sort_order=DESC&amp;title="
MEDIA = "https://www.systemspractice.org/resources/speakers-videos-slidedecks-podcasts?field_has_attachments_value=1&amp;resource_type%5B0%5D=14&amp;resource_type%5B1%5D=14&amp;sort_by=field_publication_date_value&amp;sort_order=DESC"
SYSBOK_SCIO = "https://www.systemspractice.org/sysbok-from-scio"
SYSBOK_KUMU = "https://kumu.io/koryckaa/scio-sysbok-v1"

ABOUT_PANEL = f'''\n        <article class="plain-panel wide scio-source-links-panel">\n          <p class="eyebrow">SCiO source routes</p>\n          <h2>Professional-practice resources and SysBoK</h2>\n          <p>These are SCiO's current public routes into its competency resources, resource catalogue and SysBoK. Material carried from SysBoK retains SCiO attribution and links to both SCiO's project page and the live Kumu project.</p>\n          <div class="button-row wrap">\n            <a class="button" href="{RESOURCES}" target="_blank" rel="noopener">All SCiO resources</a>\n            <a class="button" href="{BOOKS}" target="_blank" rel="noopener">Books, articles &amp; newsletters</a>\n            <a class="button" href="{MEDIA}" target="_blank" rel="noopener">Talks, video, slides &amp; podcasts</a>\n            <a class="button" href="{CF_DROPBOX}" target="_blank" rel="noopener">CF Resources</a>\n            <a class="button" href="{SYSBOK_SCIO}" target="_blank" rel="noopener">SysBoK at SCiO</a>\n            <a class="button primary" href="{SYSBOK_KUMU}" target="_blank" rel="noopener">Open SysBoK in Kumu</a>\n          </div>\n        </article>\n'''

HOME_CARDS = f'''\n          <a class="resource-pathway-card" href="{RESOURCES}" target="_blank" rel="noopener">\n            <span class="eyebrow">Current SCiO resource catalogue</span>\n            <strong>SCiO resources</strong>\n            <span>Browse SCiO's books, articles, talks, video, slide decks, podcasts and other practitioner resources using the site's own categories and reuse labels.</span>\n          </a>\n          <a class="resource-pathway-card" href="{SYSBOK_KUMU}" target="_blank" rel="noopener">\n            <span class="eyebrow">Connected body of knowledge</span>\n            <strong>SCiO SysBoK in Kumu</strong>\n            <span>Open the live SCiO model of systems-thinking concepts, precedents, dependent derivatives, examples and references.</span>\n          </a>'''


def insert_once(text: str, marker: str, anchor: str, insertion: str, *, after: bool = True) -> str:
    if marker in text:
        return text
    if anchor not in text:
        raise SystemExit(f"0.20.4 deployment source drifted; anchor not found: {anchor[:100]}")
    if after:
        return text.replace(anchor, anchor + insertion, 1)
    return text.replace(anchor, insertion + anchor, 1)


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    site_config_anchor = '<script src="assets/site-config.js?v=0.20.3-reader-scio"></script>'
    text = insert_once(text, 'assets/scio-links-204.js', site_config_anchor, '\n  ' + SCIO_LINKS_SCRIPT)

    enhancements_anchor = '<script src="assets/site-enhancements.js?v=0.20.3-reader-scio"></script>'
    text = insert_once(text, 'assets/iteration-20.js', enhancements_anchor, '\n  ' + ITERATION_SCRIPT)

    coverage_anchor = '        <article class="plain-panel wide"><h2>Coverage programme</h2>'
    text = insert_once(text, 'scio-source-links-panel', coverage_anchor, ABOUT_PANEL + '\n', after=False)

    reading_card_anchor = '''          <a class="resource-pathway-card" href="https://stream.syscoi.com/2024/10/01/updated-rough-draft-systems-complexity-cybernetics-reading-list/" target="_blank" rel="noopener">'''
    text = insert_once(text, 'Current SCiO resource catalogue', reading_card_anchor, HOME_CARDS + '\n', after=False)

    INDEX.write_text(text, encoding="utf-8")
    print(f"Prepared {INDEX} for 0.20.4 rule placement and SCiO/SysBoK links")


if __name__ == "__main__":
    main()
