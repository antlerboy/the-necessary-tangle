#!/usr/bin/env python3
"""Finish release 0.16 presentation, canonical URLs and release prose."""
from __future__ import annotations

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
APP = ROOT / "docs" / "assets" / "app.js"
CSS = ROOT / "docs" / "assets" / "site-enhancements.css"
RELEASE = "0.16-grammar-connections-presentation-alpha"
PUBLIC_URL = "https://transduction.systems/"


def clean(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.rstrip().splitlines()) + "\n"


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{PUBLIC_URL}">', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{PUBLIC_URL}">', text, count=1)
    text = re.sub(r'assets/styles\.css(?:\?v=[^"\']+)?', "assets/styles.css?v=0.16", text, count=1)
    text = re.sub(r'assets/site-enhancements\.css(?:\?v=[^"\']+)?', "assets/site-enhancements.css?v=0.16", text, count=1)
    text = re.sub(r'assets/app\.js(?:\?v=[^"\']+)?', "assets/app.js?v=0.16", text, count=1)

    if 'id="browseConnectionDepth"' not in text:
        marker = '<label>Depth<select id="browseLevel"><option value="developed">All readable entries</option><option value="profile">Developed entries only</option></select></label>'
        addition = marker + '\n        <label>Connections<select id="browseConnectionDepth"><option value="all">All connection depths</option><option value="rich">Rich</option><option value="developing">Developing</option><option value="thin">Thin</option><option value="unconnected">Unconnected</option></select></label>'
        if marker not in text:
            raise RuntimeError("browse-depth filter marker not found")
        text = text.replace(marker, addition, 1)
    text = text.replace('Reader map — substantive relationships', 'Reader map — meaningful relationships')

    start_cards = '''<div class="start-small-grid">
          <a class="start-small-card" href="#view=item&id=person_ivo_velitchkov&from=home"><span class="eyebrow">Viability and balance</span><strong>Ivo Velitchkov</strong><span>Viable organisation, Essential Balances, requisite inefficiency and explicit semantic graphs.</span></a>
          <a class="start-small-card" href="#view=item&id=person_patrick_hoverstadt&from=home"><span class="eyebrow">Management cybernetics</span><strong>Patrick Hoverstadt</strong><span>The Viable System Model, systems laws, organisation design and relational strategy.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_inquiry_governance_and_intervention&step=0"><span class="eyebrow">A guided route</span><strong>Inquiry, governance and intervention</strong><span>Checkland, Ulrich, Espejo, Ison, Meadows, Oshry, Velitchkov and Hoverstadt in one inspectable route.</span></a>
          <a class="start-small-card" href="#view=item&id=person_donella_meadows&from=home"><span class="eyebrow">Feedback and intervention</span><strong>Donella Meadows</strong><span>Thinking in Systems, leverage points and disciplines for acting with nonlinear systems.</span></a>
          <a class="start-small-card" href="#view=map&layer=substantive&depth=1&focus=concept_viability"><span class="eyebrow">A readable neighbourhood</span><strong>Viability and its immediate connections</strong><span>Start with one question-sized piece of the graph; expand only when it helps.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_david_ing_systems_in_plural&step=0"><span class="eyebrow">Service systems and lineages</span><strong>David Ing journey</strong><span>Follow service systems thinking, Systems Changes Learning, pattern language and unusually rich documentation of systems lineages.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_core_systems_practice_reading&step=0"><span class="eyebrow">Professional systems practice</span><strong>Core systems practice</strong><span>Concepts and laws, CSH, SSM, System Dynamics, VSM, multi-methodology, intervention and reflexive learning.</span></a>
          <a class="start-small-card" href="#view=journeys&id=journey_grammar_principles_in_connection&step=0"><span class="eyebrow">The Grammar of Systems</span><strong>The Grammar is a web, not a list</strong><span>Follow eight principles through all nine thinking patterns, then inspect their conceptual and practical connections.</span></a>
          <a class="start-small-card" href="reading-list.html"><span class="eyebrow">Reading and coverage</span><strong>Reading-list depth map</strong><span>Every captured reading-list item with its current status: developed profile, represented, or inventory-only.</span></a>
        </div>'''
    text, count = re.subn(r'<div class="start-small-grid">.*?</div>', start_cards, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("start-small grid not found")

    if "documentation/original-vision-audit.md" not in text:
        marker = '<div class="button-row wrap">'
        addition = marker + '<a class="button primary" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/original-vision-audit.md" target="_blank" rel="noopener">Original vision audit</a>'
        documentation_panel = text.find('<article class="plain-panel wide"><h2>Documentation</h2>')
        if documentation_panel < 0:
            raise RuntimeError("documentation panel not found")
        marker_at = text.find(marker, documentation_panel)
        if marker_at < 0:
            raise RuntimeError("documentation button row not found")
        text = text[:marker_at] + text[marker_at:].replace(marker, addition, 1)

    if "relationalDepthMetrics" not in text:
        marker = '<article class="plain-panel wide"><h2>What it is</h2><p>The Necessary Tangle is a navigable, evidence-backed account of systems | cybernetics | complexity. It maps concepts, people, methods, publications, institutions, practices and traditions, and distinguishes the different ways they connect.</p><p>It is both a reference atlas and a revisable argument. Any map is selective and interpretive; drawing it does not make it neutral.</p></article>'
        addition = marker + '''

        <article class="plain-panel wide relational-depth-panel">
          <p class="eyebrow">Connections are maintained data</p>
          <h2>Relational depth, made visible</h2>
          <p>Every public entry now has two separate readings: <strong>structural depth</strong> counts distinct reader neighbours and relation families; <strong>evidence depth</strong> distinguishes accepted or corroborated statements from provisional crosswalks. More lines never turn interpretation into proof.</p>
          <div class="metrics" id="relationalDepthMetrics"></div>
          <p>The target shape differs by entry: a concept needs prerequisites, contrasts, history, uses and challenges; a person needs works, institutions and human transmission; a method needs foundations, tools, cases and limits. Thin entries remain visible as the public work queue.</p>
          <p><a class="button primary" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/relational-depth.md" target="_blank" rel="noopener">Inspect the relational-depth programme</a> <a class="button" href="#view=browse" data-view-link="browse">Browse by connection depth</a></p>
        </article>'''
        if marker not in text:
            raise RuntimeError("about introduction marker not found")
        text = text.replace(marker, addition, 1)

    INDEX.write_text(clean(text), encoding="utf-8")


def check_reader_code() -> None:
    app = APP.read_text(encoding="utf-8")
    if "function publicEntryEdge(edge)" not in app or ".filter(publicEntryEdge)" not in app:
        raise RuntimeError("full-entry public connection filter is missing")
    for marker in ("relationalDepthByNode", "browseConnectionDepth", "connectionBandLabel", "documentary: 'Works, authorship and presentation'"):
        if marker not in app:
            raise RuntimeError(f"relational-depth reader marker missing: {marker}")
    css = CSS.read_text(encoding="utf-8")
    for marker in (
        "/* 0.16 presentation repair",
        ".metrics {",
        ".quick-links",
        ".card-grid {",
        ".results-line {",
        ".drawer {",
        ".scrim {",
        ".relational-depth-panel",
        ".update-thread-dot {",
    ):
        if marker not in css:
            raise RuntimeError(f"0.16 CSS marker missing: {marker}")


def patch_release_prose() -> None:
    citation = ROOT / "CITATION.cff"
    text = citation.read_text(encoding="utf-8")
    text = re.sub(r"^url:.*$", f"url: {PUBLIC_URL}", text, flags=re.M)
    text = re.sub(r"^version:.*$", f"version: {RELEASE}", text, flags=re.M)
    text = re.sub(r"^date-released:.*$", "date-released: 2026-08-14", text, flags=re.M)
    citation.write_text(clean(text), encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("https://antlerboy.github.io/the-necessary-tangle/", PUBLIC_URL)
    data = json.loads((ROOT / "data" / "public-data.json").read_text(encoding="utf-8"))
    meta = data["meta"]
    text = re.sub(
        r"This is a public alpha\. Release 0\.\d+ contains \d+ canonical public entries, including \d+ developed profiles, \d+ sources and \d+ guided journeys\.",
        f"This is a public alpha. Release 0.16 contains {meta['public_entry_count']} canonical public entries, including {meta['profile_count']} developed profiles, {meta['source_count']} sources and {meta['journey_count']} guided journeys.",
        text,
        count=1,
    )
    duplicate = "The [reading-list depth map](https://transduction.systems/reading-list.html) exposes all 110 captured items and distinguishes developed profiles, thinner representation and inventory-only coverage."
    while text.count(duplicate) > 1:
        text = text.replace("\n" + duplicate + "\n", "\n", 1)
    relational_paragraph = "The [relational-depth programme](documentation/relational-depth.md) now measures every public entry by distinct reader neighbours and relation families, separately from the evidential strength of those statements. The first graph-wide cohort removes reader-isolated entries, connects all maintained intervention skills, and leaves thin people, publications and corpora visible as an ordered research queue rather than disguising them with generic “related to” links."
    if relational_paragraph not in text:
        marker = "Release 0.16 makes the 33 *Grammar of Systems* laws and principles visible as a connected web rather than a disconnected list. The book-to-law statements are source-backed; the new law-to-concept, law-to-law and law-to-practice crosswalk is explicitly provisional and open to page-level evidence and challenge."
        if marker not in text:
            raise RuntimeError("0.16 Grammar README paragraph not found")
        text = text.replace(marker, marker + "\n\n" + relational_paragraph, 1)
    readme.write_text(clean(text), encoding="utf-8")

    for name in ("reading-list-coverage.md", "core-systems-practice.md"):
        path = ROOT / "documentation" / name
        text = path.read_text(encoding="utf-8").replace("0.15-ing-reading-practice-alpha", RELEASE)
        path.write_text(clean(text), encoding="utf-8")

    reading_page = ROOT / "docs" / "reading-list.html"
    text = reading_page.read_text(encoding="utf-8")
    text = re.sub(r'assets/styles\.css(?:\?v=[^"\']+)?', "assets/styles.css?v=0.16", text, count=1)
    reading_page.write_text(clean(text), encoding="utf-8")

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    heading = f"## {RELEASE} — 14 August 2026"
    if heading not in text:
        entry = f"""{heading}

- Connected all 33 *Grammar of Systems* laws and principles to the source publication and to multiple concepts, principles or practices.
- Marked the 178 semantic crosswalk statements as provisional and challengeable pending page-level evidence review.
- Added the guided journey “The Grammar is a web, not a list” across all nine Grammar patterns.
- Restored the missing layout primitives and the fixed entry drawer while retaining the discreet bottom-right update dot.
- Added an audit and ordered acceptance criteria against the original vision and specification.
- Closed the two superseded v0.12 release-workflow pull requests without merging them.

"""
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    relational_bullet = "- Added graph-wide structural and evidential depth measures, a public depth filter and an explicit enrichment queue."
    if relational_bullet not in text:
        marker = "- Marked the 178 semantic crosswalk statements as provisional and challengeable pending page-level evidence review."
        addition = marker + "\n" + relational_bullet + "\n- Added typed provisional routes for all maintained intervention skills and the previously isolated concept, method, tool and tradition cohort; exposed official collection contents as documentary statements.\n- Incorporated slide-level relational evidence from the supplied transformation, convening, organisational-dynamics, VSM, clarity and conversation material."
        if marker not in text:
            raise RuntimeError("0.16 Grammar changelog marker not found")
        text = text.replace(marker, addition, 1)
    changelog.write_text(clean(text), encoding="utf-8")


def main() -> None:
    patch_index()
    check_reader_code()
    patch_release_prose()
    print("Patched 0.16 presentation, canonical URLs and release prose")


if __name__ == "__main__":
    main()
