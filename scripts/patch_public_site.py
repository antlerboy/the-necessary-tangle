#!/usr/bin/env python3
"""Apply the public-facing 0.6 site wording and interface refinements.

The source page pre-dates the move to the canonical antlerboy account and the
first public feedback round. Keeping this as an idempotent build step makes the
release reproducible while avoiding hand-edited drift in generated deployments.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

AUTHOR_STRIP = '''      <section class="author-strip">
        <div><p class="eyebrow">Curator</p><h2><a href="https://www.antlerboy.com/">Benjamin P Taylor</a></h2><p>The Necessary Tangle is an independent public project. Its immediate provocation was David Ing's formulation, as Benjamin records it: ‘we need to map the constellation of influences around practitioners’. It develops the connected-body-of-knowledge idea behind SCiO's earlier SysBoK while treating systems | cybernetics | complexity as a necessary tangle of theory, practice, people and institutions.</p></div>
        <div class="button-stack"><a class="button" href="https://www.antlerboy.com/">About Benjamin</a><a class="button" href="https://stream.syscoi.com/" target="_blank" rel="noopener">Systems Community of Inquiry</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle" target="_blank" rel="noopener">Project on GitHub</a></div>
      </section>'''

ABOUT_SECTION = '''    <section id="view-about" class="view">
      <header class="page-head"><p class="eyebrow">Purpose, method, coverage and limits</p><h1>About The Necessary Tangle</h1><p>A reference work should explain its choices without forcing readers to learn its database vocabulary.</p></header>
      <div class="about-grid">
        <article class="plain-panel wide"><h2>What it is</h2><p>The Necessary Tangle is a navigable, evidence-backed account of systems | cybernetics | complexity. It maps concepts, people, methods, publications, institutions, practices and traditions, and distinguishes the different ways they connect.</p><p>It is both a reference atlas and a revisable argument. Any map is selective and interpretive; drawing it does not make it neutral.</p></article>

        <article class="plain-panel"><h2>Current state</h2><p>This is a public alpha. It has broad seed coverage and a smaller evidence-deepened core. The current build reports its entry, source, connection, profile and journey counts on the home page.</p></article>
        <article class="plain-panel"><h2>Strongest now</h2><p>The deepest connected material is around boundaries and observers; feedback and regulation; variety, viability and the Viable System Model; recursion; emergence; and self-organisation.</p></article>
        <article class="plain-panel"><h2>Most incomplete</h2><p>Complexity needs a fuller treatment on its own terms. Human and institutional lineage, teaching, supervision, collaboration, laboratories, conferences and practice transmission remain thin. Many entries still offer orientation rather than a full research profile.</p></article>

        <article class="plain-panel"><h2>Why ‘necessary’?</h2><p>The project asks which earlier ideas are needed to understand a later one, which adjacent material is needed to explain the field, and what evidence is needed before a connection is treated as established.</p></article>
        <article class="plain-panel"><h2>Every line makes a statement</h2><p>A line may represent logical dependence, historical sequence, influence, teaching, collaboration, practical use, comparison or dispute. Select it to see the wording, limits, status and sources. ‘Related to’ is not enough.</p></article>
        <article class="plain-panel"><h2>Scope</h2><p>The core is systems | cybernetics | complexity. Adjacent material is included when it materially explains a central idea, practice, lineage or dispute. The aim is not to map all human thought.</p></article>
        <article class="plain-panel"><h2>Sources</h2><p>Public links are used where they exist. A published book or archive item without an open copy is marked ‘No public link’. Private research may identify a lead, but private URLs and extracts are not published.</p></article>

        <article class="plain-panel wide"><h2>A practitioner-centred origin</h2><blockquote>‘We need to map the constellation of influences around practitioners.’</blockquote><p>This formulation from David Ing, as recorded by Benjamin P Taylor, is the immediate provocation for the human-lineage layer. It shifts attention from a tidy history of schools to the actual routes through which practitioners encounter, combine, teach and use ideas.</p></article>

        <article class="plain-panel wide"><h2>Coverage programme</h2><p>The following are now explicit pieces of work, not vague aspirations. Each card opens the issue containing scope and completion tests.</p><div class="coverage-grid">
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/3" target="_blank" rel="noopener"><strong>Foundational Papers in Complexity Science</strong><span>Inventory, summarise and map every item in the named collection.</span></a>
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/4" target="_blank" rel="noopener"><strong>Monoskop</strong><span>Review relevant public pages and bibliographies without treating the whole site as automatically in scope.</span></a>
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/5" target="_blank" rel="noopener"><strong>SysCoI and model.report</strong><span>Use the public archives as evidence of circulation, discussion and discovery.</span></a>
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/6" target="_blank" rel="noopener"><strong>Prior maps and bodies of knowledge</strong><span>Compare purposes, categories, boundaries, lines and evidence, including Castellani's map and Benjamin's critique.</span></a>
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/7" target="_blank" rel="noopener"><strong>Practitioner influence constellations</strong><span>Deepen teaching, mentoring, collaboration, institutions and practice transmission.</span></a>
          <a class="coverage-card" href="https://github.com/antlerboy/the-necessary-tangle/issues/8" target="_blank" rel="noopener"><strong>Company knowledge discovery</strong><span>Use private knowledge only to find leads; replace it with public evidence or a proper ‘No public link’ citation.</span></a>
        </div><p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/coverage-programme.md" target="_blank" rel="noopener">Read the full coverage programme →</a></p></article>

        <article class="plain-panel"><h2>How to read status</h2><p>‘Developed entry’ means a fuller research pass, not final consensus. ‘Brief entry’ offers responsible orientation and sources. Disputed connections can remain visible as disputed.</p></article>
        <article class="plain-panel"><h2>Corrections and dialogue</h2><p>Definite corrections belong in GitHub Issues. Open questions and wider interpretations belong in GitHub Discussions. Accepted changes are versioned; unresolved disagreement is recorded.</p></article>

        <article class="plain-panel wide"><h2>Curatorship and acknowledgements</h2><p><strong>Curated by <a href="https://www.antlerboy.com/">Benjamin P Taylor</a>.</strong> Benjamin is responsible for the current editorial choices; ‘curator’ does not imply sole creation of the knowledge represented here.</p><p>The project develops the connected approach of the original SCiO Systems Thinking Body of Knowledge and later competency work. Particular acknowledgement is due to David Ing for the practitioner-influence provocation and for preserving and supporting the SysCoI/model.report lineage; Tony Korycki and other SysBoK contributors; Patrick Hoverstadt, Lucy Loh and colleagues associated with the Grammar of Systems; Igor Perko for a substantial researchers-network comparator; Brian Castellani and other map makers whose work provides both material and challenge; the SCiO community; and the authors, teachers, practitioners and archivists cited throughout.</p><p>OpenAI tools have assisted research organisation, data processing and software prototyping. Benjamin P Taylor remains responsible for what is accepted and published.</p><p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/ACKNOWLEDGEMENTS.md" target="_blank" rel="noopener">Read the fuller acknowledgements →</a></p></article>

        <article class="plain-panel wide"><h2>Rights, reuse and responsibility</h2><p>Original atlas text, public data and editorial material are licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="license noopener">Creative Commons Attribution-ShareAlike 4.0 International</a>, unless otherwise marked. Original software is available under the MIT licence. Third-party works remain under their own terms and are not relicensed here.</p><p>This is a developing scholarly and practitioner resource, not an official position of SCiO or any other named organisation. It contains provisional and disputed interpretations and will contain errors and omissions.</p><p><a href="https://github.com/antlerboy/the-necessary-tangle/blob/main/RIGHTS.md" target="_blank" rel="noopener">Read the rights and licensing statement →</a></p></article>

        <article class="plain-panel wide"><h2>Documentation</h2><p>The method, source policy, data model, maintenance process, governance, coverage programme and current limitations live with the project rather than in detached files.</p><div class="button-row wrap"><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/reading-the-atlas.md" target="_blank" rel="noopener">How to read the atlas</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/editorial-model.md" target="_blank" rel="noopener">Editorial model</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/source-policy.md" target="_blank" rel="noopener">Source policy</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/coverage-programme.md" target="_blank" rel="noopener">Coverage programme</a><a class="button" href="https://github.com/antlerboy/the-necessary-tangle/blob/main/documentation/roadmap.md" target="_blank" rel="noopener">Roadmap</a></div></article>
      </div>
      <details class="technical-details"><summary>Editorial and technical detail</summary><div><h3>Different connections answer different questions</h3><p>Historical sequence, logical dependence, explicit influence, teaching, collaboration, citation and practical use are represented separately. Treating them all as ‘related to’ produces false family trees.</p><h3>Statements remain inspectable</h3><p>Each proposed connection has a direction, wording, scope, status and sources. Competing accounts can coexist. Editorial acceptance means that the current evidence supports the stated wording; it does not make the field finally settled.</p><h3>What the website publishes</h3><p>The GitHub Pages build contains only public data and public website files. Private research leads and internal working material are excluded.</p></div></details>
    </section>'''


def replace_once(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise RuntimeError(f"Expected public-site marker not found: {old[:80]!r}")


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    replacements = {
        "The Necessary Tangle is a living evidence atlas of systems, complexity and cybernetics: what the ideas mean, where they came from, how they connect and how they are used.": "The Necessary Tangle is a living evidence atlas of systems | cybernetics | complexity: ideas, people, methods, practices, lineages and the evidence behind their connections.",
        "A living evidence atlas of systems, complexity and cybernetics. Every connection must say what it means.": "A living evidence atlas of systems | cybernetics | complexity. Every connection must say what it means.",
        "https://antlerboy-benjamintaylor.github.io/the-necessary-tangle/": "https://antlerboy.github.io/the-necessary-tangle/",
        "A living evidence atlas of systems, complexity and cybernetics": "A living evidence atlas of systems | cybernetics | complexity",
        "<div class=\"header-meta\"><span id=\"releaseBadge\">Public alpha</span><span>Created and edited by Benjamin P Taylor</span></div>": "<div class=\"header-meta\"><span id=\"releaseBadge\">Public alpha</span><span>Curated by <a href=\"https://www.antlerboy.com/\">Benjamin P Taylor</a></span></div>",
        "<p class=\"eyebrow\">A public route into systems, complexity and cybernetics</p>": "<p class=\"eyebrow\">Systems | cybernetics | complexity</p>",
        "The Necessary Tangle shows what ideas mean, where they came from, what they depend on, how they developed, and how people use them in practice.": "The Necessary Tangle maps ideas, people, methods, publications, institutions, practices and lineages: what they mean, where they came from, what they depend on and how they are used.",
        "Search recognises standard names, abbreviations, alternate spellings and close matches.": "Search recognises maintained names, abbreviations, alternate spellings and close matches.",
        "Each journey develops an argument through a sequence of connected entries. Every named idea opens its full entry.": "Each journey develops an argument through connected entries. Named concepts in the steps open their full entries.",
        "Search for an entry to centre the map on it. Select any item to refocus. Select any line to inspect the claim and its sources.": "Search for an entry to centre the map. Select an item to refocus. Select a line to inspect the statement, its status and its sources.",
        "The precise claim and sources are examined.": "The precise statement and sources are examined.",
        "https://github.com/antlerboy-benjamintaylor/the-necessary-tangle": "https://github.com/antlerboy/the-necessary-tangle",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    if 'assets/site-enhancements.css' not in text:
        text = replace_once(
            text,
            '  <link rel="stylesheet" href="assets/styles.css">',
            '  <link rel="stylesheet" href="assets/styles.css">\n  <link rel="stylesheet" href="assets/site-enhancements.css">',
        )

    release_pattern = re.compile(
        r'        <aside class="hero-panel">\s*<p class="eyebrow">This release</p>\s*<div class="metrics" id="homeMetrics"></div>\s*<p class="small">.*?</p>\s*</aside>',
        re.S,
    )
    release_panel = '''        <a class="hero-panel release-panel" href="#view=about" aria-label="Read what this public alpha contains and what remains unfinished">
          <p class="eyebrow">This release</p>
          <div class="metrics" id="homeMetrics"></div>
          <p class="small">Broad seed coverage, a smaller evidence-deepened core, and an explicit programme for what comes next.</p>
          <span class="panel-link">Read what is covered, missing and next →</span>
        </a>'''
    text, count = release_pattern.subn(release_panel, text, count=1)
    if count == 0 and release_panel not in text:
        raise RuntimeError("Could not locate the release panel")

    text, count = re.subn(
        r'      <section class="author-strip">.*?</section>',
        AUTHOR_STRIP,
        text,
        count=1,
        flags=re.S,
    )
    if count == 0 and AUTHOR_STRIP not in text:
        raise RuntimeError("Could not locate the author strip")

    text, count = re.subn(
        r'    <section id="view-about" class="view">.*?</section>\s*</main>',
        ABOUT_SECTION + "\n  </main>",
        text,
        count=1,
        flags=re.S,
    )
    if count == 0 and ABOUT_SECTION not in text:
        raise RuntimeError("Could not locate the About view")

    footer = '''  <footer class="site-footer"><div><strong>The Necessary Tangle</strong><br><span>Curated by <a href="https://www.antlerboy.com/">Benjamin P Taylor</a></span></div><div><button data-view-link="contribute" class="text-button">Submit a correction</button><button data-view-link="about" class="text-button">Coverage, method and rights</button><a class="text-button" href="https://github.com/antlerboy/the-necessary-tangle" target="_blank" rel="noopener">GitHub</a></div></footer>'''
    text, count = re.subn(r'  <footer class="site-footer">.*?</footer>', footer, text, count=1, flags=re.S)
    if count == 0 and footer not in text:
        raise RuntimeError("Could not locate the footer")

    if 'assets/site-enhancements.js' not in text:
        text = replace_once(
            text,
            '  <script src="assets/app.js"></script>',
            '  <script src="assets/app.js"></script>\n  <script src="assets/site-enhancements.js"></script>',
        )

    forbidden = ["antlerboy-benjamintaylor", "Created and edited", "Creator and editor"]
    for phrase in forbidden:
        if phrase in text:
            raise RuntimeError(f"Obsolete public wording remains after patch: {phrase}")

    INDEX.write_text(text, encoding="utf-8")
    print("Patched docs/index.html for The Necessary Tangle 0.6-feedback-alpha")


if __name__ == "__main__":
    main()
