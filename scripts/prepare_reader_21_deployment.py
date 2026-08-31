#!/usr/bin/env python3
"""Prepare the release 0.21 public reader after the reviewed assets are copied."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
SYSTEMIC = ROOT / "docs" / "prior-maps" / "systemic-evolution" / "index.html"
PRIOR_MAPS = ROOT / "docs" / "prior-maps" / "index.html"

PACKAGE_URL = (
    "https://www.dropbox.com/scl/fi/dwryvxbigb0nkw17p2plp/"
    "systemic-evolution-2026-08-26-review-1.zip?rlkey=mlacrhl6n9lwu1xsp03b0sm3i&dl=1"
)
PACKAGE_SHA = "cc0aaa4adc58a91c56f04555d5cd6885d025cdf4d546e4da8e7a692ce55c3cf6"


def replace_optional(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"0.21 reader source drifted; expected {label} marker was not found")
    return text.replace(old, new, 1)


def prepare_home() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = replace_optional(
        text,
        "assets/iteration-20.js?v=0.20.5-header",
        "assets/iteration-20.js?v=0.21-reviewed-systemic-evolution",
        "header cache",
    )
    text = replace_optional(
        text,
        '<span id="releaseBadge">Release 0.20.5</span>',
        '<span id="releaseBadge">Release 0.21</span>',
        "release badge",
    )
    old_note = (
        '<p class="release-note-inline"><strong>Updated for 0.20.5:</strong> observations now include release-state drift, '
        'interface accumulation, display-layer isolation, SCiO corpus boundaries and the difference between linking a '
        'source graph and canonising it.</p>'
    )
    new_note = (
        '<p class="release-note-inline"><strong>Updated for 0.21:</strong> the source-owner-reviewed Systemic Evolution '
        'package is now published with focused and complete layouts, a text alternative, immutable checksums and a '
        'separate approval record.</p>'
    )
    text = replace_optional(text, old_note, new_note, "AI release note")
    text = replace_optional(
        text,
        (
            '<a class="coverage-card" href="/prior-maps/"><strong>Prior maps and bodies of knowledge</strong>'
            '<span>Explore three live comparator layers, their complete source links, cumulative reconciliation and '
            'evidential limits.</span></a>'
        ),
        (
            '<a class="coverage-card" href="/prior-maps/"><strong>Prior maps and bodies of knowledge</strong>'
            '<span>Explore three live comparator layers, including the source-owner-reviewed Systemic Evolution '
            'reader, its complete source links, reconciliation and evidential limits.</span></a>'
        ),
        "prior-map home card",
    )
    INDEX.write_text(text, encoding="utf-8")


def prepare_systemic_page() -> None:
    text = SYSTEMIC.read_text(encoding="utf-8")
    text = replace_optional(
        text,
        "/assets/prior-maps.css?v=0.21.0-review",
        "/assets/prior-maps.css?v=0.21.0-published",
        "Systemic Evolution stylesheet",
    )
    text = replace_optional(
        text,
        "/assets/systemic-evolution-map.js?v=0.21.0-review",
        "/assets/systemic-evolution-map.js?v=0.21.0-published",
        "Systemic Evolution script",
    )
    publication_stylesheet = (
        '  <link rel="stylesheet" href="/assets/systemic-evolution-release-21.css?v=0.21.0-published">\n'
    )
    if publication_stylesheet not in text:
        stylesheet_anchor = '  <link rel="stylesheet" href="/assets/prior-maps.css?v=0.21.0-published">\n'
        if stylesheet_anchor not in text:
            raise SystemExit("0.21 Systemic Evolution stylesheet anchor was not found")
        text = text.replace(stylesheet_anchor, stylesheet_anchor + publication_stylesheet, 1)
    approval = (
        '  <div class="pm-callout"><p><strong>Source-owner review completed.</strong> Benjamin Hadorn reviewed the '
        f'exact package identified by SHA-256 <code>{PACKAGE_SHA[:12]}…</code> and approved the enhanced version for '
        'publication on 31 August 2026. The scope grant, reviewed files and publication decision remain separate '
        'records.</p></div>\n'
    )
    if approval not in text:
        marker = "  </header>\n\n  <div class=\"pm-stats\""
        if marker not in text:
            raise SystemExit("0.21 Systemic Evolution header marker was not found")
        text = text.replace(marker, "  </header>\n\n" + approval + "\n  <div class=\"pm-stats\"", 1)

    old_files = '''    <p>The original 2016 GraphML is retained byte for byte. The enriched derivative adds attribution, permission, reconciliation and evidence-state fields without removing or adding a source node or source edge. A checksummed manifest identifies the exact files submitted for source-owner review.</p>
    <ul>
      <li><a href="/assets/systemic_evolution-2016-original.graphml" download>Original GraphML</a> — 650 nodes, 1,320 links; SHA-256 <code>c42241d6…d104</code>.</li>
      <li><a href="/assets/systemic_evolution-the-necessary-tangle.graphml" download>Enriched derivative GraphML</a> — the same source structure plus Tangle annotations.</li>
      <li><a href="/assets/comparator-systemic-evolution.json">Machine-readable comparator JSON</a>.</li>
      <li><a href="/assets/systemic-evolution-reconciliation.json">Cumulative reconciliation ledger</a>.</li>
      <li><a href="/assets/systemic-evolution-review-manifest.json">Checksums and review manifest</a>.</li>
    </ul>'''
    new_files = f'''    <p>The original 2016 GraphML is retained byte for byte inside the reviewed archive. The enriched derivative adds attribution, permission, reconciliation and evidence-state fields without removing or adding a source node or source edge. The manifest identifies every reviewed file and checksum.</p>
    <ul>
      <li><a href="{PACKAGE_URL}" target="_blank" rel="noopener">Download the exact reviewed package</a> — original and enriched GraphML, reader files and records; SHA-256 <code>{PACKAGE_SHA}</code>.</li>
      <li><a href="/assets/comparator-systemic-evolution.json">Machine-readable comparator JSON</a>.</li>
      <li><a href="/assets/systemic-evolution-reconciliation.json">Cumulative reconciliation ledger</a>.</li>
      <li><a href="/assets/systemic-evolution-review-manifest.json">Checksums and review manifest</a>.</li>
      <li><a href="/assets/systemic-evolution-publication-approval.json">Publication approval record</a>.</li>
    </ul>'''
    text = replace_optional(text, old_files, new_files, "reviewed file list")
    old_permission = (
        "On 26 August 2026 Benjamin Hadorn authorised the requested retention, parsing, visualisation, annotation, "
        "extension, derivative publication and independently checked incorporation, subject to full attribution "
        "and pre-publication review of modifications. He confirmed that separate approaches to the other parties "
        "were not required for the complete version if those conditions were met. This project-specific permission "
        "is not presented as a general CC BY-SA relicensing of the original."
    )
    new_permission = old_permission + (
        " On 31 August 2026, he confirmed that he had checked the exact checksummed package and approved use of "
        "the enhanced version in this way."
    )
    text = replace_optional(text, old_permission, new_permission, "final source-owner approval")
    SYSTEMIC.write_text(text, encoding="utf-8")


def prepare_prior_map_hub() -> None:
    text = PRIOR_MAPS.read_text(encoding="utf-8")
    text = replace_optional(
        text,
        (
            '<a class="pm-card" href="/prior-maps/systemic-evolution/"><span class="eyebrow">Permissioned comparator</span>'
            '<strong>Map of Systemic Evolution</strong><p>650 source nodes, all 1,320 reported major-influence links, '
            'and a cumulative reconciliation ledger.</p></a>'
        ),
        (
            '<a class="pm-card" href="/prior-maps/systemic-evolution/"><span class="eyebrow">Source-owner reviewed comparator</span>'
            '<strong>Map of Systemic Evolution</strong><p>650 source nodes, all 1,320 reported major-influence links, '
            'focused and complete layouts, and a cumulative reconciliation ledger.</p></a>'
        ),
        "Systemic Evolution hub card",
    )
    PRIOR_MAPS.write_text(text, encoding="utf-8")


def main() -> None:
    prepare_home()
    prepare_systemic_page()
    prepare_prior_map_hub()
    print("Prepared the 0.21 reviewed Systemic Evolution reader and release routes")


if __name__ == "__main__":
    main()
